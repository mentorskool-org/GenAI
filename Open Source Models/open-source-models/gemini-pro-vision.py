from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler

# from dotenv import load_dotenv
# import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage
from PIL import Image


st.set_page_config(page_title="LangChain Gemini Chatbot", page_icon="🦜")

st.title("Google Gemini Pro Max Model!!")


# File uploader in the sidebar on the left
with st.sidebar:
    api_key = st.text_input(f"Enter the Gemini Pro Vision API Key", type="password")
if not api_key:
    st.info(f"Please add your Gemini Pro Vision API key to continue.")
    st.stop()


# Create a llm model
llm = ChatGoogleGenerativeAI(
    # google_api_key=os.environ.get("PALM_API_KEY"),
    google_api_key=api_key,
    model="gemini-pro-vision",
)


content = []
prompt = st.text_input("Input", key="input")
# if prompt:
#     content.append({"type": "text", "text": prompt})

uploaded_file = st.file_uploader("Choose an image....", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption=prompt, use_column_width=True)


submit = st.button("Generate")

if submit:
    if prompt:
        content.append({"type": "text", "text": prompt})
    else:
        default_prompt = "Tell me something about the image"
        content.append({"type": "text", "text": default_prompt})

    content.append({"type": "image_url", "image_url": image})

    message = HumanMessage(content=content)
    response = llm.invoke([message])

    with st.chat_message("assistant"):
        print(response.content)
        st.write(response.content)

# if prompt := st.chat_input("Input", key="input"):
#     with st.chat_message("human"):
#         st.session_state.messages.append({"role": "human", "content": prompt})
#         st.write(prompt)

#     chain = ConversationChain(llm=llm, memory=st.session_state.memory, verbose=True)

#     with st.chat_message("assistant"):
#         response = chain.run(prompt)
#         # st_response = response.content
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.markdown(response)


### We can use the agent here  (Try the gemini-pro-vision once)
