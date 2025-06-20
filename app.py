import warnings
import logging
import streamlit as st

def main():

    # Tirando avisos e erros desnecessários
    warnings.filterwarnings('ignore')
    logging.getLogger('transformers').setLevel(logging.ERROR)

    # Definindo o nome da página e o ícone
    st.set_page_config(page_title='AssistantAI', page_icon='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/ChatGPT-Logo.svg/512px-ChatGPT-Logo.svg.png?20240214002031')

    st.title('AssistantAI')

    # Verificando se já existem mensagens na sessão
    # Se não, inicializando a lista de mensagens
    if 'messages' not in st.session_state:
        st.session_state.messages = [] # Essa lista armazenará todas as mensagens do chat
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    # O código acima é responsável por redesenhar o histórico com mensagens anteriores, ao recarregar a página 

    st.subheader('Como posso ajudar?')
    prompt = st.chat_input('Pergunte alguma coisa sobre os PDFs enviados...', key='chat_input')

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        response = "Olá, sou o AssistantAI! Como posso ajudar você hoje?"
        st.chat_message('assistant').markdown(response)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
    
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
                    st.success('Arquivos processados com sucesso!')
                else:
                    st.info('Nenhum arquivo carregado. Por favor, carregue um arquivo PDF para começar.')
        except Exception as e:
            st.info(f'Erro ao carregar o arquivo {pdf_docs}. Verifique se o arquivo é um PDF válido.')


if __name__ == "__main__":

    main()