from openai import OpenAI
import streamlit as st
import hmac

st.set_page_config(
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

st.markdown("""
    <a href="https://github.com/shashwatdreams/octo" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" style="float:right; max-height: 32px; margin: 10px">
    </a>
""", unsafe_allow_html=True)

model_mapping = {
    "GPT-3.5-Turbo": "gpt-3.5-turbo-0125",
    "GPT-4": "gpt-4"
}


# fix spacing
st.markdown("""
    <style>
    .block-container{padding-top:2rem!important;}
    </style>
""", unsafe_allow_html=True)


col1, col2 = st.columns([3, 1])
with col1:
    st.title("octo")
with col2:
    model_selection = st.selectbox("", list(model_mapping.keys()), key="openai_model")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Message Octo..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        selected_model = model_mapping[model_selection]
        stream = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
