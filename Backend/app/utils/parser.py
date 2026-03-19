import re
from datetime import datetime
from typing import Dict, Any, Optional

def clean_monto_str(val_str: str) -> float:
    """
    Limpia strings de montos para convertirlos a float.
    Maneja heurísticas para detectar si . o , son decimales o miles.
    """
    if not val_str: return 0.0
    
    # Quitar símbolos monetarios y otros caracteres no numéricos
    clean = re.sub(r'[^\d,\.]', '', val_str)
    if not clean: return 0.0
    
    # Caso común: termina en ,00 o .00 (centavos cero)
    if clean.endswith(',00') or clean.endswith('.00'):
        clean = clean[:-3]
        
    # Si tiene ambos (punto y coma), el último suele ser el decimal
    if '.' in clean and ',' in clean:
        if clean.find('.') < clean.find(','):
            clean = clean.replace('.', '').replace(',', '.')
        else:
            clean = clean.replace(',', '').replace('.', '.')
    # Si solo tiene uno, adivinamos por posición
    elif ',' in clean:
        # Si tiene exactamente 2 decimales después de la coma, es decimal
        if len(clean) - clean.rfind(',') == 3:
            clean = clean.replace(',', '.')
        else:
            # Es un punto de miles (ej: 1,000)
            clean = clean.replace(',', '')
    elif '.' in clean:
        # Si tiene exactamente 2 decimales después del punto, ya es formato float
        if len(clean) - clean.rfind('.') == 3:
            pass
        else:
            # Es un punto de miles (ej: 1.000)
            clean = clean.replace('.', '')
            
    try:
        return float(clean)
    except:
        return 0.0

