import openai 
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # Add the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Directly use the openai module to get a response from the chat model
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    # Extract the message content from the response
    msg = response.choices[0].message["content"]

    # Append the assistant's response to the session state and display it
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)