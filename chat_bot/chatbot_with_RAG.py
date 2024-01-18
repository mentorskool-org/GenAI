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
from langchain.chains import LLMMathChain, LLMChain, RetrievalQA
from langchain.memory import ConversationBufferMemory

from langchain.memory.chat_message_histories import SQLChatMessageHistory
from langchain.schema.output_parser import OutputParserException

from sqlalchemy.engine import URL

# Libraries for embeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

load_dotenv(find_dotenv())

# gpt-3.5-turbo-16k -> provides more token (around 32,000 tokens)
# streaming - Some chat models provide a streaming response. This means that instead of waiting for
# the entire response to be returned, you can start processing it as soon as it's available
llm = ChatOpenAI(temperature=0, streaming=True, model="gpt-4", max_retries=3)
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


# Add the chain of fetching the information from the Enqurious_ETL_DB document

# # The steps is performed and embeddings are stored in vector store, so no need to perform this again
# Load the pdf
# loader = PyPDFLoader("Enqurious_ETL_DB document.pdf")

# # Now split the pdf into pages
# pages = loader.load_and_split()

# # Now split the documents via CharacterTextSplitter
# text_splitter = CharacterTextSplitter(
#     chunk_size=200,
#     chunk_overlap=20
# )

# docs = text_splitter.split_documents(pages)

# Now create an embedding object
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')

# # Create a deep lake object and fetch information from deep lake
my_activeloop_org_id = "burhanuddinnahargarwala"
my_activeloop_datset_name = "enqurious_practice"
dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_datset_name}"

vector_db = DeepLake(dataset_path=dataset_path, embedding=embeddings) # embedding is already stored in db

# Now add documents to the vector db
# db.add_documents(docs)

# Now fetch the retriever from the db
retriever = vector_db.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# response = qa_chain.run("List down all the table of enqurious etl db in list format.")

#####
tools = [
    # Tool.from_function(
    #     name="Search",
    #     func=search.run,
    #     description="useful for when you need to answer questions about current events",
    # ),
    # Tool.from_function(
    #     name="Calculator",
    #     func=llm_math_chain.run,
    #     description="useful for when you need to answer questions regarding calculations or maths",
    # ),
    Tool.from_function(
        name="Enqurious ETL Document",
        description="Contains the answers of queries regarding extraction, transformation and loading of data in enqurious. It also contains the schema of the fact tables",
        func=qa_chain.run,
    ),
    Tool.from_function(
        name="Local DB",
        func=db_chain.run,
        description="Useful when we need to answer the questions regarding learners, clients, progress, skills, scores, etc.",
    ),
]


# break prompt into a prefix and suffix the prefix is our instructions
prefix = """
You are a PotgrSQL expert. Given an input question, first create a syntactically correct PotgrSQL query without SQL markdown syntax to 
run in the database, then look at the results of the query and return the answer to the input question. Unless the user specifies in 
the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per PotgrSQL. 
You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. 
Wrap each column name in double quotes ("") to denote them as delimited identifiers. Pay attention to use only the column names 
you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in 
which table. Pay attention to use date('now') function to get the current date, if the question involves "today".
Insert the is_current=True condition in all sql queries. If users asks the question regarding scores, skills, etc, then refer the 
skills_fact table. If user aks questions regarding activity_status, total_inputs, completed_inputs, progress_in_percent,
duration, learner's status then refer the progress_fact table

skills_fact and progress_fact tables are not granular at single attribute, to merge the records of both attribute we need to use
participants_email along with activity_id


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
is the name of the project. In skills_fact for a single participant in single project there
are multiple scores divided at skills level. So first perform group by operation on project
name and find the sum on score attribute to get the total scores scored by learners in a particular project.
And then based on that project_name, filter the records.

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

User: Fetch the learners who got more than 80% in the SQL Assessment from the batch FRAC-IMG-09102023.
In the given question batch FRAC-IMG-09102023 is the substring of the description attribute in the orders_dimension table. Filter the 
records based on the batch name and then find the score

Run the give query in the database:
SELECT participant_email, SUM(score) AS total_scores,  
        SUM(total) as out_of_scores,  
        (SUM(score)/SUM(total))*100 as scores_in_percentage  
        FROM skills_fact sk
        join orders_dimension od 
        on sk.order_id =od.id
        and od.description like '%FRAC-IMG-09102023%'
        WHERE project_name = 'SQL Assessment' AND is_current = True  
        GROUP BY participant_email 
        HAVING (SUM(score)/SUM(total))*100 > 80;

Current conversation:

User: [input]

Agent:

Have a conversation with a human, answering the following
questions as best as you can based on the memory available and the context provided 
below. If the question cannot be answered using the information provided, answer with 
"I don't know".
""" 

# and the suffix our user input and output indicator
# The agent_scratchpad is where we add every thought or action the agent has already performed.
# All thoughts and actions (within the current agent executor chain) can then be accessed 
# by the next thought-action-observation loop, enabling continuity in agent actions.
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
    session_id="new-session", connection_string="sqlite:///sqlite.db"
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
    handle_parsing_errors=True,
)

# An Agent Executor is an Agent and set of Tools. The agent executor is responsible for 
# calling the agent, getting back and action and action input, calling the tool that the action 
# references with the corresponding input, getting the output of the tool, and then passing all that 
# information back into the Agent to get the next action it should take

# https://docs.langchain.com/docs/use-cases/personal-assistants
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
            # Handle the exception
            print("An error occurred:", error)
            agent_chain.early_stopping_method = 'force'
            st.session_state.messages.append(
                {"role": "assisstant", "content": "Sorry, I don't know the answer"}
            )
            st.write("Sorry, I don't know the answer")
        except Exception as error:
            print("An error occurred:", error)
            agent_chain.early_stopping_method = 'force'
            st.session_state.messages.append(
                {"role": "assisstant", "content": "Sorry, I don't know the answer"}
            )
            st.write("Sorry, I don't know the answer")
