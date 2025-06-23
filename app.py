import warnings
import logging
import streamlit as st
from backend.rag_chatbot import create_vectorstore, create_conversation_chain

def main():

    warnings.filterwarnings('ignore')
    logging.getLogger('transformers').setLevel(logging.ERROR)

    st.set_page_config(page_title='AssistantAI', page_icon='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/ChatGPT-Logo.svg/512px-ChatGPT-Logo.svg.png?20240214002031')

    st.title('AssistantAI')
    st.subheader('Como posso ajudar?')

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None    
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.chat_input('Pergunte alguma coisa sobre os PDFs enviados...', key='chat_input')
    
    with st.sidebar:
        st.subheader('Seus arquivos')
        pdf_docs = st.file_uploader(
            label='Carregue seus arquivos PDF',
            type='pdf',
            accept_multiple_files=True
        )

        button_process = st.button('Processar PDFs')

        try:
            if button_process:
                if pdf_docs:
                    st.info('Arquivos enviados!')
                    vectorstore = create_vectorstore(pdf_docs)
                    st.info('Aguarde mais um pouco, estamos processando os arquivos...')
                    st.session_state.conversation = create_conversation_chain(vectorstore)
                    st.success('Arquivos processados com sucesso!')
                else:
                    st.info('Nenhum arquivo carregado. Por favor, carregue um arquivo PDF para começar.')
        except Exception as e:
            st.warning(f'Erro ao carregar o arquivo {e}')

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        if st.session_state.conversation is None:
            st.info("Por favor, carregue e processe seus PDFs clicando em 'Processar PDFs' antes de perguntar.")
        else:
            response = st.session_state.conversation.invoke({'question': prompt})
            st.chat_message('assistant').markdown(response['answer'])
            st.session_state.messages.append({'role': 'assistant', 'content': response['answer']})


if __name__ == "__main__":

    main()