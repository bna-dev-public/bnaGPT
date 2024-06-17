from dataclasses import dataclass, field
import streamlit as st
from utils.loaders import load_image
from controller.simple_chatbot import SimpleChatEngine
from models.messages import StreamingMessage, Message
from llama_index.core.base.llms.types import MessageRole


chat_engine = SimpleChatEngine()


# This class represents a simple chatbot in Python.
@dataclass(slots=True)
class SimpleChatbotView:

    # default values for the page
    page_title: str = field(default="bnaGPT")
    page_icon: str = field(default=":desktop_computer:")
    logo_filename: str = field(default="static/images/logo.png")
    header_string: str = field(default="bnaGPT | Simple Chat")
    text_box_string: str = field(default="Talk to our agent and see how it works!")

    # build the page configuration
    def build_config(self):
        st.set_page_config(
            page_title=self.page_title,
            page_icon=self.page_icon,
        )

    # build the page body
    def build_body(self):
        # build the header
        st.header(self.header_string)
        # build the chat input
        chat_input = st.chat_input("What is up?")
        return chat_input

    # build the page sidebar
    def build_sidebar(self):
        with st.sidebar:
            image = load_image(self.logo_filename)
            st.logo(image)

    # Streamlit has a session element that you can create and save variables in it
    # So we need to update it once our main runs in a loop
    def initialize_session(self):

        # we can create a variable called messages
        # to save and output the messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # output messages where:
        # role = user or assistant
        # content = content of the message
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # get user input
    def handle_chat_input(self, chat_input):
        if prompt := chat_input:
            message = Message(MessageRole.USER, prompt)
            st.session_state.messages.append(message.create_message())

            # printing the user message
            with st.chat_message(MessageRole.USER):
                st.markdown(prompt)

            # now creating the assistant response
            with st.chat_message(MessageRole.ASSISTANT):
                # getting the streaming response from controller
                streaming_response = StreamingMessage(
                    chat_engine.get_simple_chat_response(prompt)
                )
                # printing response
                response = st.write_stream(streaming_response.stream_message())
            # saving response
            message = Message(MessageRole.ASSISTANT, str(response))
            st.session_state.messages.append(
                {"role": MessageRole.ASSISTANT, "content": response}
            )
