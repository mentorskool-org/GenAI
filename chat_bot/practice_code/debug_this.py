from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
from langchain.llms import OpenAIChat
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType, Tool, create_sql_agent
from langchain.tools import DuckDuckGoSearchRun, Tool, BaseTool, tool # Before import download it pip install duckduckgo-search
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from langchain.utilities import SQLDatabase, DuckDuckGoSearchAPIWrapper
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import LLMMathChain
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from sqlalchemy.engine import URL

load_dotenv(find_dotenv())

llm = ChatOpenAI(temperature=0, streaming=True, model='gpt-3.5-turbo-16k')
search = DuckDuckGoSearchAPIWrapper()
llm_math_chain = LLMMathChain.from_llm(llm)

# Create connection string
connectionURL = URL.create(
    'postgresql+psycopg2',
    host=os.environ.get('HOST'),
    database='enqurious_etl_db',
    username=os.environ.get('USER'),
    port=5432,
    password=os.environ.get('PASSWORD')
)

db = SQLDatabase.from_uri(connectionURL)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

tools = [
    Tool.from_function(
         name='Search',
         func=search.run,
         description='useful for when you need to answer questions about current events'
     ), 
    Tool.from_function(
         name='Calculator',
         func=llm_math_chain.run,
         description=''
     ), 
     Tool.from_function(
         name='Local DB',
         func=db_chain.run,
         description='Useful when we need to answer the questions about users.'
     )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True, # https://python.langchain.com/docs/modules/agents/how_to/handle_parsing_errors
)

# https://medium.com/dataherald/how-to-connect-llm-to-sql-database-with-langchain-sqlagent-48635fddaa74
# toolkit = SQLDatabaseToolkit(llm=llm, db=db)

# agent = create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
# )

# set title of streamlit app
st.set_page_config(page_title="LangChain Chatbot", page_icon="🦜")
st.title("Enqurious - LangChain Chatbot")


# Check whether there are any message in the streamlit session or not
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome to Enqurious 🙋‍♂️. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# ## https://docs.streamlit.io/library/api-reference/chat/st.chat_message 
if prompt := st.chat_input(placeholder="Ask your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # In simple words, StreamlitCallbackHandler expands the thought and action took by LLM in the expander
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.session_state.messages.append({"role": "assisstant", "content": response})
        st.write(response)

