from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_async_session
from app.services.factura_service import FacturaService
from app.core.dependencies import get_current_user, require_roles
from app.models.usuario import Usuario
from app.schemas.factura import FacturaCreate, FacturaUpdate, FacturaResponse
from app.services.ocr_service import OCRService
from app.utils.parser import parse_factura_data
from app.services.llm_service import LLMService

router = APIRouter(prefix="/facturas", tags=["Facturas"])

ocr_service = OCRService()
llm_service = LLMService(model="llama3") # Cambia el modelo según lo que tengas en Ollama

@router.get("/", response_model=List[FacturaResponse])
async def listar_facturas(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user),
):
    service = FacturaService(db)
    
    # Restricción: Los usuarios normales solo ven sus propias facturas.
    # Los admin y contador ven TODO.
    if usuario_actual.rol and usuario_actual.rol.nombre in ["admin", "contador"]:
        return await service.obtener_todasFacturas(skip=skip, limit=limit, search=search)
    
    return await service.obtener_facturas_por_usuario(usuario_actual.id, skip=skip, limit=limit, search=search)


@router.get("/{id}", response_model=FacturaResponse)
async def obtener_factura(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user),
):
    service = FacturaService(db)
    factura = await service.obtenerFactura_por_id(id)
    
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Verificación de propiedad (si no es admin/contador)
    es_admin_o_contador = usuario_actual.rol and usuario_actual.rol.nombre in ["admin", "contador"]
    if not es_admin_o_contador and factura.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta factura")
        
    return factura


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(
    factura_data: FacturaCreate,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user), 
):
    service = FacturaService(db)
    return await service.crearFactura(factura_data, usuario_id=usuario_actual.id)


@router.put("/{id}", response_model=FacturaResponse)
async def actualizar_factura(
    id: int,
    factura_data: FacturaUpdate,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(require_roles(["admin", "contador"])),
):
    service = FacturaService(db)
    factura = await service.actualizarFactura(id, factura_data)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_factura(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(require_roles(["admin"])),
):
    service = FacturaService(db)
    success = await service.eliminarFactura(id)
    if not success:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return None

@router.post("/upload")
async def upload_factura(
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user),
    file: UploadFile = File(...)
):
    service = FacturaService(db)
    
    if usuario_actual.rol and usuario_actual.rol.nombre in ["admin", "contador", "user"]:
        import os
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
       
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # 1. Extracción de texto (OCR)
        if file.filename.lower().endswith('.pdf'):
            ocr_result = ocr_service.extraer_texto_desde_pdf(file_path)
            text = ocr_result["text_raw"]
            metodo_ocr = ocr_result["method"]
        else:
            text = ocr_service.extraer_texto_desde_imagen(file_path)
            metodo_ocr = "easyocr"
            
        # 2. Parseo inteligente con LLM (Ollama)
        try:
            datos_factura_dict = await llm_service.parse_factura(text)
            if not datos_factura_dict or "factura_numero" not in datos_factura_dict:
                raise Exception("LLM returned empty or invalid data")
            metodo_final = f"llm_ollama_{llm_service.model}"
        except Exception as e:
            # Fallback al parser tradicional de regex
            datos_factura_dict = parse_factura_data(text)
            metodo_final = f"regex_fallback_{metodo_ocr}"
            
        # 3. Completar datos adicionales
        datos_factura_dict["archivo"] = file_path
        datos_factura_dict["factura_metodoextraccion"] = metodo_final
        datos_factura_dict["factura_textocrudo"] = text[:1000] # Guardamos una muestra
        
        # 4. Crear registro en BD
        factura_data = FacturaCreate(**datos_factura_dict)
        nueva_factura = await service.crearFactura(factura_data, usuario_id=usuario_actual.id)
        
        return {
            "mensaje": "Factura procesada exitosamente",
            "metodo": metodo_final,
            "datos": nueva_factura
        }
    
    else:
        raise HTTPException(status_code=403, detail="No tienes permiso para cargar una factura")