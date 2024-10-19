from typing import List
from typing_extensions import TypedDict

class GraphState(TypedDict):
    
    """
    This state object will contain all the data 
    that we want to pass around the nodes
    """
    query : str
    relevance : str # detect if the user query is relevant to the chatbot job, or to the documentation provided
    documents = List[str]
    answer : str
    
    
# Define nodes