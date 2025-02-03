import anthropic
import time


from .base_model import BaseModel


class Claude(BaseModel):

    def __init__(self,  model_name: str, api_key: str):
         
        super().__init__(model_name, api_key)
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_name = model_name
        
        
        
    def describe(self,  frame_urls: list, prompt: str):
        
        
        base64_images = [self.encode_image(url) for url in frame_urls]
        
        try:
            content_parts = [{"type": "text", "text": prompt}]
            content_parts.extend(
                [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image
                            }   
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
            
            response = self.client.messages.create(
            model=self.model_name,
            max_tokens=4096,
            messages=messages
                )
            
            end_time = time.time()
            
            out_text = response.content[0].text
            
            processing_time = end_time - start_time

            return processing_time, out_text
        
        except Exception as e:
            raise AttributeError(f"Error in Antrhopic VLM: {e}")
            
        


