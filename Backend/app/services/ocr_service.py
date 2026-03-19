import fitz
import easyocr
import io
from typing import List, Dict, Any

class OCRService:
    def __init__(self):
        # Inicializar el lector de OCR (CPU por defecto para compatibilidad)
        self.reader = easyocr.Reader(['es'], gpu=False)
    
    def leer_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Lectura simple de texto de un PDF usando PyMuPDF."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return {"text": text}

    def extraer_texto_desde_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Intenta extraer texto de un PDF. Si no hay texto, usa OCR en las páginas.
        """
        text_raw = ""
        images_processed = 0
        doc = fitz.open(pdf_path)
        
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            if page_text.strip():
                text_raw += page_text + "\n"
            else:
                # Si la página está vacía (posible imagen), usar OCR
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                result = self.reader.readtext(img_bytes)
                for detection in result:
                    text_raw += detection[1] + " "
                images_processed += 1
                
        doc.close()
        
        return {
            "text_raw": text_raw.strip(),
            "images_processed": images_processed,
            "method": "mixed" if images_processed > 0 else "pymupdf"
        }
         
    def extraer_texto_desde_imagen(self, image_path: str) -> str:
        """Extrae texto de una imagen usando EasyOCR."""
        result = self.reader.readtext(image_path)
        text = " ".join([detection[1] for detection in result])
        return text