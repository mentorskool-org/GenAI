# # import streamlit as st


# # st.set_page_config(page_title='Langchain: Chat with SQL DB', page_icon="🦜")
# # st.title("🦜 LangChain: Chat with SQL DB")

# from langchain.chat_models import ChatOpenAI
# from dotenv import load_dotenv, find_dotenv
# import os

# from sqlalchemy.engine import URL
# from langchain.agents import create_sql_agent
# from langchain.utilities import SQLDatabase
# from langchain_experimental.sql import SQLDatabaseChain
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.agents.agent_types import AgentType
# from langchain.llms import OpenAI

# # Load the environment variables
# load_dotenv(find_dotenv())

# # Create llm object
# llm = OpenAI(temperature=0)

# # create database uri
# connectionURL = URL.create(
#     drivername="postgresql+psycopg2",
#     host=os.environ.get("HOST"),
#     database="enqurious_etl_db",
#     username=os.environ.get("USER"),
#     port=5432,
#     password=os.environ.get("PASSWORD"),
# )

# # Create sqldatabase object from URI
# db = SQLDatabase.from_uri(connectionURL)

# # print(f"All the available methods of SQL Database object: {db.__dir__()}")
# # print(f"Database contains the attribute _all_tables that gives all the available table in database\
# #       as shown: {db._all_tables}")

# # print(db.table_info)

# # The agent should contain the SQLDatabaseToolkit which contains tools to:
# # 1.Create and execute queries
# # 2.Check query syntax
# # 3.Retrieve table descriptions
# # 4. ... and more
# toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# # Use create_sql_agent
# agent_executor = create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     verbose=True,
#     handle_parsing_errors=True,
#     return_intermediate_steps=True,
# )

# print(agent_executor.run("How many tables are present in the database?"))


# Following are some of the attributes available in the agent_exceutor. here we can use memory, callbacks, etc
# ['memory', 'callbacks', 'callback_manager', 'verbose', 'tags', 'metadata', 'agent', 'tools',
# 'return_intermediate_steps', 'max_iterations', 'max_execution_time', 'early_stopping_method',
# 'handle_parsing_errors', 'trim_intermediate_steps']

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
        description="Useful when we need to answer the questions regarding learners, clients, progress, skills, scores, etc.",
    ),
]

# The agent_scratchpad is where we add every thought or action the agent has already performed.
# All thoughts and actions (within the current agent executor chain) can then be accessed
# by the next thought-action-observation loop, enabling continuity in agent actions.
prefix = """You are a PotgrSQL expert. Given an input question, first create a syntactically correct PotgrSQL query to 
run, then look at the results of the query and return the answer to the input question. Unless the user specifies in 
the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per PotgrSQL. 
You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. 
Wrap each column name in double quotes ("") to denote them as delimited identifiers. Pay attention to use only the column names 
you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in 
which table. Pay attention to use date('now') function to get the current date, if the question involves "today".
Insert the is_current=True condition in all sql queries. If users asks the question regarding scores, skills, etc, then refer the 
skills_fact table. If user aks questions regarding activity_status, total_inputs, completed_inputs, progress_in_percent,
duration, learner's status then refer the progress_fact table


Example conversation:

User: Hey can you help me with something

Agent: Sure! What do you need help with?

User: I want you to perform queries on database when user ask questions. Also keep in mind that if a 
table contains is_current attribute then select only those records where is_current is True

Agent: Sure! Have noted your point.

User: When user ask the question related to the scores of learners, then refer the skills_fact table and find the 
total scores of a particular learners from the score attribute by performing group by on participant_email atribute.

Agent: Okay Got that.

User: When user ask the question related to the progress of learners, then refer the progress_in_percent_by_activity
and filter the records based on that learner giving his progress in all the project. And in case, if progress is asked for a
specific project then refer the project_name attribute of progress_fact table and give the progress of a specific project.

Agent: Sure!

User: When user ask the question related to the learner's status, then refer the learner_status_by_order attribute of progress_fact
and filter the records based on that learner giving his status in all projects. And in case, if status is asked for a
specific project then refer the project_name attribute of progress_fact table and give the status of a specific project.

Agent: Sure!

User: Filter the top 5 participants based on their total scores in the Excel Assessment. In the given question, the excel assessment 
is the name of the project. So refer the project_name and filter the records based on that.

Agent: Sure!

User: When user asks to find the scores in percentage then refer the skills_fact table then find the 
total scores of a particular learners from the score attribute by performing group by on participant_email atribute
and find the out of scores from the total attribute by performing group by on participant_email atribute. And then calculate
the percentage based on total scores/out of scores.

Run the give query in the database:
SELECT participant_email, SUM(score) AS total_scores,
        sum(total) as out_of_scores,
        (sum(score)/sum(total))*100 as scores_in_percentage
        FROM skills_fact
        WHERE project_name = 'Excel Assessment' AND is_current = True
        GROUP BY participant_email
        ORDER BY total_scores DESC
        LIMIT 5;


Agent: Sure!


User: Filter the top 5 participants based on their scores in percentage in the Data Quality Assessment for the batch TRED-DE-07092023.
In the given question batch TRED-DE-07092023 is the substring of the description attribute in the orders_dimension table. Filter the 
records based on the batch name and then find the score

Run the give query in the database:
SELECT participant_email, SUM(score) AS total_scores,
        sum(total) as out_of_scores,
        (sum(score)/sum(total))*100 as scores_in_percentage
        FROM skills_fact sk
        join orders_dimension od 
        on sk.order_id =od.id
        WHERE sk.project_name = 'Excel Assessment' AND sk.is_current = true
        and od.description like '%TRED-DE-07092023%'
        GROUP BY participant_email
        ORDER BY total_scores DESC
        LIMIT 5;

        
Have a conversation with a human, answering the following
questions as best as you can based on the memory available and the context provided 
below. If the question cannot be answered using the information provided, answer with 
"I don't know".
"""
suffix = """Begin!"

Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "agent_scratchpad"],
)

# message_history = SQLChatMessageHistory(
#     session_id="my-session", connection_string="sqlite:///sqlite.db"
# )

# https://www.pinecone.io/learn/series/langchain/langchain-agents/
# memory = ConversationBufferMemory(
#     memory_key="chat_history", chat_memory=message_history
# )

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
    agent=agent, tools=tools, verbose=True #, memory=memory
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
