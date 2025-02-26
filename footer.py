import streamlit as st
from htbuilder import div, p, styles

def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin="0px",
        width="100%",
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    body = p()
    foot = div(
        style=style_div
    )(
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        else:
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    with st.expander("ℹ️ more"):
        st.write("use gemini for basic tasks cz it's the cheapest 🙏 alhamdulillah")

    layout()

if __name__ == "__main__":
    footer()
