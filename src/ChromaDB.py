from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma



class ChromaDB:
    def __init__(self, embedd_model_name, DBpath,file=None) -> None:
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedd_model_name)
        self.document = file
        self.DBpath = DBpath
    def saveDB(self):
        try:
            raw_documents = PyPDFLoader(self.document).load()
            if not raw_documents:
                raise ValueError("No documents were loaded")

            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=150)
            documents = text_splitter.split_documents(raw_documents)

            db = Chroma.from_documents(
                documents, self.embedding_model, persist_directory=self.DBpath
            )
            return db
        except Exception as e:
            print(f"Error saving database: {e}")

    def loadDB(self):
        db = Chroma(persist_directory=self.DBpath, embedding_function=self.embedding_model)        
        return db

# "/sentence-transformers/all-MiniLM-L6-v2"
if __name__ == "__main__":
    
    chroma = ChromaDB("sentence-transformers/all-MiniLM-L6-v2","../data/chromadb","../data/Applying_semi_empirical_simulation_of_wildfire_on_real_worldsatellite_imagery_data.pdf")
    
    chroma.saveDB()
    db = chroma.loadDB()
    docs = db.similarity_search_with_relevance_scores("What is the basis of the paper: 'Applying semi empirical simulation of wildfire on real worldsatellite imagery data' and what is the goal of it?",k=5)
    for doc in docs:
        print(doc)
        print('#######')