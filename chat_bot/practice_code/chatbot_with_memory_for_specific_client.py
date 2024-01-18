from dotenv import load_dotenv, find_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain.tools import (
    Tool,
)  # Before import download it pip install duckduckgo-search
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from langchain.utilities import SQLDatabase, DuckDuckGoSearchAPIWrapper
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import LLMMathChain, LLMChain
from langchain.memory import ConversationBufferMemory

from langchain.memory.chat_message_histories import SQLChatMessageHistory
from langchain.schema.output_parser import OutputParserException

from sqlalchemy.engine import URL

load_dotenv(find_dotenv())

# gpt-3.5-turbo-16k -> provides more token (around 32,000 tokens)
# streaming - Some chat models provide a streaming response. This means that instead of waiting for
# the entire response to be returned, you can start processing it as soon as it's available
llm = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo-16k")
search = (
    DuckDuckGoSearchAPIWrapper()
)  # alternative search engine API i.e DuckDuckGoSearch
llm_math_chain = LLMMathChain.from_llm(llm)  # use for accessing the calculator

# Create connection string
connectionURL = URL.create(
    "postgresql+psycopg2",
    host=os.environ.get("HOST"),
    database="enqurious_etl_db",
    username=os.environ.get("USER"),
    port=5432,
    password=os.environ.get("PASSWORD"),
)

db = SQLDatabase.from_uri(connectionURL)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

tools = [
    Tool.from_function(
        name="Local DB",
        func=db_chain.run,
        description="Useful when we need to answer the questions about users.",
    ),
]

# The agent_scratchpad is where we add every thought or action the agent has already performed.
# All thoughts and actions (within the current agent executor chain) can then be accessed 
# by the next thought-action-observation loop, enabling continuity in agent actions.
prefix = """Have a conversation with a human, answering the following
questions as best as you can based on the context and memory available: """
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

message_history = SQLChatMessageHistory(
    session_id="my-session-2", connection_string="sqlite:///sqlite.db"
)

# https://www.pinecone.io/learn/series/langchain/langchain-agents/
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=message_history
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

# Zero-shot means the agent functions on the current action only — it has no memory.
# It uses the ReAct framework to decide which tool to use, based solely on the tool’s description.
# LLM could cycle through Reasoning and Action steps (ReAct)
agent = ZeroShotAgent(
    llm_chain=llm_chain,
    tools=tools,
    verbose=True,
)

# An Agent Executor is an Agent and set of Tools. The agent executor is responsible for 
# calling the agent, getting back and action and action input, calling the tool that the action 
# references with the corresponding input, getting the output of the tool, and then passing all that 
# information back into the Agent to get the next action it should take
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
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
        {
            "role": "assistant",
            "content": "Welcome to Enqurious 🙋‍♂️. How can I help you?",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ## https://docs.streamlit.io/library/api-reference/chat/st.chat_message
if prompt := st.chat_input(placeholder="Ask your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # In simple words, StreamlitCallbackHandler expands the thought and action took by LLM in the expander
        st_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent_chain.run(input=prompt, callbacks=[st_callback])
            st.session_state.messages.append(
                {"role": "assisstant", "content": response}
            )
            st.write(response)
        except OutputParserException as error:
            print("Error: ", error)
