# Assistant AI  
## Upload your PDFs and receive amazing insights!

### Select language:
- [English]()
- [Português](https://github.com/louuispy/Chatbot-with-PDF-reader/blob/main/README.md)

---

### What is AssistantAI?
AssistantAI is a project I developed, **100% in Python**, to deepen my studies in AI and put into practice my knowledge of Python, Streamlit, and Langchain.

The chatbot's goal is to answer user questions by providing accurate and insightful responses based on PDF files uploaded by the user.

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

4. Set up environment variables by creating a `.env` file in the root directory, including your Groq Llama3 API key.

5. Run the app with:

   ```bash
   streamlit run .\app.py
   ```

---

### How was the project developed?
The chatbot development was divided into three main stages:
1. Building the application interface  
2. Creating a RAG system with Langchain to process and chunk the uploaded PDFs  
3. Building the chatbot system using the Llama3 language model via Groq

---

### 1. Building the Interface
I used `Streamlit` to create the interface.  
The UI is intentionally simple, featuring a *prompt* area for user messages and a *sidebar* for uploading and processing PDFs.  
After sending a message, the user input and AI response are displayed in a chat-like format.

![image](https://github.com/user-attachments/assets/d7a61bca-70ea-466a-9b52-4f2d7fefa243)

To handle chat message flow, I used `st.session_state` from `Streamlit`:

```python
if 'messages' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])
```

This logic initializes an empty list of messages if it doesn't exist. As the user interacts with the bot, each message is added to this list and displayed accordingly, based on the *role* (who sent it) and the *content* (user prompt or AI response).

---

### 2. Building the RAG System
For the Retrieval-Augmented Generation (RAG), a temporary file is created for each uploaded PDF. This allows the file to be read and stored in a variable called `loaders`, initially an empty list.

Then, I implemented a function to create a `vectorstore` using `VectorstoreIndexCreator` and `HuggingFaceEmbeddings` from Langchain.

Chunks are generated from the PDF and used as context for the Llama3 language model.

---

### 3. Building the Chatbot Structure
Once the RAG system was ready, I built the conversation function. This function sets up a chain that allows the user to interact with the LLM using the extracted chunks as context.

I used `ChatGroq` from Langchain along with the *Llama3* model.

The conversation chain uses a template with:
- a *system* message: defining the assistant’s behavior and tone  
- a *user* message: containing the user’s question

I also implemented `ConversationBufferMemory`, enabling the bot to remember previous messages and maintain the conversation context.

After these steps, the final integrations were made into the interface, enabling PDF upload and LLM-powered chat.

---

### 👨🏻‍💻 Author  
**Luís Henrique**  
UX/UI Designer and Dev passionate about AI, Computer Vision, and User Experience.

[Connect with me on LinkedIn](https://www.linkedin.com/in/luishenrique-ia/)
