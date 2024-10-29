from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import logging
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from mychromadb import ChromaDB
from ollama_setup import OllamaSetup
from graph import  makegraph
import mychromadb as ch
from langgraph import graph

app = FastAPI()
OLLAMA_NGROK_URL = "https://6e29-34-127-120-178.ngrok-free.app"


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global_dict = {}

class QueryRequest(BaseModel):
    query: str


def chat_with_chatbot(
    user_query: str,
    document_description: str,
    graph: graph,
) -> str:
    """
    This function allows interaction with the chatbot and returns the response.
    """
    state = {"document_description": document_description, "conversation_history": []}

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


@app.post("/submit/")
async def submit_data(
    description: str = Form(...),
    selectedBase: str = Form(...),
    selectedEmbedding: str = Form(...),
    temperature: float = Form(...),
    top_p: float = Form(...),
    top_k: int = Form(...),
    pdfFiles: List[UploadFile] = File(...),
):
    try:
        # Save the uploaded PDF files
        uploaded_file_paths = []
        for file in pdfFiles:
            file_location = f"../data/{file.filename}"
            with open(file_location, "wb") as f:
                content = await file.read()
                f.write(content)
            uploaded_file_paths.append(file_location)

        # Log and return the form data for debugging
        logger.info(f"Description: {description}")
        logger.info(f"Selected Base: {selectedBase}")
        logger.info(f"Selected Embedding: {selectedEmbedding}")
        logger.info(f"Temperature: {temperature}")
        logger.info(f"Top P: {top_p}")
        logger.info(f"Top K: {top_k}")
        logger.info(f"Uploaded files: {uploaded_file_paths}")

        ## create the embedding dataset and the model

        ollamaobject = OllamaSetup(
            OLLAMA_NGROK_URL, selectedBase, temperature, top_p, top_k
        )
        ollamaobject.create_llm_instance()
        chroma = ch.ChromaDB(selectedEmbedding, "../data/chromadb", uploaded_file_paths)
        database = chroma.loadDB()
        graph = makegraph(ollamaobject, database)
        global_dict["graph"] = graph
        global_dict["document_description"] = description
        modelconfig = {
            "message": "Data received successfully",
            "description": description,
            "selectedBase": selectedBase,
            "selectedEmbedding": selectedEmbedding,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "uploaded_files": uploaded_file_paths,
        }
        return modelconfig
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/chat")
async def chat(query_request: QueryRequest) -> Dict[str, str]:
    user_query = query_request.query
    if not user_query:
        return {"error": "No query provided"}
    graph = global_dict["graph"]
    document_description = global_dict["document_description"]
    response = chat_with_chatbot(user_query,document_description,graph  )
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
