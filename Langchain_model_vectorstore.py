
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

import getpass
import os
#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
#/Users/user/opt/miniconda3/envs/langchain2024/bin/python Langchain_model_vectorstore.py

#make vectors

#payments_guide
payments_guide = "Global_payments_guide.pdf"

def makellm():
    os.environ["OPENAI_API_KEY"] = getpass.getpass()
    llm = ChatOpenAI(model="gpt-4o")
    return llm

class VectorDatSource:
    def __init__(self, docs=None):
            self.docs = docs if docs else []
    
    def read_single_pdf(self, pdf_path):
        #SINGLE PDF
        file_path = pdf_path
        loader = PyPDFLoader(file_path)
        self.docs = loader.load()
        #print(len(docs))
        return self.docs
        
        
        
    def read_multiple_pdf(self,list_of_pdf):
        #example how file paths are organised
        #file_paths = [file_name,filepath2]
        
        # Load and combine documents from each PDF
        self.docs = []
        for path in list_of_pdf:
            loader = PyPDFLoader(path)
            self.docs.extend(loader.load())  # Append the loaded documents to the docs list

        #print(len(docs))
        return self.docs
    
    def vectorize_data(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=3500, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = InMemoryVectorStore.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )
        
        return vectorstore
        
    
class makeragchain() :
    
    def makechain(self,vectorstore,llm):
        # Load embeddings with a high-quality model
        embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
        retriever = vectorstore.as_retriever(
            embedding_model=embedding_model,
            search_type="similarity",
            search_kwargs={"k": 5, "similarity_threshold": 0.75}  # Adjust k and similarity threshold to get precise response
        )
        
        # Define prompt with concise answer instructions
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use only the retrieved context to answer accurately. "
            "If you can't find the information, reply 'Query not found.'\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # Create the RAG chain
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        return rag_chain

        


'''
if __name__ == "__main__":
    llm= makellm()
    print("LLM INITIATED",llm)
    ReadDocs= VectorDatSource()
    #doc= ReadDocs.read_single_pdf([payments_guide1,payments_guide2])
    doc= ReadDocs.read_single_pdf(payments_guide)
    vectorstore = ReadDocs.vectorize_data(doc)
    print("vectorstore created",vectorstore)
  
    
    # Run the query
    payment_rag_chain= makeragchain()
    rag_chain =payment_rag_chain.makechain(vectorstore)
    results = rag_chain.invoke({"input": "for Australia, what is payment formatting rules"})
    print(results["answer"]) 
    
    
'''