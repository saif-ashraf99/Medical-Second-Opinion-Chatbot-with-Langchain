from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.document_loaders import UnstructuredFileLoader

class LangChainRetriever:
    def __init__(self, docs_path='data/knowledge_base/documents'):
        self.docs_path = docs_path
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.index = None

    def build_index(self):
        # Load documents
        loader = DirectoryLoader(self.docs_path, glob='*.txt', loader_cls=TextLoader)
        documents = loader.load()
        # Split documents
        texts = self.text_splitter.split_documents(documents)
        # Create vector store
        self.index = FAISS.from_documents(texts, self.embeddings)

    def retrieve(self, query, top_k=5):
        if self.index is None:
            self.build_index()
        docs = self.index.similarity_search(query, k=top_k)
        return docs
