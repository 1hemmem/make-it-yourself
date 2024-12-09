# Make It Yourself

## About this project

Make It Yourself is a web application designed to help you create customizable, domain-specific chatbots powered by state-of-the-art AI models. Whether you're building a chatbot for software guidance, educational purposes, or cases where you don't want to share your private data but still want to ask 

It provide also a good level of flexibility when building your assistant:

- **Rich Selection of Models**:
  - **LLMs**: Choose from powerful options like Llama 3.2, Llama 3.1, Gemma 2, Phi 3.5, and more.
  - **Embedding Models**: Options include NVIDIA/NV-Embed-v2, BAAI/bge-en-icl, Sentence-Transformers/all-MiniLM-L6-v2, and more.
- **Hyperparameter Customization** Adjust temperature, top-p, and top-k for tailored responses
- **Dynamic Relevance Detection** The chatbot's pipeline intelligently determines if a question is relevant to your uploaded documents and provides appropriate responses or guidance.

### Wokflow

**Configuration:**

- Upload your PDF along with a description of the document content.
- Select an embedding model, LLM, and fine-tune hyperparameters.

**Chatbot Pipeline:**

- Router: Determines if a question is relevant to the uploaded document or irrelevant, if it was relevant it will be sent to the retriever, if not it will be handled by the apologizer.
- Apologizer: Generates polite responses for irrelevant queries.
- Retriever: Finds the most relevant document chunks using similarity search.
- Generator: Creates the final answer using retrieved documents and the user question.

**Testing:**

Start interacting with your chatbot and refine its behavior as needed.

## Setup

### ollama-server

- Copy the `ollama-server.ipynb` code and put it in google colab
- Sign up in ngrok and get an authentication token and put it where I have commented in the code. [Get Ngrok](https://ngrok.com/)
- run the code in the T4 GPU.

### backend-server

- install ollama locally : [Get Ollama](https://ollama.com/)
- Change the path :
  `cd /app/src`
- Install the required libraries:
  `pip install -r requirements.txt`
- Plug the endpoint generated from the ollama-server to the `api.py` file
- Run the api:
  `python -m uvicorn api:app --host 0.0.0.0 --port 8000`

### frontend

- Change the path:
  `cd /frontend`
- Install required packages:
  `npm install`
- Run the react app :
  `npm run dev`



## Futur work

**Multi-Instance Testing:**
- Compare multiple chatbot configurations side by side.

**Enhanced Workflow Control:**
- Fine-tune similarity search functions.
- Adjust document chunking strategies.
- Retrieve a custom number of documents (k).

**Improved Accuracy:**
- Add hallucination checking node.



<!-- 


- Implemetation of multi-instance testing
- Give more control over the workflow parameters: similarity search function, k: number of documents retrieved, document chuncking strategy
- Improving the results with hellucination check. -->
