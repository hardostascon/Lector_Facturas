import httpx
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = f"{base_url}/api/chat"

    async def parse_factura(self, text: str) -> Dict[str, Any]:
        """
        Envía el texto de la factura a un LLM local (Ollama) para extraer información estructurada en JSON.
        """
        prompt = f"""
        Eres un experto en extracción de datos de facturas. Tu tarea es extraer la información de la siguiente factura y devolverla estrictamente en formato JSON. 
        Si un campo no se encuentra, devuélvelo como null para strings o 0 para números.
        Devuelve SOLO el objeto JSON, nada de texto adicional.

        Campos a extraer:
        - facturador: Nombre de la empresa que emite la factura (ej. 'Restaurante El Sabor')
        - factura_numero: Texto del número de factura (ej. 'FE-123')
        - factura_fecha: Fecha en formato ISO (YYYY-MM-DD)
        - factura_monto: Valor TOTAL de la factura sin puntos ni comas (ej. 150000)
        - factura_moneda: Código de la moneda (USD, COP, EUR)
        - factura_impuestos: Valor de los impuestos (IVA) sin puntos ni comas
        - items: Una lista de objetos con la descripción detallada del producto o servicio, cantidad, precio unitario e impuesto (si aplica).

        Texto de la factura:
        ---
        {text}
        ---

        Formato de respuesta JSON esperado:
        {{
            "facturador": "Nombre empresa",
            "factura_numero": "Nro",
            "factura_fecha": "YYYY-MM-DD",
            "factura_monto": 0,
            "factura_moneda": "COP",
            "factura_impuestos": 0,
            "items": [
                {{
                    "descripcion": "Descripción item",
                    "cantidad": 1,
                    "precio_unitario": 0,
                    "impuesto": 0
                }}
            ]
        }}
        """

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json"
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(self.base_url, json=payload)
                response.raise_for_status()
                result = response.json()
                
                # Obtener el contenido del mensaje
                content = result.get("message", {}).get("content", "")
                
                # Intentar parsear el JSON de la respuesta
                parsed_data = json.loads(content)
                logger.info("Información de factura extraída exitosamente con LLM")
                return parsed_data

        except Exception as e:
            logger.error(f"Error llamando al LLM local: {str(e)}")
            # Fallback a un diccionario vacío si falla
            return {}
