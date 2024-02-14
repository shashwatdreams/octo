import openai
import streamlit as st

# Set the OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

# Initialize session state for messages if it doesn't already exist
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    st.chat_message(role=msg["role"], body=msg["content"])

# Handle new user input
prompt = st.chat_input("Type your message:")
if prompt:
    # Add the user's message to the session state
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Prepare messages for the API request
    messages_formatted = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state["messages"]]

    # Use the Completion API to get a response
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=messages_formatted,
        temperature=0.7,
        max_tokens=150,
        n=1,
        stop=None,
        user="user-id-or-session-id"
    )

    # Extract and display the response
    if response and response.choices:
        answer = response.choices[0].text.strip()
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.chat_message(role="assistant", body=answer)