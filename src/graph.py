from typing import List
from typing_extensions import TypedDict
import mychromadb as ch
from ollama_setup import OllamaSetup
from langchain_core.messages import SystemMessage, HumanMessage
import json
from langgraph.graph import StateGraph

class GraphState(TypedDict):
    conversation_history: List[str]
    document_description: str
    query: str
    relevant: str
    documents: List[str]
    answer: str


def router(state, ollamaobject: OllamaSetup):

    router_system_prompt = [
        SystemMessage(
            content=f"""You are an expert at routing a user question to either using vectorstore to answer it or declaring it as irrelavant.

        The vectorstore contains {state["document_description"]}.

        Use the vectorstore for questions on these topics. For all else, you are not required to provide an answer.

        Return JSON with single key, datasource, that is 'None' or 'vectorstore' depending on the question."""
        )
    ]
    route_question = ollamaobject.invoke_llm_json(
        router_system_prompt + [HumanMessage(content=state["query"])]
    )
    source = json.loads(route_question)["datasource"]
    if source == "None":
        print("### Question irrelevant: Route to apology ###")
        return "None"

    elif source == "vectorstore":
        print("### Question Relevant: Route to retriver function")
        return "vectorstore"


def retriver(state, database):
    r"""
    This node is executed only if the output of the router was : "vectorstore"
    """
    print("### Retriver ###\n")
    documents = database.similarity_search(query=state["query"], k=5)
    state["documents"] = documents
    return state


def generator(state, ollamaobject: OllamaSetup):
    conversation_history = "\n".join(
        [f"User: {q}\nAssistant: {a}" for q, a in state["conversation_history"]]
    )

    rag_system_prompt = [
        HumanMessage(
            content=f"""You are a knowledge managment assistant, users will ask you domain specific questions and you will answer them according to your experience

    Here is the needed documentation to use to answer the question:

    {state["documents"]}

    Think carefully about the above context and the conversation so far:

    {conversation_history}

    Now, review the new user question:

    {state["query"]}
    
    Always end the answer with a question to provide more details if needed or offering more help. 

    Answer:"""
        )
    ]
    state["answer"] = ollamaobject.invoke_llm(rag_system_prompt)
    state["conversation_history"].append((state["query"], state["answer"]))
    return state


def apology(state, ollamaobject):

    conversation_history = "\n".join(
        [f"User: {q}\nAssistant: {a}" for q, a in state["conversation_history"]]
    )

    apology_system_prompt = [
        SystemMessage(
            content=f"""You will be handling cases where the user asks an irrelevant question to your specific domain.

    You are an expert at answering questions only about {state["document_description"]}.

    Previous conversation:

    {conversation_history}

    The user question is:

    {state["query"]}

    Apologize politely and suggest they ask questions relevant to your domain."""
        )
    ]

    apology = ollamaobject.invoke_llm(system_prompt=apology_system_prompt)
    state["answer"] = apology
    state["conversation_history"].append((state["query"], state["answer"]))
    return state


def makegraph(ollamaobject: OllamaSetup, database):
    workflow = StateGraph(GraphState)

    workflow.add_node("retriver", lambda state: retriver(state, database))
    workflow.add_node("apology", lambda state: apology(state, ollamaobject))
    workflow.add_node("generator", lambda state: generator(state, ollamaobject))

    workflow.set_conditional_entry_point(
        lambda state: router(state, ollamaobject),
        {
            "None": "apology",
            "vectorstore": "retriver",
        },
    )

    workflow.add_edge("retriver", "generator")

    graph = workflow.compile()
    return graph


# def chat_with_chatbot():
#     """
#     This function allows an interactive chat between you and the chatbot.
#     The chat ends when you type 'exit'.
#     """
#     state = {"document_description": document_description}

#     print("Building the model...")

#     # Initialize ollamaobject here
#     ollamaobject = OllamaSetup(OLLAMA_NGROK_URL, model, temperature, top_p, top_k)
#     ollamaobject.create_llm_instance()
#     chroma = ch.ChromaDB(
#         embedding_model,
#         "../data/chromadb",
#         [
#             # "../data/Applying_semi_empirical_simulation_of_wildfire_on_real_worldsatellite_imagery_data.pdf",
#             "../data/NIPS-2017-attention-is-all-you-need-Paper.pdf",
#         ],
#     )
#     database = chroma.loadDB()
#     # Pass the ollamaobject to the graph
#     graph = makegraph(ollamaobject, database)

#     print("Model built")

#     while True:
#         user_query = input("You: ")

#         if user_query.lower() == "exit":
#             print("Chat ended.")
#             break

#         inputs = {
#             "query": user_query,
#             "document_description": state["document_description"],
#             "conversation_history": [],
#         }

#         state["answer"] = ""

#         print("Chatbot:", end=" ", flush=True)
#         for event in graph.stream(inputs, stream_mode="values"):
#             if "answer" in event:
#                 state.update(event)
#                 print(event["answer"], end="", flush=True)

#         print()
