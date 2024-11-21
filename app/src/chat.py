from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict
import uvicorn
import mychromadb as ch
from graph import makegraph
from ollama_setup import OllamaSetup

app = FastAPI()
OLLAMA_NGROK_URL = "https://c3fa-34-148-212-117.ngrok-free.app"
model = "llama3.2:3b"
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
k = 4
temperature = 0
whoami = "You are a knowledge managment assistant, users will ask you domain specific questions and you will answer them according to your experience"
document_description = """The document is the **Ubuntu Server Guide (2024 version)**, which serves as a comprehensive manual for installing, configuring, and managing an Ubuntu Server. It covers topics including:

- **Installation**: Step-by-step instructions for installing Ubuntu Server using various methods, such as bootable USB and network boot.
- **Configuration**: How to configure essential services like networking (NetPlan), storage, and security settings (firewall, user access, etc.).
- **Package Management**: Managing software with APT, third-party repositories, and upgrades.
- **Advanced Server Operations**: Guides for LDAP, Kerberos, virtualization, containers (LXC, Docker), VPNs, and high availability.
- **Web and Mail Services**: Setting up web servers (Apache, Nginx), databases (MySQL, PostgreSQL), and mail servers (Postfix, Dovecot).
- **Backup Solutions**: Methods for backups using tools like Bacula, rsnapshot, or shell scripts.

The guide includes tutorials, how-to guides, technical references, and resources for troubleshooting, ensuring that users can get the most out of their Ubuntu Server setup."""

top_p = 0.9

"""Works together with top-k. A higher value (e.g., 0.95) will lead
    to more diverse text, while a lower value (e.g., 0.5) will
    generate more focused and conservative text. (Default: 0.9)"""

top_k = 40

"""Reduces the probability of generating nonsense. A higher value (e.g. 100)
    will give more diverse answers, while a lower value (e.g. 10)
    will be more conservative. (Default: 40)"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

def chat_with_chatbot(user_query: str) -> str:
    """
    This function allows interaction with the chatbot and returns the response.
    """
    state = {
        "document_description": document_description,
        "conversation_history": []
    }

    # Initialize ollamaobject here
    ollamaobject = OllamaSetup(OLLAMA_NGROK_URL, model, temperature, top_p, top_k)
    ollamaobject.create_llm_instance()
    chroma = ch.ChromaDB(
        embedding_model,
        "../data/chromadb",
        [
            "../data/NIPS-2017-attention-is-all-you-need-Paper.pdf",
        ],
    )
    database = chroma.loadDB()
    graph = makegraph(ollamaobject, database)

    inputs = {
        "query": user_query,
        "document_description": state["document_description"],
        "conversation_history": [],
    }

    state["answer"] = ""

    for event in graph.stream(inputs, stream_mode="values"):
        if "answer" in event:
            state.update(event)

    return state["answer"]

@app.post("/chat")
async def chat(query_request: QueryRequest) -> Dict[str, str]:
    user_query = query_request.query
    if not user_query:
        return {"error": "No query provided"}
    
    response = chat_with_chatbot(user_query)
    return {"response": response}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
