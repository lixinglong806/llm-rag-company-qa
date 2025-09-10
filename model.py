import warnings
warnings.filterwarnings('ignore')
from langchain.llms.base import LLM
from typing import Any, List, Optional
from openai import OpenAI
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
class RagLLM(object):
    client: Optional[Any] = None
    def __init__(self):
        super().__init__()
        self.client = OpenAI(base_url="http://localhost:11434/v1/",
                             # api_key="qwen2:72b",
                             api_key="llama3.2:latest" 

                             )

        
    def __call__(self, prompt : str, **kwargs: Any):
        completion = self.client.completions.create(model="llama3.2:latest",# need run ollma w/ the model
                                                    # model="qwen2:72b",
                                                    prompt=prompt,
                                                    temperature=kwargs.get('temperature', 0.1),
                                                    top_p=kwargs.get('top_p', 0.9),
                                                    max_tokens=kwargs.get('max_tokens', 4096), 
                                                    stream=kwargs.get('stream', False))
        if kwargs.get('stream', False):
            return completion
        return completion.choices[0].text
    

class QwenLLM(LLM):
    client: Optional[Any] = None
    def __init__(self):
        super().__init__()
        self.client = OpenAI(base_url="http://localhost:11434/v1/",
                             api_key="qwen2:72b")

        
    def _call(self, 
              prompt : str, 
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        completion = self.client.completions.create(model="qwen2:72b", 
                                                    prompt=prompt,
                                                    temperature=kwargs.get('temperature', 0.1),
                                                    top_p=kwargs.get('top_p', 0.9),
                                                    max_tokens=kwargs.get('max_tokens', 4096), 
                                                    stream=kwargs.get('stream', False))
        return completion.choices[0].text
    
    @property
    def _llm_type(self) -> str:
        return "rag_llm_qwen2_72b"
    

class Llama(LLM):
    client: Optional[Any] = None
    def __init__(self):
        super().__init__()
        self.client = OpenAI(base_url="http://localhost:11434/v1/",
                             api_key="llama3.2:latest")

        
    def _call(self, 
              prompt : str, 
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        completion = self.client.completions.create(model="llama3.2:latest", 
                                                    prompt=prompt,
                                                    temperature=kwargs.get('temperature', 0.1),
                                                    top_p=kwargs.get('top_p', 0.9),
                                                    max_tokens=kwargs.get('max_tokens', 4096), 
                                                    stream=kwargs.get('stream', False),
                                                    extra_body={"response_format": {"type": "json_object"}}
                                                   )
        return completion.choices[0].text
    
    @property
    def _llm_type(self) -> str:
        return "rag_llm_llama3.2_latest"

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
class RagEmbedding(object):
    def __init__(self, model_path="./data/llm_app/embedding_models/bge-m3/", 
                 device="cpu"):
        self.embedding = HuggingFaceEmbeddings(model_name=model_path,
                                               model_kwargs={"device": "cpu"})
    def get_embedding_fun(self):
        return self.embedding

        