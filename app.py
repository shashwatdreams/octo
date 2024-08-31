from openai import OpenAI
import streamlit as st
import hmac
import google.generativeai as gen_ai
import anthropic

st.set_page_config(
    page_title="Octo Engine",
    menu_items={
        'About': "The world is yours"
    }
)

def check_password():
    def password_entered():
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True
    
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()

model_mapping = {
    "GPT-3.5": "gpt-3.5-turbo",
    "Google Gemini": "google-gemini",
}

st.markdown("""
    <style>
    .block-container{padding-top:2rem!important;}
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.title("Octo")
with col2:
    model_selection = st.selectbox("", list(model_mapping.keys()), key="openai_model")

# Initialize clients based on model selection
if model_selection == "GPT-3.5":
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    client = openai
elif model_selection == "Google Gemini":
    gen_ai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = gen_ai.GenerativeModel('gemini-pro')
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if model_selection == "GPT-3.5":
        with st.chat_message("assistant"):
            stream = client.ChatCompletion.create(
                model=model_mapping[model_selection],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    elif model_selection == "Google Gemini":
        with st.chat_message("assistant"):
            gemini_response = st.session_state.chat_session.send_message(prompt)
            st.markdown(gemini_response.text)
            st.session_state.messages.append({"role": "assistant", "content": gemini_response.text})

# Hide Streamlit's default elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)