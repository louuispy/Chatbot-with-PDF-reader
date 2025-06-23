import os
from dotenv import load_dotenv
import tempfile
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

system_template = '''Você é um assistente de inteligência artificial simpático e profissional chamado Assistant. Você responde em Português do Brasil.
Você sempre responde de forma clara, objetiva e precisa as dúvidas dos usuários. Você responde com base no contexto: {context}'''

def create_vectorstore(uploaded_files):
    loaders = []
    for pdf in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf.read())
            tmp_path = tmp.name
        loaders.append(PyPDFLoader(tmp_path))
    
    for loader in loaders:
        docs = loader.load()
        for doc in docs:
            print("Trecho do PDF:", doc.page_content)

    index=VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    ).from_loaders(loaders)

    return index.vectorstore


def create_conversation_chain(vectorstore):
    llm = ChatGroq(
        groq_api_key=os.environ["GROQ_API_KEY"],
        model_name="llama3-8b-8192"
    )
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", "{question}")
        ])

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )

    return conversation_chain
