import Langchain_model_vectorstore
from Langchain_model_vectorstore import *
import random
import gradio as gr
import os 
import getpass

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

payments_guide = "Global_payments_guide.pdf"

def makellm():
    os.environ["OPENAI_API_KEY"] = getpass.getpass()
    llm = ChatOpenAI(model="gpt-4o")
    return llm



def random_response(message, history):  
     
    #retrive the answer from vectorstore
    results = rag_chain.invoke({"input": message})
    #results["answer"] is the response 
    #print(results["answer"])
    
    #check is the message is actually valid
    if len(message) >=15:
        
        # Assuming 'results' is the dictionary containing 'input' and 'context' keys
        documents = results['context']  # 'context' holds a list of Document objects
        
        #here we get the responses
        source_list=[]
        for doc in documents:
            # Extract each attribute from the Document
            source = doc.metadata.get('source')
            page = doc.metadata.get('page')
            source_list.append(str(f'Page No: {page} {source}'))
        print(source_list)
        return str(results["answer"]) + "\n SOURCES :" + str(source_list)

    else:
        return str(results["answer"]) 

    
    
#chatbot CSS   
css= """
        .gradio-container {
            background: #ebeef3 !important;
        }

        .user.svelte-5ng3n.svelte-5ng3n {
        border:#344ca4;
        background-color:#cee3f9;
        }

        .gradio-container-5-5-0 {
        width: 60% !important;
        }

        .element.style {
        background: #ebeef3 !important;
        }
        .pending.svelte-1gpwetz {
        background:#f8f8f8
        }
"""

custom_header = """
<div style="display: flex; align-items: center; gap: 10px;">
    <img src="https://via.placeholder.com/50" alt="Logo" style="height: 50px;"/>
    <h1 style="margin: 0;">My Chatbot</h1>
</div>
"""

demo = gr.ChatInterface(random_response, 
                        description="""
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a4/Paypal_2014_logo.png" alt="Logo" style="height: 50px;"/>
                            <span style="font-size: 30px; font-weight:600;">Payments Documents Chat Help</span>
                        </div>
                        """,
                        css= css,  
                        type="messages")


if __name__ == "__main__":
    llm= makellm()
    #enter your OAI key
    print("LLM INITIATED",llm)
    ReadDocs= VectorDatSource()
    #doc= ReadDocs.read_single_pdf([payments_guide1,payments_guide2])
    doc= ReadDocs.read_single_pdf(payments_guide)
    print("creating vectors ... pls wait")
    vectorstore = ReadDocs.vectorize_data(doc)
    print("vectorstore created",vectorstore)
  
    
    # Run the query
    payment_rag_chain= makeragchain()
    rag_chain =payment_rag_chain.makechain(vectorstore,llm)
    
    #Model Inference test
    #results = rag_chain.invoke({"input": "for Australia, what is payment formatting rules"})
    #print(results["answer"]) 
    
    print("Launching Gradio")
    demo.launch(share=True)