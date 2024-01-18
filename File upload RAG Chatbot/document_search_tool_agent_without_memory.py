# Properly check the version of openai, chromadb, etc

# Required packages
# 1. langchain
# 2. openai==0.27.8
# 3. chromadb
# 4. pip install unstructured
# 5. pip install "unstructured[pdf]"
# 6. pip install "unstructured[docx]"
# 7. pip install "unstructured[all-docs]" # Available document types: "csv", "doc", "docx", "epub",
# "image", "md", "msg", "odt", "org", "pdf", "ppt", "pptx", "rtf", "rst", "tsv", "xlsx"

import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.tools import Tool
from langchain.agents import AgentType, initialize_agent
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.memory import ConversationBufferMemory
# from langchain.tools import WikipediaQueryRun
# from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import AgentType
import os

# Chat UI title
# Chat UI title
st.header("Upload your own files and ask questions like ChatGPT")
# st.subheader("File type supported: PDF/DOCX/TXT :city_sunrise:")


# File uploader in the sidebar on the left
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()


# Set OPENAI_API_KEY as an environment variable
os.environ["OPENAI_API_KEY"] = openai_api_key


llm = ChatOpenAI(temperature=0, max_tokens=1000, model_name="gpt-4", streaming=True)

with st.sidebar:
    uploaded_files = st.file_uploader(
        "Please upload your files", accept_multiple_files=True, type=None
    )
    st.info(
        "Please refresh the browser if you decided to upload more files to reset the session",
        icon="🚨")


# search = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
search = DuckDuckGoSearchAPIWrapper()

if uploaded_files:
    # Print the number of files to console
    print(f"Number of files uploaded: {len(uploaded_files)}")

    # Load the data and perform preprocessing only if it hasn't been loaded before
    if "processed_data" not in st.session_state:
        # Load the data from uploaded PDF files
        documents = []
        for uploaded_file in uploaded_files:
            # Get the full file path of the uploaded file
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            file_name = file_path.split("\\")[-1].split(".")[0]
            print(file_name)

            # Save the uploaded file to disk
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Use UnstructuredFileLoader to load the PDF file
            loader = UnstructuredFileLoader(file_path)
            loaded_documents = loader.load()
            print(f"Number of files loaded: {len(loaded_documents)}")

            # Extend the main documents list with the loaded documents
            documents.extend(loaded_documents)

        # Chunk the data, create embeddings, and save in vectorstore
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        document_chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(document_chunks, embeddings)

        # Store the processed data in session state for reuse
        st.session_state.processed_data = {
            "document_chunks": document_chunks,
            "vectorstore": vectorstore,
        }

        # Print the number of total chunks to console
        print(f"Number of total chunks: {len(document_chunks)}")

    else:
        # If the processed data is already available, retrieve it from session state
        document_chunks = st.session_state.processed_data["document_chunks"]
        vectorstore = st.session_state.processed_data["vectorstore"]

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff"
    )

    tools = [
        Tool.from_function(
            name="Search",
            func=search.run,
            description="It is useful when you need to answer questions about current events, from the web",
        ),
        Tool(
            name="Documents",
            func=qa_chain.run,
            description="""Any queries related to the context of the document""",
        ),
    ]
else:
    tools = [
          Tool.from_function(
            name="Search",
            func=search.run,
            description="It is useful when you need to answer questions about current events, from the web",
        )
    ]

PREFIX = """Answer the following questions as best you can. If user mentions that answer the 
questions based on the document uploaded. In that case refer the Documents Tool and answer the user's
query. If user asks any real time questions or general question then refer the Search Tool, and in case 
of contextual queries refer the Documents Tool. If user asks the questions

User: Give me some idea on the context of the document uploaded

In this case refer the Documents tool and try to find out the context of the document.

You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""
SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}
AI:
"""

# No matter file uploads or not, the prompt should be there to answer the user queries
agent = initialize_agent(
    llm=llm,
    tools=tools,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
    agent_kwargs={
        "prefix": PREFIX,
        "format_instructions": FORMAT_INSTRUCTIONS,
        "suffix": SUFFIX,
    },
)

# Check whether there are any message in the streamlit session or not
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
if "messages" in st.session_state:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input(placeholder="Ask your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # In simple words, StreamlitCallbackHandler expands the thought and action took by LLM in
        # the expander
        try:
            response = agent.run(input=prompt, chat_history=st.session_state.messages)
            st.session_state.messages.append(
                {"role": "assisstant", "content": response}
            )
            st.write(response)
        except Exception as error:
            print("An error occurred:", error)
            st.session_state.messages.append(
                {"role": "assisstant", "content": "Sorry, I don't know the answer"}
            )
            st.write("Sorry, I don't know the answer")
