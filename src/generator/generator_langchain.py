from langchain import LLMChain, PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory

import os

class LangChainGenerator:
    def __init__(self):
        self.llm = HuggingFaceHub(repo_id="gpt2", model_kwargs={"temperature": 0.7}, huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))  
        self.prompt_template = PromptTemplate(
            input_variables=['context', 'question'],
            template="""
            You are a medical assistant. Use the following context to answer the question.
            

            Context:
            {context}

            Question:
            {question}

            Answer:
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def generate(self, context, question):
        response = self.chain.run(context=context, question=question)
        return response.strip()
