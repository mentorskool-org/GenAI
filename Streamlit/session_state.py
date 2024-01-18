import streamlit as st

st.set_page_config(page_title='Learning Streamlit!', initial_sidebar_state='expanded')
st.title('Learning Streamlit!')

'st.session_state object:', st.session_state

if 'a_counter' not in st.session_state:
    st.session_state['a_counter'] = 0

if 'boolean' not in st.session_state:
    st.session_state['boolean'] = False

st.write(st.session_state)

button = st.button("Update State")
"before pressing button", st.session_state

if button:
    st.session_state['a_counter'] += 1
    st.session_state['boolean'] = not st.session_state.boolean
    "after pressing button", st.session_state

clear_button = st.button("Clear the session state!")

if clear_button:
    for key in st.session_state.keys():
        del st.session_state[key]

st.session_state