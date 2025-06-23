# Assistant AI
## Envie seus PDFs e receba insights incríveis!

### Selecionar idioma:
- [English](https://github.com/louuispy/Chatbot-with-PDF-reader/blob/main/README-en.md)
- [Português](https://github.com/louuispy/Chatbot-with-PDF-reader/blob/main/README.md)

---

### O que é o AssistantAI?
O AssistantAI consiste em um projeto desenvolvido por mim, **100% em Python**, para aprofundar meus estudos em IA e colocar em prática meus conhecimentos de Python, Streamlit e Langchain.

A proposta do chatbot é responder perguntas do usuário, fornecendo insights interessantes e precisos, com base em arquivos PDF enviados pelo próprio usuário para a IA.

### Tecnologias utilizadas:
- Streamlit
- Langchain
- Groq API (Llama3)
- HuggingFace Transformers
- PyPDFLoader

### Como utilizar?
  1. Faça um clone desse repositório git para a sua máquina
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
> Alguns arquivos PDF podem não ser processados corretamente.
> Esse ponto será corrigido em futuras atualizações do projeto.

---

### Como o projeto foi desenvolvido?
O desenvolvimento do chatbot foi dividido em 3 etapas:
  1. Desenvolver a interface da aplicação.
  2. Desenvolver um sistema de RAG com langchain, para receber os PDFs, criar chunks a partir deles.
  3. Desenvolver o sistema de chatbot usando uma API do modelo de linguagem Llama3, por meio do Groq.

---

### 1. Desenvolvendo a interface
Para desenvolver a interface, utilizei `Streamlit`.
Optei por criar uma interface relativamente simples, apenas com o *promp*, para o usuário mandar as mensagens, e uma *sidebar*, para o envio e processamento de PDFs.
Após o envio de uma mensagem, serão exibidos na tela as mensagens do user, e logo em seguida da IA.

![image](https://github.com/user-attachments/assets/d7a61bca-70ea-466a-9b52-4f2d7fefa243)

Para que a interface exibisse uma mensagem após a outra, em formato de chat, utilizei o `st.session_state`, do `Streamlit`.
```python
if 'messages' not in st.session_state:
        st.session_state.messages = []
for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])
```
Basicamente, se não houver nenhuma mensagem no `session_state`, ele cria uma lista vazia e, com base o usuário vai enviando prompts e a IA respondendo, as mensagens são armazenadas nesta mesma lista vazia criada.

A partir do momento que uma nova mensagem é salva na lista `st.session_state.messages`, ela é exibida na tela, respeitando o *role*, ou seja, quem enviou a mensagem, e o *context*, que consiste no prompt do usuário e na resposta gerada pela IA.

---

### 2. Desenvolvendo o RAG
Para o RAG, criei um sistema onde é criado um arquivo temporário do PDF enviado pelo usuário pela interface em `Streamlit`, para assim, ter acesso ao arquivo e a partir disso, fazer a leitura do PDF e armazenar o conteúdo lido em uma variável `loaders`, que é uma lista vazia.
```python
def create_vectorstore(uploaded_files):
    loaders = []
    for pdf in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf.read())
            tmp_path = tmp.name
        loaders.append(PyPDFLoader(tmp_path))
```

Com isso, ainda nessa função `create_vectorstore` parti para a criação de uma function para criar um `vectorstore`, utilizando o `VectorstoreIndexCreator` e o `HuggingFaceEmbeddings`, ambos importados do `Langchain`.
A partir desse função, são criados os chunks do arquivo PDF passado pelo usuário. Esses chunks serão utilizados para "alimentar" o modelo de linguagem do Llama3.
```python
index=VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    ).from_loaders(loaders)

    return index.vectorstore
```
---

### 3. Criação da estrutura de chatbot
Com a etapa de RAG concluída, partimos então para a criação da function de conversação com o chatbot, onde criaremos uma chain que permitirá uma conversa do usuário com a LLM alimentada pelos chunks do PDF.
Para isso, utilizei o `ChatGroq`, ou apenas `Groq`, importado também do `Langchain`, e o modelo de linguagem *Llama3*.

O sistema em si da conversação foi simples, feito a partir de um template com *system* - onde passo informações de como o modelo deve responder, e baseado em que - e *user*, onde temos a *question* do usuário.
```python
system_template = '''Você é um assistente de inteligência artificial simpático e profissional chamado Assistant. Você responde em Português-BR.
Você sempre responde de forma clara, objetiva e precisa as dúvidas dos usuários. Você responde com base no contexto: {context}'''

prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", "{question}")
        ])
```

Uma funcionalidade interessante implementada na function de conversação foi o `ConversationBufferMemory`, que permite que o modelo tenha uma memória de conversa. Ou seja, ela consegue responder várias mensagens no prompt com memória das mensagens anteriores.
```python
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
```
Após essas etapas, foram feitas as devidas implementações na interface da aplicação, onde são inseridos o processamento dos PDFs e a conversação com a LLM.

---

### 👨🏻‍💻 Autor
Luís Henrique

UX/UI Designer e Dev apaixonado por IA, Visão Computacional e Experiência do Usuário.

[Conecte-se comigo no LinkedIn](https://www.linkedin.com/in/luishenrique-ia/)
