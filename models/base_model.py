from abc import ABC, abstractmethod
import requests
from PIL import Image
from io import BytesIO
import base64
import textwrap

class BaseModel(ABC):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

    @abstractmethod
    def describe(self, frame_urls: list, prompt: str):
        
        pass
    
    
    def clean_ocr_text(self, text : str):
        if text.startswith('<'):
            text = text[1:]
        return text.strip()


    def to_markdown(self, text: str):
        text = text.replace("•", "  *")
        return textwrap.indent(text, "<", predicate=lambda _: True)

    def encode_image(self, image_url: str) -> str:
        """
        Encode an image from a URL to base64.

        Args:
            image_url (str): URL of the image.

        Returns:
            str: Base64 encoded image.
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
        except Exception as e:
            raise AttributeError(f"Error encoding image from {image_url}: {str(e)}")
        
        
    def load_image(self, image_url):
        if image_url.startswith("https://storage.googleapis.com/videodb") or image_url.startswith(
                "https://storage.videodb.io"):
            response = requests.get(image_url)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
            else:
                raise AttributeError(f"Error encoding image from {image_url}: {str(e)}")
                
        else:
            try:
                return Image.open(image_url)
            except Exception as e:
                raise AttributeError(f"Error encoding image from {image_url}: {str(e)}")