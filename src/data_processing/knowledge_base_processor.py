import os
from tqdm import tqdm
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

class KnowledgeBaseProcessor:
    def __init__(self, model_name='sentence-transformers/msmarco-distilbert-base-v4'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.doc_embeddings = None
        self.doc_texts = []
        self.doc_ids = []

    def load_documents(self, docs_path):
        print("Loading knowledge base documents...")
        for doc_file in tqdm(os.listdir(docs_path)):
            doc_id = doc_file
            with open(os.path.join(docs_path, doc_file), 'r', encoding='utf-8') as f:
                text = f.read()
                self.doc_texts.append(text)
                self.doc_ids.append(doc_id)
        print(f"Loaded {len(self.doc_texts)} documents.")

    def build_embeddings(self):
        print("Generating document embeddings...")
        self.doc_embeddings = self.model.encode(self.doc_texts, show_progress_bar=True)

    def build_index(self, index_path):
        print("Building FAISS index...")
        dimension = self.doc_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.doc_embeddings)

        # Save index and document metadata
        faiss.write_index(self.index, os.path.join(index_path, 'kb_index.faiss'))
        with open(os.path.join(index_path, 'doc_ids.pkl'), 'wb') as f:
            pickle.dump(self.doc_ids, f)
        print("Index built and saved.")

    def process(self, docs_path, index_path):
        self.load_documents(docs_path)
        self.build_embeddings()
        self.build_index(index_path)

if __name__ == '__main__':
    docs_path = 'data/knowledge_base/documents'
    index_path = 'data/knowledge_base/index'
    os.makedirs(index_path, exist_ok=True)

    kb_processor = KnowledgeBaseProcessor()
    kb_processor.process(docs_path, index_path)
