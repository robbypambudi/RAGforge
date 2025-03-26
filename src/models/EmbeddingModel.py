
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:
    _token = None
    
    def __init__(self, model_name, model_kwargs, encode_kwargs)->HuggingFaceEmbeddings:
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.encode_kwargs = encode_kwargs
        
    def __call__(self):
        return HuggingFaceEmbeddings(model_name=self.model_name, model_kwargs=self.model_kwargs, encode_kwargs=self.encode_kwargs)