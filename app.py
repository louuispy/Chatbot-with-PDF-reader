import streamlit as st

def main():

    st.set_page_config(page_title='AssistantAI', page_icon='📚')
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