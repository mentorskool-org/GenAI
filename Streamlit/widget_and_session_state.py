import streamlit as st

age = st.slider(':red[Select your age:]', min_value=12, max_value=100)

if 'age' not in st.session_state:
    st.session_state.age = None

'Before confirmation of age: ', st.session_state

button = st.button('Confirm the Age')
if button:
    'Your age is:', age
    st.session_state.age = age

    'After confirmation of age: ', st.session_state