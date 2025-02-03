import time
from rapidocr_onnxruntime import RapidOCR

from .base_model import BaseModel

class Rapidocr(BaseModel):

    def __init__(self,  model_name: str):
         
        super().__init__(model_name,"")
        
        self.model_name = model_name
        
        
        
    def describe(self, frame_urls, prompt):
        
        def extract_text_from_results(results):
            """
            Extracts text from model output results.
            Each result is expected to be in the format:
            [[[x1, y1], [x2, y2], [x3, y3], [x4, y4]], text, confidence]
            
            Args:
                results (list): List of detection results
                
            Returns:
                list: List of extracted text strings
            """
        
            
            extracted_text = []
            
            # Access the list of detection results (before the final tuple)
            detection_results = results[0]
            if detection_results == None:
                return ""

            for result in detection_results:
                text = result[1]
                extracted_text.append(text)
            
            return " ".join(extracted_text)
        
        
        images = [self.load_image(url) for url in frame_urls]     
          
        model = RapidOCR()
        
        try:   
            
            start_time = time.time()
            
            response = extract_text_from_results( model(images[0]) )
            end_time = time.time()
            
            ocr_text = self.to_markdown(response)
            cleaned_ocr_text = self.clean_ocr_text(ocr_text)
            
            processing_time = end_time - start_time
        
            return processing_time, cleaned_ocr_text
        
        except Exception as e:
            raise AttributeError(f"Error in RapidOCR Model: {e}")