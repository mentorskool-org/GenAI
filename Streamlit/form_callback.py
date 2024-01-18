import streamlit as st

def form_callback():
    st.write(st.session_state.my_slider)
    st.write(st.session_state.my_checkbox)


with st.form(key='my-form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider') # 5 is the default value of slider
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    submit_button = st.form_submit_button(label='submit', on_click=form_callback)

st.session_state