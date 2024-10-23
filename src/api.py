from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import logging
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mychromadb import ChromaDB
from ollama_setup import OllamaSetup
from graph import chat_with_chatbot


app = FastAPI()

OLLAMA_NGROK_URL = "https://edac-34-80-16-214.ngrok-free.app"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS middleware to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        
        chroma = ChromaDB(selectedEmbedding,"../data/chromadb",uploaded_file_paths)
        db = chroma.saveDB(1000,150)
        
        print(db)
        ## when the creation is done return a message
        
        ollama = OllamaSetup(OLLAMA_NGROK_URL,selectedBase,temperature,top_p,top_k)
        ollama.create_llm_instance()
        chat_with_chatbot()
        
        return {
            "message": "Data received successfully",
            "description": description,
            "selectedBase": selectedBase,
            "selectedEmbedding": selectedEmbedding,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "uploaded_files": uploaded_file_paths,
        }
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
