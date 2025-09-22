import warnings
import logging
import streamlit as st
from utils import text
#from rag_chatbot import create_vectorstore, create_conversation_chain

def main():

    warnings.filterwarnings('ignore')
    logging.getLogger('transformers').setLevel(logging.ERROR)

    st.set_page_config(page_title='AssistantAI', page_icon='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/ChatGPT-Logo.svg/512px-ChatGPT-Logo.svg.png?20240214002031')

    st.title('AssistantAI')
    st.subheader('Como posso ajudar?')


    
    with st.sidebar:
        st.subheader('Insira sua chave de API Groq')
        GROQ_API_KEY = st.text_input('Insira sua chave de API Groq', key='groq_api_key', type='password')
        button_process_api = st.button('Enviar chave de API')

        try:
            if button_process_api:
                if GROQ_API_KEY:
                    st.info('Chave de API enviada!')
                    st.session_state.GROQ_API_KEY = GROQ_API_KEY
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
                    st.success('Arquivos processados com sucesso!')
                    print(all_files_text)
                else:
                    st.info('Nenhum arquivo carregado. Por favor, carregue um arquivo PDF para começar.')
        except Exception as e:
            st.warning(f'Erro ao carregar o arquivo {e}')

if __name__ == "__main__":

    main()