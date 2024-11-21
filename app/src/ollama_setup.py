from langchain_ollama import OllamaLLM
import os
import subprocess
import mychromadb as DB

class OllamaSetup:
    def __init__(self, url: str, model: str, temperature: float,top_p: float, top_k:float,):
        self.url = url
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.llm = None
        self.llm_json_mode = None
        self.setup_env()

    def setup_env(self):
        os.environ["OLLAMA_HOST"] = self.url
        try:
            subprocess.run(["ollama", "pull", self.model], capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in pulling the model: {e}")

    def create_llm_instance(self):
        self.llm = OllamaLLM(base_url=self.url, model=self.model, temperature=self.temperature,top_p=self.top_p,top_k=self.top_k)
        self.llm_json_mode = OllamaLLM(base_url=self.url, model=self.model, format="json", temperature=self.temperature,top_p=self.top_p,top_k=self.top_k)

    def invoke_llm(self, system_prompt):
        return self.llm.invoke(system_prompt)

    def invoke_llm_json(self, system_prompt):
        return self.llm_json_mode.invoke(system_prompt)
