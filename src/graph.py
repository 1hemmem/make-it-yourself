from typing import List
from typing_extensions import TypedDict
import mychromadb as ch
from ollama_setup import OllamaSetup
from langchain_core.messages import SystemMessage, HumanMessage
import json
from langgraph.graph import StateGraph
from IPython.display import Image, display

# User input data
OLLAMA_NGROK_URL = "https://cf44-35-240-163-56.ngrok-free.app"
model = "llama3.2:3b"
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
temperature = 0
whoami = "you are a cutomer support chatbot, the users expect you to be an expert of ubuntu and will ask you question about it"
top_p = 0.9
"""Works together with top-k. A higher value (e.g., 0.95) will lead
    to more diverse text, while a lower value (e.g., 0.5) will
    generate more focused and conservative text. (Default: 0.9)"""

top_k = 40
"""Reduces the probability of generating nonsense. A higher value (e.g. 100)
    will give more diverse answers, while a lower value (e.g. 10)
    will be more conservative. (Default: 40)"""


class GraphState(TypedDict):
    """
    This state object will contain all the data
    that we want to pass around the nodes
    """

    document_description: str
    query: str
    relevant: str
    documents: List[str]
    answer: str


def router(state):

    print("### Router ###\n")

    ollama = OllamaSetup(OLLAMA_NGROK_URL, model, temperature, top_p, top_k)
    ollama.create_llm_instance()
    router_system_prompt = [
        SystemMessage(
            content=f"""You are an expert at routing a user question to a vectorstore or web search.

        The vectorstore contains {state["document_description"]}.

        Use the vectorstore for questions on these topics. For all else, you are not required to provide an answer.

        Return JSON with single key, datasource, that is 'None' or 'vectorstore' depending on the question."""
        )
    ]
    route_question = ollama.invoke_llm_json(
        router_system_prompt + [HumanMessage(content=state["query"])]
    )
    source = json.loads(route_question)["datasource"]
    if source == "None":
        print("### Question irrelevant: Route to apology ###")
        return "None"

    elif source == "vectorstore":
        print("### Question Relevant: Route to retriver function")
        return "vectorstore"


def retriver(state):
    r"""
    This node is executed only if the output of the router was : "vectorstore"
    """
    print("### Retriver ###\n")
    chroma = ch.ChromaDB(
        embedding_model,
        "../data/chromadb",
        [
            "../data/Applying_semi_empirical_simulation_of_wildfire_on_real_worldsatellite_imagery_data.pdf",
            "../data/NIPS-2017-attention-is-all-you-need-Paper.pdf",
        ],
    )
    Database = chroma.loadDB()
    documents = Database.similarity_search(query=state["query"], k=4)
    # return {"documents": documents}
    state["documents"] = documents
    return state


def generator(state):

    print("### Generate ###\n")
    ollama = OllamaSetup(OLLAMA_NGROK_URL, model, temperature, top_p, top_k)
    ollama.create_llm_instance()

    # rag_system_prompt = [
    #     HumanMessage(
    #         content=f"""{whoami}

    # Here is the needed documentation to use to answer the question:

    # {state["documents"]}

    # Think carefully about the above context.

    # Now, review the user question:

    # {state["query"]}

    # Provide a detailed answer to this question, considering all relevant documentation.

    # Aim for clarity and completeness in your explanation.

    # If the question need to more explaination ask for it.

    # Answer:"""
    #     )
    # ]
    rag_system_prompt = [
        HumanMessage(
            content=f"""{whoami}

    Here is the needed documentation to use to answer the question:

    {state["documents"]}

    Think carefully about the above context.

    Now, review the user question:

    {state["query"]}

    Provide a **concise** and **to-the-point** answer to this question. Aim for brevity, but include the most relevant details.

    If the user asks for more details, provide them, but otherwise, keep the answer short and straightforward.
    
    Answer:"""
        )
    ]
    state["answer"] = ollama.invoke_llm(rag_system_prompt)
    return state


def apology(state):

    ollama_setup = OllamaSetup(OLLAMA_NGROK_URL, model, temperature, top_p, top_k)
    ollama_setup.setup_env()
    ollama_setup.create_llm_instance()
    apology_system_prompt = [
        SystemMessage(
            content=f"""you will be handling the cases where the user asks an irrelavant question.

    you are an expert of answering question only about {state["document_description"]}.

    Do not give any answer to the irrelavent question, just apologies and suggest to the user to ask you things relevant to your job."""
        )
    ]
    apology = ollama_setup.invoke_llm(system_prompt=apology_system_prompt)
    state["answer"] = apology
    return state


workflow = StateGraph(GraphState)

workflow.add_node("retriver", retriver)
workflow.add_node("apology", apology)
workflow.add_node("generator", generator)

workflow.set_conditional_entry_point(
    router,
    {
        "None": "apology",
        "vectorstore": "retriver",
    },
)

workflow.add_edge("retriver", "generator")

graph = workflow.compile()
# display(Image(graph.get_graph().draw_mermaid_png()))
# image_data = graph.get_graph().draw_mermaid_png()

# with open("graph_image.png", "wb") as f:
# f.write(image_data)

# state = {}

# inputs = {
#     "query": "How to configure a web server?",
#     "document_description": """The official documentation of ubuntu server, it contains all the technical knowledge you have to know,
#     all the configuration and anything related to ubuntu.""",
# }
# for event in graph.stream(inputs, stream_mode="values"):
#     state.update(event)

# print(state["answer"])


def chat_with_chatbot():
    """
    This function allows an interactive chat between you and the chatbot.
    The chat ends when you type 'exit'.
    """
    state = {
        "document_description": """The official documentation of ubuntu server, it contains all the technical knowledge you have to know,
        all the configuration and anything related to ubuntu."""
    }

    while True:
        # Get input from the user
        user_query = input("You: ")

        # Exit the chat if the user types 'exit'
        if user_query.lower() == "exit":
            print("Chat ended.")
            break

        # Update the query in the state
        inputs = {
            "query": user_query,
            "document_description": state["document_description"],
        }

        # Process the query through the workflow
        for event in graph.stream(inputs, stream_mode="values"):
            state.update(event)

        # Display the chatbot's answer
        print(f"Chatbot: {state['answer']}")


# Start the chat
chat_with_chatbot()
