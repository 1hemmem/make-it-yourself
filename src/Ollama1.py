from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
import os
import subprocess
import ChromaDB as DB

class OllamaSetup:
    def __init__(self, url: str, model: str, temperature: float):
        self.url = url
        self.model = model
        self.temperature = temperature
        self.llm = None
        self.llm_json_mode = None
        self.setup_env()

    def setup_env(self):
        os.environ["OLLAMA_HOST"] = self.url
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU
        try:
            subprocess.run(["ollama", "pull", self.model], capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in pulling the model: {e}")

    def create_llm_instance(self):
        self.llm = OllamaLLM(base_url=self.url, model=self.model, temperature=self.temperature)
        self.llm_json_mode = OllamaLLM(base_url=self.url, model=self.model, format="json", temperature=self.temperature)

    def invoke_llm(self, system_prompt):
        return self.llm.invoke(system_prompt)

    def invoke_llm_json(self, system_prompt):
        return self.llm_json_mode.invoke(system_prompt)


if __name__ == "__main__":
    
    # User inputs
    document_subjects_ = "the policies and rules of facebook, the documentation and the help center, the answer of any technical problem you might have about this platform."
    user_query = "What is the basis of the paper: 'Applying semi empirical simulation of wildfire on real world satellite imagery data' and what is the goal of it"
    temperature = 0.5

    # Set up Ollama LLM
    OLLAMA_NGROK_URL = "https://15c6-35-197-67-52.ngrok-free.app"
    model = "llama3.2:3b"

    # Create and configure the Ollama LLM
    ollama_setup = OllamaSetup(OLLAMA_NGROK_URL, model, temperature)
    ollama_setup.setup_env()
    ollama_setup.create_llm_instance()

    