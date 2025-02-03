'''
Based on https://docs.moondream.ai/openai-compatibility
'''


from openai import OpenAI
import time

from .base_model import BaseModel

class Moondream(BaseModel):

    def __init__(self,  model_name: str, api_key: str):
         
        super().__init__(model_name, api_key)
        self.client = OpenAI( base_url="https://api.moondream.ai/v1", api_key=api_key)
        self.model_name = model_name
        
        
    def describe(self, frame_urls, prompt):
        
        
        base64_images = [self.encode_image(url) for url in frame_urls]
        
        try:
            
            content_parts = [{"type": "text", "text": prompt}]
            content_parts.extend(
                [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    }
                    for base64_image in base64_images
                ]
            )
            messages = [
                {
                    "role": "user",
                    "content": content_parts,
                }
            ]
    
    
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            
            end_time = time.time()

            out_text = response.choices[0].message.content.strip()

            processing_time = end_time - start_time

            return processing_time, out_text
        
        except Exception as e:
            print(f"Error in OPENAI VLM: {e}")
            return None
        


