# Assistant AI  
## Upload your PDFs and receive incredible insights!

### Select language:
- [English](https://github.com/louuispy/Chatbot-with-PDF-reader/blob/main/README-en.md)
- [Português](https://github.com/louuispy/Chatbot-with-PDF-reader/blob/main/README.md)

---

### What is AssistantAI?
AssistantAI is a project I developed, **100% in Python**, to deepen my AI studies and put into practice my knowledge of Python, Streamlit, and Langchain.

The chatbot is designed to answer user questions by providing interesting and accurate insights, based on PDF files uploaded by the user.

### Technologies used:
- Streamlit  
- Langchain  
- Groq API (Llama3)  
- HuggingFace Transformers  
- PyPDFLoader  

### How to use it?
1. Clone this repository to your local machine  
2. Create and activate a virtual environment with Python

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   For Linux or MacOS:

   ```bash
   source venv/bin/activate
   ```

3. Install the required libraries using `requirements.txt`

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file in the root of the project with your Groq Llama3 API key.
5. Run the app with:

   ```bash
   streamlit run .\app.py
   ```

---

### AssistantAI Use Case
Once you’ve completed the steps above, here’s a case to try:
1. Open the *sidebar* and upload a resume PDF or a study guide from an exam you're preparing for.  
2. Click "Process PDFs" to have the files parsed by the AI.  
3. If all goes well, a confirmation message will appear.  
4. Ask anything related to the PDFs and the AI will reply with the insights you need—concise and laser-sharp.

> [!NOTE]
> Some PDF files may not be processed correctly.  
> This will be improved in future updates.

---

### How was the project developed?
The chatbot development was divided into three stages:
1. Build the application interface  
2. Develop a RAG system using Langchain to receive PDFs and chunk them  
3. Create the chatbot system powered by the Llama3 language model via Groq

---

### 1. Building the interface
To build the interface, I used `Streamlit`.  
I kept it elegantly simple: a *prompt* for messages, and a *sidebar* for PDF upload and processing.  
Once a message is sent, the user's input and the AI’s response are displayed like a proper chat.

![image](https://github.com/user-attachments/assets/d7a61bca-70ea-466a-9b52-4f2d7fefa243)

To ensure messages appear sequentially in a chat format, I used `st.session_state`:

```python
if 'messages' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])
```

If no messages exist, it initializes an empty list. Then, as prompts and responses are exchanged, each is stored and displayed based on its *role* (who sent it) and *context* (prompt/response pair).

---

### 2. Developing the RAG
The RAG system starts by creating a temporary file for each uploaded PDF in `Streamlit`. These are read and stored in a `loaders` list:

```python
def create_vectorstore(uploaded_files):
    loaders = []
    for pdf in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf.read())
            tmp_path = tmp.name
        loaders.append(PyPDFLoader(tmp_path))
```

Still within `create_vectorstore`, we build the `vectorstore` using `VectorstoreIndexCreator` and `HuggingFaceEmbeddings`, both from Langchain:

```python
index = VectorstoreIndexCreator(
    embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
).from_loaders(loaders)

return index.vectorstore
```

These chunks are the tasty snacks the Llama3 model digests to provide contextual answers.

---

### 3. Building the chatbot structure
With the RAG phase complete, we create the chatbot conversation function—where the user talks with the LLM, fueled by the PDF chunks.

Using `ChatGroq` from Langchain and the *Llama3* model, I set up a simple yet elegant prompt template, composed of *system* (instructions for the model) and *user* (the question):

```python
system_template = '''You are a friendly and professional AI assistant named Assistant. You answer in Brazilian Portuguese.
You always respond clearly, objectively, and accurately to users' questions. You answer based on the context: {context}'''

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{question}")
])
```

One nifty feature is the `ConversationBufferMemory`, allowing the assistant to *remember* the chat flow:

```python
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
```

Once these parts are done, they are integrated into the Streamlit interface—where PDF processing and chatting with the LLM unfold harmoniously.

---

### 👨🏻‍💻 Author
**Luís Henrique**  
UX/UI Designer and Dev passionate about AI, Computer Vision, and User Experience.

[Connect with me on LinkedIn](https://www.linkedin.com/in/luishenrique-ia/)
