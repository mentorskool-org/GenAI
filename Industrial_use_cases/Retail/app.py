from retail import get_few_shot_chain

import streamlit as st

st.title("Retail Data Analysis Chatbot!")

question = st.text_input("Enter your query: ")

if question:
    chain = get_few_shot_chain()
    response = chain.run(question)

    st.header("Answer: ")
    st.write(response)