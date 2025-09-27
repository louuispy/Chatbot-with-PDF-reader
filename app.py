import warnings
import logging
import streamlit as st
from utils import process_embeddings, text, chatbot, youtube_transcription

def main():

    warnings.filterwarnings('ignore')
    logging.getLogger('transformers').setLevel(logging.ERROR)

    st.set_page_config(
        page_title='AssistantAI',
        page_icon='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/ChatGPT-Logo.svg/512px-ChatGPT-Logo.svg.png?20240214002031',
        layout='wide',
        initial_sidebar_state='expanded'
        )

    st.title('AssistantAI')
    st.subheader('Como posso ajudar?')
    
    user_question = st.chat_input('Escreva sua pergunta...')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'conversation_chain' not in st.session_state:
        st.session_state.conversation_chain = None

    if 'conversation_without_pdf' not in st.session_state:
        st.session_state.conversation_without_pdf = None    

    if 'mode' not in st.session_state:
        st.session_state.mode = None

    if 'pdf_docs' not in st.session_state:
        st.session_state.pdf_docs = []

    if 'youtube_link' not in st.session_state:
        st.session_state.youtube_link = None

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

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

        st.markdown('---')

        st.subheader('Qual tarefa você deseja que o AssistantAI faça?')
        button_pdf = st.button('Tirar dúvidas sobre seus PDFs')
        button_youtube = st.button('Tirar dúvidas sobre vídeos do YouTube')
        button_conversation_without_pdf = st.button('Conversa livre')

        st.markdown('---')

        if (button_pdf):
            st.session_state.mode = 'pdf'

        elif (button_youtube):
            st.session_state.mode = 'yt'

        elif (button_conversation_without_pdf):
            st.session_state.mode = 'free'


        if st.session_state.mode=='pdf':
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
                        st.session_state.pdf_docs = pdf_docs
                        st.info('Arquivos enviados!')
                        all_files_text = text.process_files(st.session_state.pdf_docs)

                        st.info('Aguarde mais um pouco, estamos processando os arquivos...')
                        chunks = text.create_text_chunks(all_files_text)
                        vectorstore = process_embeddings.create_vectorstore(chunks)
                        st.session_state.conversation_chain = chatbot.create_conversation_chain(vectorstore, st.session_state.api_key)

                        st.success('Arquivos processados com sucesso!')
                    else:
                        st.info('Nenhum arquivo carregado. Por favor, carregue um arquivo PDF para começar.')
            except Exception as e:
                st.warning(f'Erro ao carregar o arquivo: {e}')
            
        elif st.session_state.mode == 'yt':
            st.subheader('URL do vídeo do YouTube')
            url = st.text_input('Insira a URL do vídeo do Youtube', key='youtube_input_link', type='default')
            button_process_youtube = st.button('Enviar URL')

            try:
                if button_process_youtube:
                    if url:
                        st.session_state.youtube_link = url
                        st.info('URL enviado!')
                        transcription_video = youtube_transcription.transcript_video(st.session_state.youtube_link)
                        

                        st.info('Aguarde mais um pouco, estamos acessando o vídeo...')
                        chunks = text.create_text_chunks(transcription_video)
                        print('criou os chunks')

                        vectorstore = process_embeddings.create_vectorstore(chunks)
                        st.info('Analisando a transcrição do vídeo')
                      
                        st.session_state.conversation_chain = chatbot.create_conversation_chain(vectorstore, st.session_state.api_key)
                      
                        st.success('Vídeo analisado com sucesso!')
                    else:
                        st.info('Nenhuma URL foi digitada. Por favor, digite a URL do vídeo do YouTube desejado para começar.')
            except Exception as e:
                st.warning(f'Erro ao carregar a URL: {e}')
        
        elif st.session_state.mode == 'free':
            st.session_state.conversation_without_pdf = chatbot.create_conversation_without_pdf(st.session_state.api_key)

            st.subheader('Envie sua mensagem e converse com o Assistant!')
    
    if (user_question) and (st.session_state.mode=='pdf'):
        st.chat_message('user').markdown(user_question)
        st.session_state.messages.append({'role': 'user', 'content': user_question})
        with st.spinner("Analisando sua pergunta..."):
            try:
                response = st.session_state.conversation_chain(user_question)

            
                st.chat_message('assistant').markdown(response['answer'])
                st.session_state.messages.append({'role': 'assistant', 'content': response['answer']})
            except Exception as e:
                st.error(f'Erro: {e}')


    elif (user_question) and (st.session_state.mode=='yt'):
        st.chat_message('user').markdown(user_question)
        st.session_state.messages.append({'role': 'user', 'content': user_question})
        with st.spinner("Analisando sua pergunta..."):
            try:
                response = st.session_state.conversation_chain(user_question)

            
                st.chat_message('assistant').markdown(response['answer'])
                st.session_state.messages.append({'role': 'assistant', 'content': response['answer']})
            except Exception as e:
                st.error(f'Erro: {e}')

    elif (user_question) and (st.session_state.mode=='free'):
        st.chat_message('user').markdown(user_question)
        st.session_state.messages.append({'role': 'user', 'content': user_question})
        with st.spinner("Analisando sua pergunta..."):
            try:
                conversation_with_no_pdf = st.session_state.conversation_without_pdf(user_question)
                st.chat_message('assistant').markdown(conversation_with_no_pdf['response'])
                st.session_state.messages.append({'role': 'assistant', 'content': conversation_with_no_pdf['response']})

            except Exception as e:
                st.error(f'Erro: {e}')

if __name__ == "__main__":

    main()