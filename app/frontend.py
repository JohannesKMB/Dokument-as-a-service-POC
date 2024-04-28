import streamlit as st
import requests
import json

st.title("Dokument-as-a-service")

st.text_input('Frage über das Dokument:', key='question')
question = st.session_state.question

uploaded_file = st.file_uploader("Choose a file")

url = 'http://127.0.0.1:8000/answer'
headers = {'Content-Type': 'application/json', 'accept': 'application/json'}

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue().decode('latin-1')

    data = {
        'question': question,
        'image': bytes_data
    }
    payload = json.dumps(data)
    resp = requests.post(url, data=payload, headers=headers)
    resp = resp.content
    resp = eval(resp.decode("utf-8"))['prediction']

    if st.button('Dokument befragen:'):
        resp
