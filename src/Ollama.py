from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
import os
import subprocess
import ChromaDB as DB


def setup_env(url: str, model: str):
    os.environ["OLLAMA_HOST"] = url
    try:
        subprocess.run(["ollama", "pull", model], capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e)


if __name__ == "__main__":
    # User inputs

    document_subjects_ = "the policies and rules of facebook, the documentation and the help center, the answer of any technical problem you might have about this platform."
    
    # Controll the temperature and all the other parameters
    temperature = 0.5
    

    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    OLLAMA_NGROK_URL = "https://b25b-34-124-148-219.ngrok-free.app"
    model = "llama3.2:3b"

    ## What the document describe as an input
    # The format is: "The document contains ...."
    setup_env(OLLAMA_NGROK_URL, model)

    # Create an instance of Ollama connected to the ngrok-exposed URL
    llm = OllamaLLM(base_url=OLLAMA_NGROK_URL, model=model,temperature=temperature)
    llm_json_mode = OllamaLLM(base_url=OLLAMA_NGROK_URL, model=model, format="json",temperature=temperature)

    user_query = "What is the basis of the paper: 'Applying semi empirical simulation of wildfire on real worldsatellite imagery data' and what is the goal of it"
    #     routing_system_prompt = [
    #         SystemMessage(
    #             content=f"""You are an expert at routing a user question to a vectorstore or web search.

    #     The vectorstore contains {document_subjects_}.

    #     Use the vectorstore for questions on these topics. For all else, you are not required to provide an answer.

    #     Return JSON with single key, datasource, that is 'None' or 'vectorstore' depending on the question."""
    #         )
    #     ]

    #     respond = llm_json_mode.invoke(
    #         routing_system_prompt
    #         + [
    #             HumanMessage(
    #                 content="I have a problem logging in to my account, can you help me?"
    #             )
    #         ]
    #     )
    #     print(json.loads(respond))

    #     appology_system_prompt = [
    #         SystemMessage(
    #             content=f"""you are an expert of generating apology messages, the questions that you will be handling are irrelevant to your experience and answering it isn't your task.

    # you know everything about {document_subjects_}

    # Do not give any answer to the irrelavent question, just apologies and suggest to the user to ask you things relevant to your job."""
    #         )
    #     ]

    #     respond = llm.invoke(
    #         appology_system_prompt
    #         + [HumanMessage(content=f"{user_query}")]
    #     )
    #     print(respond)
    db = DB.ChromaDB(
        embedd_model_name="sentence-transformers/all-MiniLM-L6-v2",
        DBpath="../data/chromadb",
    )
    db = db.loadDB()
    # rag_system_prompt = [
    #     HumanMessage(
    #         content=f"""You are an assistant for question-answering tasks. 

    # Here is the context to use to answer the question:

    # {context} 

    # Think carefully about the above context. 

    # Now, review the user question:

    # {user_query}

    # Provide an answer to this questions using only the above context. 

    # Use three sentences maximum and keep the answer concise.

    # Answer:"""
    #     )
    # ]
    while True:
        question = input("user: ")
        context = db.similarity_search(user_query,k=4)
        rag_system_prompt = [
        HumanMessage(
            content=f"""You are an assistant for question-answering tasks.

        Here is the context to use to answer the question:

        {context}

        Think carefully about the above context.

        Now, review the user question:

        {question}

        Provide a detailed answer to this question, considering all relevant context. 
        
        However, you should not be talking about a provided document or somthing like that, you have to speake with confidance.

        Aim for clarity and completeness in your explanation.
        Answer:"""
            )
        ]
        respond = llm.invoke(rag_system_prompt)
        print(respond)