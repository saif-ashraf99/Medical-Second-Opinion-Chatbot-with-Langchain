from retriever.retriever_langchain import LangChainRetriever
from generator.generator_langchain import LangChainGenerator
from langchain.chains import RetrievalQA

class RAGLangChainModel:
    def __init__(self):
        self.retriever = LangChainRetriever()
        self.generator = LangChainGenerator()
        self.qa_chain = RetrievalQA(
            llm=self.generator.llm,
            retriever=self.retriever.index.as_retriever(),
            prompt=self.generator.prompt_template
        )

    def generate_response(self, question, patient_info):
        # Combine patient info with question
        query = f"{patient_info}\n{question}"
        # Generate response using RetrievalQA chain
        response = self.qa_chain.run(query)
        return response.strip()
