import time
import numpy as np
import easyocr

from .base_model import BaseModel

class Easyocr(BaseModel):

    def __init__(self,  model_name: str):
         
        super().__init__(model_name,"")
        
        self.model_name = model_name
        
        
        
    def describe(self, frame_urls, prompt):
        
        def extract_text_from_results(results):
            """Extracts text from a list of tuples containing bounding box data, text, and confidence scores."""
            extracted_text = []
            if results is None:
                return ""
            for result in results:
                text = result[1]  # Access the second element of each tuple (the text)
                extracted_text.append(text)
            return " ".join(extracted_text)
        
        
        images = [self.load_image(url) for url in frame_urls] 
       
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        
        try:   
            
            start_time = time.time()
            
            response = extract_text_from_results( reader.readtext(np.array(images[0])) )
            end_time = time.time()
            
            ocr_text = self.to_markdown(response)
            cleaned_ocr_text = self.clean_ocr_text(ocr_text)
            
            processing_time = end_time - start_time
        
            return processing_time, cleaned_ocr_text
        
        except Exception as e:
            raise AttributeError(f"Error in EasyOCR Model: {e}")
        
    


