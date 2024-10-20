from typing import List
from typing_extensions import TypedDict
import ChromaDB as ch
from Ollama1 import OllamaSetup
from langchain_core.messages import SystemMessage, HumanMessage
import json
from langgraph.graph import StateGraph
from IPython.display import Image, display


OLLAMA_NGROK_URL = "https://4b11-34-16-225-232.ngrok-free.app"
model = "llama3.2:3b"
temperature = 0.5


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

    ollama = OllamaSetup(OLLAMA_NGROK_URL, model, temperature)
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
        "sentence-transformers/all-MiniLM-L6-v2",
        "../data/chromadb",
        "../data/Applying_semi_empirical_simulation_of_wildfire_on_real_worldsatellite_imagery_data.pdf",
    )
    Database = chroma.loadDB()
    documents = Database.similarity_search(query=state["query"], k=4)
    # return {"documents": documents}
    state["documents"] = documents
    return "generator"


def generator(state):

    print("### Generate ###\n")
    ollama = OllamaSetup(OLLAMA_NGROK_URL, model, temperature)
    ollama.create_llm_instance()

    rag_system_prompt = [
        HumanMessage(
            content=f"""You are an assistant for question-answering tasks.

    Here is the context to use to answer the question:

    {state["documents"]}

    Think carefully about the above context.

    Now, review the user question:

    {state["query"]}

    Provide a detailed answer to this question, considering all relevant context. 

    Aim for clarity and completeness in your explanation.
    Answer:"""
        )
    ]
    state["answer"] = ollama.invoke_llm(rag_system_prompt)
    


def apology(state):

    ollama_setup = OllamaSetup(OLLAMA_NGROK_URL, model, temperature)
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
    return apology


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




######## Testing #########
# state = {
#     "query": "Can you explain The mathematical modeling of forest fires?",
#     "document_description": "A paper with the title 'Applying_semi_empirical_simulation_of_wildfire_on_real_worldsatellite_imagery_data' ",
#     "relevant": "",
#     "documents": [],
#     "answer": ""
# }

# # Execute the graph starting from the router
# workflow.execute(state)
# print(state["answer"])  # Print the generated answer
# Test on current events
inputs = {
    "query": "Can you explain The mathematical modeling of forest fires?",
    "document_description": "A paper with the title 'Applying_semi_empirical_simulation_of_wildfire_on_real_worldsatellite_imagery_data' ",
}
for event in graph.stream(inputs, stream_mode="values"):
    print(event)