from typing import List
from typing_extensions import TypedDict
import mychromadb as ch
from ollama_setup import OllamaSetup
from langchain_core.messages import SystemMessage, HumanMessage
import json
from langgraph.graph import StateGraph

# User input data
# OLLAMA_NGROK_URL = "https://c3fa-34-148-212-117.ngrok-free.app"
# model = "llama3.2:3b"
# embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
# k = 4
# temperature = 0
# whoami = "You are a knowledge managment assistant, users will ask you domain specific questions and you will answer them according to your experience"
# document_description = """The document is the **Ubuntu Server Guide (2024 version)**, which serves as a comprehensive manual for installing, configuring, and managing an Ubuntu Server. It covers topics including:

# - **Installation**: Step-by-step instructions for installing Ubuntu Server using various methods, such as bootable USB and network boot.
# - **Configuration**: How to configure essential services like networking (NetPlan), storage, and security settings (firewall, user access, etc.).
# - **Package Management**: Managing software with APT, third-party repositories, and upgrades.
# - **Advanced Server Operations**: Guides for LDAP, Kerberos, virtualization, containers (LXC, Docker), VPNs, and high availability.
# - **Web and Mail Services**: Setting up web servers (Apache, Nginx), databases (MySQL, PostgreSQL), and mail servers (Postfix, Dovecot).
# - **Backup Solutions**: Methods for backups using tools like Bacula, rsnapshot, or shell scripts.

# The guide includes tutorials, how-to guides, technical references, and resources for troubleshooting, ensuring that users can get the most out of their Ubuntu Server setup."""

# top_p = 0.9

# """Works together with top-k. A higher value (e.g., 0.95) will lead
#     to more diverse text, while a lower value (e.g., 0.5) will
#     generate more focused and conservative text. (Default: 0.9)"""

# top_k = 40

# """Reduces the probability of generating nonsense. A higher value (e.g. 100)
#     will give more diverse answers, while a lower value (e.g. 10)
#     will be more conservative. (Default: 40)"""


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

    Provide a **concise** and **to-the-point** answer to this question. Aim for brevity, but include the most relevant details.
    
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
