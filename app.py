import openai
import streamlit as st
import hmac
import google.generativeai as gen_ai

st.set_page_config(
    page_title="Octo Engine",
    menu_items={
        'About': "The world is yours"
    }
)

# Initialize clients
openai_client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    "GPT-4o": "gpt-4o-mini",
    "Google Gemini Flash 2.0": "google-gemini",
    "Deepseek-R1": "deepseek-chat"
}

st.markdown("""
    <style>
    .block-container{padding-top:2rem!important;}
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.title("octo")
with col2:
    model_selection = st.selectbox("", list(model_mapping.keys()), key="model_selection")

# model initialization
if model_selection == "GPT-4o":
    openai.api_key = st.secrets["OPENAI_API_KEY"]
elif model_selection == "Google Gemini Flash 2.0":
    gen_ai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = gen_ai.GenerativeModel('gemini-2.0-flash').start_chat(history=[])
elif model_selection == "Deepseek-R1":
    if "deepseek_client" not in st.session_state:
        st.session_state.deepseek_client = openai.OpenAI(
            api_key=st.secrets["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model_mapping["GPT-4o"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("enter message...", key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if model_selection == "GPT-4o":
        with st.chat_message("assistant"):
            response = ""
            try:
                stream = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response_container = st.empty()
                full_response = ""
                for chunk in stream:
                    content = chunk.choices[0].delta.content or ""
                    full_response += content
                    response_container.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {e}")
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    elif model_selection == "Google Gemini Flash 2.0":
        try:
            gemini_response = st.session_state.chat_session.send_message(prompt)
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
            st.session_state.messages.append({"role": "assistant", "content": gemini_response.text})
        except Exception as e:
            st.error(f"Error: {e}")
    
    elif model_selection == "Deepseek-R1":
        with st.chat_message("assistant"):
            response = ""
            try:
                stream = st.session_state.deepseek_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response_container = st.empty()
                full_response = ""
                for chunk in stream:
                    content = chunk.choices[0].delta.content or ""
                    full_response += content
                    response_container.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {e}")
        st.session_state.messages.append({"role": "assistant", "content": full_response})

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)