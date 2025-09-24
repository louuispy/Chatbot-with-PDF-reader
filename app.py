import warnings
import logging
import os
import streamlit as st
from streamlit_chat import message
from utils import process_embeddings, text, chatbot
#from rag_chatbot import create_vectorstore, create_conversation_chain

def main():

    warnings.filterwarnings('ignore')
    logging.getLogger('transformers').setLevel(logging.ERROR)

    st.set_page_config(page_title='AssistantAI', page_icon='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/ChatGPT-Logo.svg/512px-ChatGPT-Logo.svg.png?20240214002031')

    st.title('AssistantAI')
    st.subheader('Como posso ajudar?')
    
    user_question = st.chat_input('Escreva sua pergunta...')

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_chain' not in st.session_state:
        st.session_state.conversation_chain = None    
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    if (user_question):
        response = st.session_state.conversation_chain(user_question)

        st.chat_message('user').markdown(user_question)
        st.session_state.messages.append({'role': 'user', 'content': user_question})

        st.chat_message('assistant').markdown(response['answer'])
        st.session_state.messages.append({'role': 'assistant', 'content': response['answer']})

    with st.sidebar:
        st.subheader('Insira sua chave de API Groq')
        input_api_key = st.text_input('Insira sua chave de API Groq', key='groq_api_key', type='password')
        button_process_api = st.button('Enviar chave de API')

        try:
            if button_process_api:
                if input_api_key:
                    st.info('Chave de API enviada!')
                    st.session_state.api_key = input_api_key
                else:
                    st.warning('Nenhuma chave de API inserida! Por favor, insira uma chave de API.')

        except Exception as e:
            st.warning(f'Erro ao enviar a chave de API {e}')

        st.subheader('Seus arquivos')
        pdf_docs = st.file_uploader(
            label='Carregue seus arquivos PDF',
            type='pdf',
            accept_multiple_files=True
        )

        button_process_pdf = st.button('Processar PDFs')

        try:
            if button_process_pdf:
                if pdf_docs:
                    st.info('Arquivos enviados!')
                    all_files_text = text.process_files(pdf_docs)

                    st.info('Aguarde mais um pouco, estamos processando os arquivos...')
                    chunks = text.create_text_chunks(all_files_text)
                    vectorstore = process_embeddings.create_vectorstore(chunks)
                    st.session_state.conversation_chain = chatbot.create_conversation_chain(vectorstore, st.session_state.api_key)
                    
                    st.success('Arquivos processados com sucesso!')
                else:
                    st.info('Nenhum arquivo carregado. Por favor, carregue um arquivo PDF para começar.')
        except Exception as e:
            st.warning(f'Erro ao carregar o arquivo {e}')

if __name__ == "__main__":

    main()