def parse_factura_data(text: str) -> Dict[str, Any]:
    text_lines = [l.strip() for l in text.split('\n') if l.strip()]
    text_upper = text.upper()
    
    # 1. Facturador (Heurística mejorada para buscar "Razón Social" del vendedor)
    facturador = "DESCONOCIDO"
    vendedor_index = -1
    for i, line in enumerate(text_lines):
        if "DATOS DEL VENDEDOR" in line.upper():
            vendedor_index = i
            break
    
    if vendedor_index != -1:
        for i in range(vendedor_index, min(vendedor_index + 5, len(text_lines))):
            if "RAZÓN SOCIAL" in text_lines[i].upper() or "RAZON SOCIAL" in text_lines[i].upper():
                if i + 1 < len(text_lines):
                    facturador = text_lines[i+1][:50]
                    break

    if facturador == "DESCONOCIDO":
        if "SODIMAC" in text_upper: facturador = "SODIMAC COLOMBIA S.A."
        elif "EXITO" in text_upper: facturador = "ALMACENES EXITO S.A."
        elif "CARULLA" in text_upper: facturador = "CARULLA"
        elif "HOMECENTER" in text_upper: facturador = "SODIMAC / HOMECENTER"
        elif "SURTIFAMILIAR" in text_upper: facturador = "SURTIFAMILIAR"
        elif text_lines: facturador = text_lines[0][:30]

    # 2. Número de Factura (Añadido "DOCUMENTO")
    numero = "0"
    num_patterns = [
        r'(?:FACTURA|NRO|NO\.?|NUMERO|#|ORDEN|DOCUMENTO)\s*[:\-\s]?\s*([A-Z]*\d+[\-A-Z\d]*)',
        r'VT\s*(\d+)',
        r'FE\s*(\d+)'
    ]
    for p in num_patterns:
        matches = re.findall(p, text_upper)
        if matches:
            # Filtrar si es el CUSD (el numero de 50+ chars)
            valid_nums = [m for m in matches if 3 < len(m) < 20]
            if valid_nums:
                numero = valid_nums[0]
                break

    # 3. Monto Total
    monto_patterns = [
        r'(?:TOTAL|VALOR TOTAL|PAGAR|VENTA)\.?\s*[:\-\$]?\s*([\d\.,]{4,})',
        r'[\$]\s*([\d\.,]{4,})'
    ]
    
    vals = []
    for p in monto_patterns:
        matches = re.findall(p, text_upper)
        for m in matches:
            val = clean_monto_str(m)
            if val > 0: vals.append(val)

    monto_final = 0
    if vals:
        reasonable_vals = [v for v in vals if v < 100000000]
        if reasonable_vals:
            monto_final = max(reasonable_vals)

    # 4. Fecha
    fecha_match = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})', text)
    fecha_final = datetime.now().date()
    if fecha_match:
        try:
            f_str = fecha_match.group(0)
            for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%Y-%m-%d"):
                try:
                    fecha_final = datetime.strptime(f_str, fmt).date()
                    break
                except: continue
        except: pass

    # 5. Extract items
    items = []
    lines = text_lines
    
    blacklist = ["FACTURA", "ESTIMADO", "CLIENTE", "DIRECCION", "TELÉFONO", "FECHA", "VENCIMIENTO", 
                 "CONTADO", "SUBTOTAL", "RESOLUCION", "DIAN", "ELECTRONICA", "TRANSACCION", "CAJERO",
                 "TOTAL", "UNIDADES", "KILOS", "ITEMS", "VALORES", "GRAVADA", "EXCLUIDA", "IMPUESTOS", 
                 "CONTRIBUYENTES", "WWW", "PUNTOS", "EFECTIVO", "CAMBIO", "T.D", "MAESTRO", "MASTER",
                 "CALLE", "CLL", "CRA", "CARRERA", "AVENIDA", "AV.", "NIT", "RUT", "PBX", "CIUDAD",
                 "RESPONSABLE", "IVA", "PAGINA", "PBX", "COBRO", "REGIMEN", "COMENTARIOS", "COMENTARIO", "RAPPI", 
                 "RESTAURANTE", "MESA", "CAJERO", "ARTICULO", "CANT", "DESCUENTO", "DEVOLUCION", "PAGOS","COMENTARIOS"]
    
    stop_words = ["TOTAL", "PAGUE", "AHORRO", "T O T A L", "-------"]
    
    parsing_items = True
    for i in range(len(lines)):
        line = lines[i]
        
        if any(sw in line.upper() for sw in stop_words) and i > (len(lines) // 2):
            if items: parsing_items = False
        
        if not parsing_items: break

        # Heurística A: Alfanumérico Código
        # Puede ser un Nro de ítem (1, 2) o un SKU (AVA089)
        is_small_digit = line.isdigit() and len(line) < 3
        is_sku = line.isalnum() and 4 <= len(line) <= 18
        
        if is_small_digit or is_sku:
            nombre = ""
            start_search = i + 1
            
            # Si es un dígito pequeño, el SKU suele estar en i+1 y el NOMBRE en i+2
            if is_small_digit and i + 2 < len(lines):
                if lines[i+1].isalnum() and len(lines[i+1]) < 18:
                    nombre = lines[i+2]
                    start_search = i + 3
                else:
                    nombre = lines[i+1]
                    start_search = i + 2
            elif is_sku and i + 1 < len(lines):
                nombre = lines[i+1]
                start_search = i + 2
            
            if nombre:
                if any(word in nombre.upper() for word in blacklist): continue
                if any(c.isalpha() for c in nombre):
                    precio = 0
                    # Buscar precio hacia abajo
                    for j in range(start_search, min(start_search + 10, len(lines))):
                        p_match = re.search(r'([\d\.,]{4,})', lines[j])
                        if p_match:
                            val = clean_monto_str(p_match.group(1))
                            if val in [2024, 2025, 2026, 2027]: continue
                            if 100 < val < (monto_final + 5000):
                                precio = val
                                break
                    
                    if len(nombre) > 3 and precio > 1.0: # Precio debe ser real (> 1 COP)
                        # Evitar duplicados
                        if any(item["descripcion"].upper() == nombre[:100].upper() for item in items): continue
                        if any(word in nombre.upper() for word in blacklist): continue
                        
                        items.append({
                            "descripcion": nombre[:100],
                            "cantidad": 1.0,
                            "precio_unitario": precio,
                            "impuesto": 0.0
                        })
                        
    if not items or len(items) < 1:
        # Fallback B: Búsqueda por texto largo
        parsing_items = True
        for i in range(len(lines)):
            line = lines[i]
            if any(sw in line.upper() for sw in stop_words) and i > (len(lines) // 2):
                 if items: parsing_items = False
            if not parsing_items: break

            # Si la línea está en la lista negra, saltar
            if any(word in line.upper() for word in blacklist): continue
            
            if len(line) > 8 and any(c.isalpha() for c in line) and not any(c == ':' for c in line):
                 for j in range(i+1, min(i+6, len(lines))):
                     p_match = re.search(r'([\d\.,]{4,})', lines[j])
                     if p_match:
                         val = clean_monto_str(p_match.group(1))
                         if val in [2024, 2025, 2026, 2027]: continue
                         if 100 < val < (monto_final + 1000):
                             items.append({
                                "descripcion": line[:100],
                                "cantidad": 1.0,
                                "precio_unitario": val,
                                "impuesto": 0.0
                             })
                             break
    
    # 6. Taxes (HEURÍSTICA MEJORADA)
    impuestos = 0
    # Buscamos patrones de impuestos al consumo e IVA
    iva_patterns = [
        r'(?:IVA|INC|IMPUESTO|CONSUMO)\s*[:\-\$]?\s*([\d\.,]{5,})', # Subimos a 5 para ignorar años
        r'(?:IVA|INC|IMPUESTO|CONSUMO)[^0-9]*([\d\.,]{4,20})'
    ]
    for p in iva_patterns:
        matches = re.findall(p, text_upper)
        if matches:
            for m in matches:
                val = clean_monto_str(m)
                if 100 < val < monto_final: # Impuesto reasonable > 100 COP
                    impuestos = val
                    break
            if impuestos > 0: break

    return {
        "facturador": facturador,
        "factura_numero": numero,
        "factura_fecha": fecha_final,
        "factura_monto": monto_final,
        "factura_impuestos": impuestos,
        "factura_moneda": "COP",
        "items": items
    }
   