from transformers import AutoModel, AutoTokenizer
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma


class ChromaDB:
    def __init__(self, embedd_model_name, DBpath, files=None) -> None:
        # self.tokenizer = AutoTokenizer.from_pretrained(embedd_model_name, trust_remote_code=True)
        # self.model = AutoModel.from_pretrained(embedd_model_name, trust_remote_code=True)
        # self.embedding_model = HuggingFaceEmbeddings(model=self.model, tokenizer=self.tokenizer)
        
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=embedd_model_name
        )
        self.documents = files if files else []
        self.DBpath = DBpath

    def saveDB(self, chunk_size, chunk_overlap):
        try:
            all_documents = []
            for file in self.documents:
                raw_documents = PyPDFLoader(file).load()
                if not raw_documents:
                    print(f"No documents were loaded from {file}")
                    continue

                text_splitter = CharacterTextSplitter(
                    chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
                documents = text_splitter.split_documents(raw_documents)
                all_documents.extend(documents)

            if not all_documents:
                raise ValueError("No documents were processed from the provided files.")

            db = Chroma.from_documents(
                all_documents, self.embedding_model, persist_directory=self.DBpath
            )
            return db
        except Exception as e:
            print(f"Error saving database: {e}")

    def loadDB(self):
        db = Chroma(
            persist_directory=self.DBpath, embedding_function=self.embedding_model
        )
        return db
