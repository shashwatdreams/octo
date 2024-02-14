import openai
import streamlit as st

# Assuming OPENAI_API_KEY is correctly set in your Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "How can I help you?"}]

# Display past messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message(msg["content"], is_user=True)
    else:
        st.chat_message(msg["content"])

# Input from user
prompt = st.chat_input("You", key="chat_input")
if prompt:
    # Add the user's message to the session state
    st.session_state["messages"].append({"role": "user", "content": prompt})

    try:
        # Using the OpenAI Chat API to get a response from the chat model
        chat_completion = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"]
        )
        
        # Extract the message content from the response
        msg = chat_completion.choices[0].message["content"]
        
        # Append the assistant's response to the session state and display it
        st.session_state["messages"].append({"role": "system", "content": msg})
        st.chat_message(msg)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
