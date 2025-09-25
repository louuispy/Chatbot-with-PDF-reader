from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import ConversationChain

def create_conversation_chain(vectorstore, key):
    llm = ChatGroq(
        api_key=key,
        temperature=1,
        model="openai/gpt-oss-20b"
    )
    
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return conversation_chain

template = ChatPromptTemplate.from_messages([
        ("system", """Você é um assistente de inteligência artificial simpático e profissional. *Seu nome é Assistant.* Você responde no idioma de prompt do usuário. Você sempre responde de forma clara, objetiva e precisa as dúvidas dos usuários. Você responde com base no contexto fornecido pelos usuários. Além disso, caso o usuário diga palavras, como: "Tchau", "Xau", "OK", "Okay", "Obrigado", ou palavras semelhantes, isso representa que ele deseja encerrar a conversa, portanto, você deve responder: De nada! Gostaria de mais alguma ajuda?"""),
        ("user", "{history}, {input}")])

def create_conversation_without_pdf(key):
    llm = ChatGroq(
        api_key=key,
        temperature=1,
        model="openai/gpt-oss-20b",
    )

    conversation_chain_without_pdf = ConversationChain(
        llm=llm,
        prompt=template,
        verbose=True,
        memory=ConversationBufferMemory()
        )

    return conversation_chain_without_pdf