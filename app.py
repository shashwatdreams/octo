from openai import OpenAI
import streamlit as st
import hmac


def check_password():
    def password_entered():
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True
    
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

password_correct = check_password()
if password_correct:
    # HTML for the unlocking effect
    unlocking_animation_html = """
    <div style="text-align: center;">
        <div class="lock-animation" style="font-size: 48px; display: inline-block; animation: unlock 2s ease-in-out forwards;">
            🔒
        </div>
    </div>
    <style>
    @keyframes unlock {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(20deg); }
        100% { transform: rotate(-45deg); }
    }
    </style>
    """
    st.markdown(unlocking_animation_html, unsafe_allow_html=True)
    st.success("Unlocked Successfully. Welcome!")


if not check_password():
    st.stop()


st.title("octo")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

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
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})\
    

# design
    
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)