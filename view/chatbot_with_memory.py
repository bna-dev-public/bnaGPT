from dataclasses import dataclass, field
import streamlit as st
from utils.loaders import load_image
from controller.chatbot_with_memory import (
    ChatBotWithMemoryEngine,
    list_conversations,
    save_conversation,
    load_conversation,
    delete_conversation,
)
from models.messages import StreamingMessage, Message
from llama_index.core.base.llms.types import MessageRole

chatbot = ChatBotWithMemoryEngine()


# This class represents a simple chatbot in Python.
@dataclass(slots=True)
class ChatbotWithMemoryView:

    # default values for the page
    page_title: str = field(default="bnaGPT")
    page_icon: str = field(default=":desktop_computer:")
    logo_filename: str = field(default="static/images/logo.png")
    header_string: str = field(
        default="bnaGPT - Chatbot with memory and saved conversation"
    )

    # build the page configuration
    def build_config(self):
        st.set_page_config(
            page_title=self.page_title,
            page_icon=self.page_icon,
        )

    # build the page body
    def build_body(self):
        # build the header
        st.subheader(self.header_string)
        # build the chat input
        chat_input = st.chat_input("What is up?")
        return chat_input

    # build the page sidebar
    def build_sidebar(self):
        with st.sidebar:
            image = load_image(self.logo_filename)
            st.logo(image)
            st.markdown("#### Click here to save current conversation!")
            if st.button("Save", use_container_width=True, type="primary"):
                st.session_state.show_confirm_save = True
            if st.session_state.show_confirm_save:
                save_convo_name = st.text_input(
                    "Enter a name to save the conversation:"
                )
                if st.button("Confirm Save") and save_convo_name:
                    conversation_names = save_conversation(
                        save_convo_name, st.session_state.messages
                    )
                    st.session_state.show_confirm_save = False
                    st.session_state.saved_conversations = list(conversation_names)
                    st.success(f"Conversation '{save_convo_name}' saved!")
            st.markdown("#")
            st.markdown("Saved Conversations")

            # printing every saved conversation
            for convo_name in st.session_state.saved_conversations:
                with st.popover(
                    convo_name,
                    use_container_width=True,
                ):
                    load_col, delete_col = st.columns([1, 1])
                    with load_col:
                        if st.button(
                            "Load",
                            key=f"load_{convo_name}",
                            use_container_width=True,
                            type="primary",
                        ):
                            messages, status = load_conversation(convo_name)
                            if status == "success":
                                st.session_state.messages = messages
                                # formatted_messages =
                                memory = chatbot.create_memory_from_historical_messages(
                                    st.session_state.messages
                                )
                                st.session_state.agent = chatbot.create_openAI_agent(
                                    memory=memory
                                )
                                st.experimental_rerun()
                            elif status == "wrong convo name":
                                st.error("This conversation could not be found")
                            else:
                                st.error("There is no historical conversations saved")
                    with delete_col:
                        if st.button(
                            "Delete",
                            key=f"delete_{convo_name}",
                            use_container_width=True,
                        ):
                            status, text = delete_conversation(convo_name)
                            if status == 200:
                                st.success(f"Conversation '{convo_name}' deleted!")
                                st.session_state.saved_conversations = (
                                    list_conversations()
                                )
                                st.experimental_rerun()
                            elif text == "no conversation found":
                                st.error(
                                    f"""No conversation found with the
                                    name '{convo_name}'"""
                                )
                            else:
                                st.error("No conversations file found")

    # Streamlit has a session element that you can create and save variables in it
    # So we need to update it once our main runs in a loop
    def initialize_session(self):

        # show_confirm_save = variable that will store whether the button of
        # confirm save should be seen
        if "show_confirm_save" not in st.session_state:
            st.session_state.show_confirm_save = False

        # saved_conversations = variable to store all conversations
        if "saved_conversations" not in st.session_state:
            st.session_state.saved_conversations = list_conversations()

        # we can create a variable called messages
        # to save and output the messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # agent = variable to store openAIAgent
        if "agent" not in st.session_state:
            memory = chatbot.create_memory_from_historical_messages(
                st.session_state.messages
            )
            st.session_state.agent = chatbot.create_openAI_agent(memory=memory)

        # output messages where:
        # role = user or assistant
        # content = content of the message
        for message in st.session_state.messages:
            with st.chat_message(message.role.value):
                st.markdown(message.content)

    # get user input
    def handle_chat_input(self, chat_input):
        if prompt := chat_input:
            message = Message(MessageRole.USER, prompt)
            st.session_state.messages.append(message)

            # printing the user message
            with st.chat_message(MessageRole.USER):
                st.markdown(prompt)

            # now creating the assistant response
            with st.chat_message(MessageRole.ASSISTANT):
                # getting the streaming response from controller
                streaming_response = StreamingMessage(
                    st.session_state.agent.stream_chat(chat_input)
                )
                # printing response
                response = st.write_stream(streaming_response.stream_message())
            # saving response
            message = Message(MessageRole.ASSISTANT, str(response))
            st.session_state.messages.append(message)
