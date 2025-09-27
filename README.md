# Assistant AI
## Envie seus PDFs e receba insights incríveis!

### Selecionar idioma:
- [English](https://github.com/louuispy/Chatbot-with-PDF-reader/blob/main/README-en.md)
- [Português](https://github.com/louuispy/Chatbot-with-PDF-reader/blob/main/README.md)

---

<img width="1897" height="941" alt="image" src="https://github.com/user-attachments/assets/b5eb5530-50a7-41db-bc50-b398f708dcaa" />

### O que é o AssistantAI?
O AssistantAI consiste em um projeto desenvolvido por mim, **100% em Python**, para aprofundar meus estudos em IA e colocar em prática meus conhecimentos de Python, Streamlit e Langchain.

A proposta principal do chatbot é responder perguntas do usuário, fornecendo insights interessantes e precisos, com base em arquivos PDF enviados pelo próprio usuário para a IA, no entanto, você pode também utilizá-lo para responder perguntas mais livres, sem necessidade do envio de PDFs.

>[!NOTE]
> **ATUALIZAÇÃO:** Agora você pode conversar com vídeos do YouTube! Envie a URL e tire suas dúvidas sobre o vídeo enviado.

### Tecnologias utilizadas:
- Streamlit
- Langchain
- Groq API (openai/gpt-oss-20b)
- HuggingFace Instruct Embeddings
- FAISS
- PdfReader
- YouTubeTranscriptApi

### Como utilizar?
  1. Faça um clone desse repositório git para a sua máquina
    ```
    https://github.com/louuispy/Chatbot-with-PDF-reader.git
    ```
  
  2. Crie um ambiente virtual com Python e ative-o
      
     ```
     python -m venv venv
     venv\Scripts\activate 
     ```
     
     No caso de Linux ou MacOS, ative o venv assim:
     
     ```
     source venv/bin/activate
     ```
   3. Instale as bibliotecas presentes no `requirements.txt` utilizando o `pip install`
      
      ```
      pip install -r requirements.txt
      ```
   4. Configure as variáveis de ambiente, adicionando um `.env` na raiz do projeto, junto à sua API do Groq Llama3.
   5. Execute o app com
      ```
      streamlit run .\app.py
      ```
---
### Case de uso do AssistantAI
Um case que você pode fazer, após realizar as etapas anteriores, consiste em:
1. Acesse a *sidebar* e envie um PDF de currículo, ou até mesmo apostila de algum concurso que esteja fazendo;
2. Após o envio, clique em Processar PDFs, para que o(s) arquivo(s) seja(m) processado(s) pela IA;
3. Se tudo ocorreu certo, você receberá uma mensagem indicando que os arquivos foram processados com sucesso.
4. Após isso, faça qualquer pergunta relacionada ao(s) PDF(s) para a IA, e ela responderá, trazendo os insights necessários e de forma precisa.

> [!NOTE] 
> Alguns arquivos PDF podem não ser processados corretamente, isso pode acontecer por diversos motivos, um deles é por conta do modelo não conseguir extrair os textos dos arquivos PDFs.
> Esse ponto será corrigido em futuras atualizações do projeto.

---

### Como o projeto foi desenvolvido?
O desenvolvimento do chatbot foi dividido em 5 grandes etapas:
  1. Desenvolver a interface da aplicação;
  2. Desenvolver um sistema de leitura de PDFs, extração das informações e criação de chunks;
  3. Desenvolver um sistema de vectorstore, para processar os chunks, convertê-los em embeddings e depois armazenmá-los
  4. Desenvolver o sistema de chatbot usando uma API do modelo de linguagem `openai/gpt-oss-20b`, por meio do Groq, passando para o chatbot a vectorstore.
  5. Desenvolver uma chain livre, para que o usuário possa conversar sem necessidade de enviar PDFs.

---

### 1. Desenvolvendo a interface
Para desenvolver a interface, utilizei `Streamlit`.
Optei por criar uma interface relativamente simples, apenas com o *promp*, para o usuário mandar as mensagens, e uma *sidebar*, para o envio e processamento de PDFs.
Após o envio de uma mensagem, serão exibidos na tela as mensagens do user, e logo em seguida da IA.

<img width="1474" height="853" alt="image" src="https://github.com/user-attachments/assets/c066b09c-78fe-46b1-998c-a963427aa599" />

Para que a interface exibisse uma mensagem após a outra, em formato de chat, utilizei o `st.session_state`, do `Streamlit`.
```python
if 'messages' not in st.session_state:
        st.session_state.messages = []
for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])
```
Basicamente, se não houver nenhuma mensagem no `session_state`, ele cria uma lista vazia e, com base o usuário vai enviando prompts e a IA respondendo, as mensagens são armazenadas nesta mesma lista vazia criada.

A partir do momento que uma nova mensagem é salva na lista `st.session_state.messages`, ela é exibida na tela, respeitando o *role*, ou seja, quem enviou a mensagem, e o *context*, que consiste no prompt do usuário e na resposta gerada pela IA.

Outro ponto extremamente importante da interface é a sua sidebar, onde basicamente você vai colocar sua API do Groq e então escolher a função que o chatbot irá exercer na conversação.

<img width="333" height="517" alt="image" src="https://github.com/user-attachments/assets/1d62a061-5be8-4d16-ae36-795b6bbe3e15" />

```python
with st.sidebar:
        st.subheader('Insira sua chave de API Groq')
        input_api_key = st.text_input('Insira sua chave de API Groq', key='groq_api_key', type='password')
        button_process_api = st.button('Enviar chave de API')

        st.markdown('---')

        try:
            if button_process_api:
                if input_api_key:
                    st.info('Chave de API enviada!')
                    st.session_state.api_key = input_api_key
                else:
                    st.warning('Nenhuma chave de API inserida! Por favor, insira uma chave de API.')

        except Exception as e:
            st.warning(f'Erro ao enviar a chave de API {e}')


        st.subheader('Qual tarefa você deseja que o AssistantAI faça?')
        button_pdf = st.button('Tirar dúvidas de PDFs')
        button_conversation_without_pdf = st.button('Conversa livre')

```


---

### 2. Desenvolvendo o leitor de PDFs
Para o sistema de leitura de PDFs e criação de chunks, usei o `PdfReader`, e dividi essa etapa em duas pequenas tarefas. A primeira seria desenvolver uma função para a leitura dos PDFs e, a segunda, seria uma função para criar/dividir os textos do PDF em chunks.

#### 2.1 - Leitura dos PDFs
```python
def process_files(files):
    text = ""

    for file in files:
        pdf = PdfReader(file)

        for page in pdf.pages:
            text += page.extract_text()

    return text
```

#### 2.2 - Crianção de chunks (com CharacterTextSplitter)
```python
def create_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    return chunks
```
---

### 3. Desenvolvendo a vectorstore
Agora que temos os chunks, precisamos passar eles para uma função que faça o seu processamento para embeddings e armazene eles em uma vectorstore. Essa vectorstore pode ser tanto local quanto em memória. No caso, optei por fazer em memória.
Para essa etapa, foi utilizado o `HuggingFaceInstructEmbeddings` para "criar" os embeddings baseando-se em um modelo da comunidade do HuggingFace, e o `FAISS` para a criação em si da vectorstore.
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings

def create_vectorstore(chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name='intfloat/multilingual-e5-base')
    vectorstore = FAISS.from_texts(texts = chunks, embedding=embeddings)

    return vectorstore
```

---

### 4. Desenvolvendo uma conversation chain para o modelo de LLM conversar com os PDFs
Nessa altura do campeonato, já temos uma função para ler os PDFs, criar os chunks e processar os chunks em embeddings. Agora, só precisamos passar esses embeddings para o modelo de LLM ler e responder o usuário.

Para isso, vamos usar o Groq, visto que não possui custos e também possui ótimos modelos de LLM, a exemplo do modelo utilizado no projeto.

```python
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

```

Uma funcionalidade interessante implementada na function de conversação foi o `ConversationBufferMemory`, que permite que o modelo tenha uma memória de conversa. Ou seja, ela consegue responder várias mensagens no prompt com memória das mensagens anteriores.

```python
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
```

---

### 5. Criação da chain de conversação livre
Agora que já temos basicamente toda a estrutura pronta do chatbot, basta nós usarmos a função anterior como base para a criação da nova função de conversa livre, sem passar a vectorstore para o modelo.

Nesse caso, optei por adicionar um template para essa chain específica.

```python
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
```

Após essas etapas, fazemos as devidas implementações na interface da aplicação, onde são inseridos o processamento dos PDFs e a conversação com a LLM. Nessa etapa, utiliza-se bastante o estado de sessão do Streamlit, visto que há muitas etapas que são ativadas com clicks nos botões. Por exemplo:

```python
if (button_pdf):
            st.session_state.mode = 'pdf'

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
                st.warning(f'Erro ao carregar o arquivo {e}')
```

Esse trecho específico do código ocorre caso o usuário aperte no botão de conversa com envio de PDFs.
Como o Streamlit funciona como reloads da página ao clicar em botões, e o estado de click do botão é verdadeiro apenas no momento do click, e após o reload fica falso, é necessárioc criar um estado de sessão que armazene uma informação que o botão foi apertado ou não. Com isso, podemos usar essa informação de estado de sessão como condicional para executar o restante do script.

---

### 👨🏻‍💻 Autor
Luís Henrique

Data Scientist | UX/UI Designer 

[Conecte-se comigo no LinkedIn](https://www.linkedin.com/in/luishenrique-ia/)
