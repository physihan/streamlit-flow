# %%
import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
# Initialize OpenAI API key
template = """
    Going forward, I want you to act as a software architect and build C4 diagrams using mermaid.js. Keep the answers to markdown syntax and always keep in mind software functional and non-functional aspects including but not limited to scalability, availability, redundancy, containerization, security and disaster recovery.
    Below is the email, tone, and dialect:
    type: {graph_type}
    logic: {logic_input}
    response me in chinese
    YOUR {graph_type} RESPONSE :
"""

prompt = PromptTemplate(
    input_variables=["graph_type", "logic_input"],
    template=template,
)


def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("Globalize Text")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format. This tool \
                is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
                [@GregKamradt](https://twitter.com/GregKamradt). \n\n View Source Code on [Github](https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py)")

with col2:
    st.image(image='screenshot.png', width=500,
             caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## 请输入内容：")


def get_api_key():
    input_text = st.text_input(
        label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text


# openai_api_key = get_api_key()
openai_api_key = "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"

col1, col2 = st.columns(2)
graph_type=""
with col1:
    graph_type = st.selectbox(
        '你想要绘制什么样的图表',
        ('流程图', '柱状图'))

# with col2:
#     option_dialect = st.selectbox(
#         '你想要绘制什么样的图表',
#         ('流程图', '柱状图'))


def get_text():
    input_text = st.text_area(label="请输入你要绘制的图表逻辑",
                              placeholder="Your Email...", key="logic_input")
    return input_text


logic_input = get_text()

if len(logic_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()


def update_text_with_example():
    print("in updated")
    st.session_state.logic_input = "Sally I am starts work at yours monday from dave"


st.button("*See An Example*", type='secondary',
          help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")


def handle_submit():
    print("in handle submit")
    if not logic_input:
        st.warning(
            '请填写图标逻辑. ', icon="⚠️")
        return
    if logic_input:
        if not openai_api_key:
            print("in handle submit error")

            st.warning(
                'Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
            st.stop()

        llm = load_LLM(openai_api_key=openai_api_key)

        prompt_with_email = prompt.format(
            graph_type=graph_type, logic_input=logic_input)

        formatted_result = llm(prompt_with_email)
        # print(formatted_result)
        # st.write(formatted_result)
        # st.text(formatted_result)
        st.markdown(formatted_result)


# 增加一个按钮，点击后，将输入的内容，转换成对应的格式
st.button("Convert", type='primary',
          help="Click to convert your email.", on_click=handle_submit)


# %%
