# from dotenv import load_dotenv, find_dotenv
# import streamlit as st
# import pandas as pd
# import os
# from pandasai import SmartDatalake
# from pandasai.llm.openai import OpenAI
# from pandasai.prompts import CorrectErrorPrompt, GeneratePythonCodePrompt

# import matplotlib

# matplotlib.use("TkAgg") # tkinter library

# load_dotenv(find_dotenv())


# llm = OpenAI(model_name="gpt-4", temperature=0)


# # set a title of chatbot
# st.title("Prompt-driven analysis with PandasAI")

# # Create a widget of file uploader
# uploaded_files = st.file_uploader(
#     "Upload a CSV file for analysis", accept_multiple_files=True, type=["csv"]
# )
# print(uploaded_files)

# if uploaded_files:
#     # Load the data and perform preprocessing only if it hasn't been loaded before
#     # if "loaded_df" not in st.session_state:
#     #     print("-----------------------if---------------------------")

#     dfs = []
#     for uploaded_file in uploaded_files:
#         if uploaded_file.name in st.session_state:
#             print(
#                 f"{uploaded_file.name} is already uploaded and is present in session state"
#             )
#             df = st.session_state[uploaded_file.name]
#             dfs.append(df)
#             continue

#         print(f"{uploaded_file.name} is uploaded now so let's add it in session state")
#         path = os.path.join(os.getcwd(), uploaded_file.name)
#         print("Path: " + path)

#         # Save the uploaded file to disk
#         with open(path, "wb") as f:
#             f.write(uploaded_file.getvalue())

#         try:
#             df = pd.read_csv(path)
#             dfs.append(df)
#         except PermissionError as error:
#             st.write(
#                 f"The {uploaded_file.name} is open, first close it and then try to upload it."
#             )
#             st.stop()

#         st.session_state[uploaded_file.name] = df
#     # else:
#     #     print("-----------------------else---------------------------")
#     #     dfs = st.session_state["loaded_df"]

#     # # Create an agent
#     # smart_lake_config = {
#     #     "llm": llm,
#     #     "verbose": True,
#     #     "enable_cache": False,
#     #     "custom_prompts": {
#     #         "generate_python_code": GeneratePythonCodePrompt(),
#     #         "correct_error": CorrectErrorPrompt(),
#     #     },
#     #     "custom_whitelisted_dependencies": [
#     #         "pandas",
#     #         "numpy",
#     #         "matplotlib",
#     #         "streamlit",
#     #     ]
#     # }
#     # csv_agent = SmartDatalake(dfs=dfs, config=smart_lake_config)

#     csv_agent = SmartDatalake(dfs, config={"llm": llm, "verbose": True})

#     prompt = st.text_area("Enter your prompt")

#     if st.button("Generate"):
#         if prompt:
#             with st.spinner(
#                 "Generating a response...."
#             ):  # default text: "In progress..."
#                 st.write(csv_agent.chat(prompt))
#         else:
#             st.warning("Please enter a prompt")

# ____________________________________________________________________________________________________________


from dotenv import load_dotenv, find_dotenv
import streamlit as st
import pandas as pd
import os
import pandasai
from pandasai import SmartDatalake
from pandasai.llm.openai import OpenAI

import matplotlib

matplotlib.use("TkAgg")  # tkinter library

# load_dotenv(find_dotenv())

# set a title of chatbot
st.title("Prompt-driven analysis with PandasAI")

# File uploader in the sidebar on the left
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# Set OPENAI_API_KEY as an environment variable
os.environ["OPENAI_API_KEY"] = openai_api_key


llm = OpenAI(temperature=0, model_name="gpt-4")

with st.sidebar:
    # Create a widget of file uploader
    uploaded_files = st.file_uploader(
        "Upload the CSV files for analysis", accept_multiple_files=True, type=["csv"]
    )
    st.info(
        "Please refresh the browser if you decided to upload more files to reset the session",
        icon="🚨")
    print(uploaded_files)


if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        if uploaded_file.name in st.session_state:
            print(
                f"{uploaded_file.name} is already uploaded and is present in session state"
            )
            df = st.session_state[uploaded_file.name]
            dfs.append(df)
            continue

        print(f"{uploaded_file.name} is uploaded now so let's add it in session state")
        path = os.path.join(os.getcwd(), uploaded_file.name)
        print("Path: " + path)

        # Save the uploaded file to disk
        try:
            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())

            df = pd.read_csv(path)
            dfs.append(df)
        except PermissionError as error:
            st.error(
                f"The {uploaded_file.name} file is open, first close it and then try to upload it."
            )
            st.stop()

        st.session_state[uploaded_file.name] = df

    csv_agent = SmartDatalake(dfs, config={"llm": llm, "verbose": True})

    # Check whether there are any message in the streamlit session or not
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input(placeholder="Ask your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
        # In simple words, StreamlitCallbackHandler expands the thought and action took by LLM in
        # the expander
            try:
                with st.spinner("Generating a response...."):  # default text: "In progress..."
                    response = csv_agent.chat(prompt)
                    st.session_state.messages.append(
                        {"role": "assisstant", "content": response}
                    )

                    # Let's add a variable in session state
                    if type(response) == pandasai.smart_dataframe.SmartDataframe:
                        st.dataframe(response)
                    else:
                        st.write(response)
            except Exception as error:
                print("An error occurred:", error)
                st.session_state.messages.append(
                    {"role": "assisstant", "content": "Sorry, I don't know the answer"}
                )
                st.write("Sorry, I don't know the answer")
    else:
        st.warning("Please enter a prompt")

    # if st.button("Generate"):
    #     if prompt:
    #         with st.spinner(
    #             "Generating a response...."
    #         ):  # default text: "In progress..."
    #             st.write(csv_agent.chat(prompt))
    #     else:
    #         st.warning("Please enter a prompt")
