from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings

def create_vectorstore(chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name='intfloat/multilingual-e5-base')
    vectorstore = FAISS.from_texts(texts = chunks, embedding=embeddings)

    return vectorstore