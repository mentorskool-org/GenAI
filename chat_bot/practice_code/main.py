from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.tools import DuckDuckGoSearchRun # Before import download it pip install duckduckgo-search
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st



load_dotenv(find_dotenv())

llm = OpenAI(temperature=0, streaming=True)
tools = load_tools(
    ['ddg-search', 'llm-math'], llm=llm
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# set title of streamlit app
st.set_page_config(page_title="LangChain Chatbot", page_icon="🦜")
st.title("Enqurious - LangChain Chatbot")


### Can set the website logo using the given code

# from PIL import Image
# # Loading Image using PIL
# im = Image.open('/content/App_Icon.png')
# # Adding Image to web app
# st.set_page_config(page_title="Surge Price Prediction App", page_icon = im)

# Check whether there are any message in the streamlit session or not
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome to Enqurious 🙋‍♂️. How can I help you?"}
    ]
print(st.session_state)

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

