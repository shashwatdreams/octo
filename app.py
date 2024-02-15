from openai import OpenAI
import streamlit as st
import hmac

#about

st.set_page_config(
    menu_items={
        'About': "The world is yours\nhttps://www.github.com/shashwatdreams/octo"
    }
)

# Function to check password
def check_password():
    def password_entered():
        # Compare the entered password with the stored password securely
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # Check if the password is already verified
    if st.session_state.get("password_correct", False):
        return True
    
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False



if not check_password():
    st.stop()

# Define the model mapping
model_mapping = {
    "GPT-3.5-Turbo": "gpt-3.5-turbo-0125",
    "GPT-4": "gpt-4"
}

st.markdown("""
    <style>
    .block-container{padding-top:2rem!important;}
    </style>
""", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([3, 1])
with col1:
    st.title("octo")
with col2:
    # Use the model_mapping keys for the selectbox display options
    model_selection = st.selectbox("", list(model_mapping.keys()), key="openai_model")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat messages in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new messages
if prompt := st.chat_input("Message Octo..."):
    # Append the new user message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Handle the assistant response
    with st.chat_message("assistant"):
        # Use the model_mapping to get the specific model identifier
        selected_model = model_mapping[model_selection]
        stream = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    # Append the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": response})

# Hide Streamlit's default UI elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
