import os
import json
from groq import Groq
import streamlit as st

# Groq configuration
# If don't want to use environment variables use:
# GROQ_API_KEY = <YOUR API KEY>
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Creating the Groq Client
client = Groq(
    api_key=GROQ_API_KEY,
)

# Setting the model we'll use
MODEL_NAME = "llama3-70b-8192"

# file to save all the conversations
CONVERSATIONS_FILE = "./conversations/saved_conversations.json"


# Function to make streaming work with groq
def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


# Function to save all conversations to a single file
def save_conversation(convo_name):
    convo_file = CONVERSATIONS_FILE
    if os.path.exists(convo_file):
        with open(convo_file, "r") as f:
            all_conversations = json.load(f)
    else:
        all_conversations = {}

    all_conversations[convo_name] = st.session_state.messages

    with open(convo_file, "w") as f:
        json.dump(all_conversations, f)

    st.session_state.saved_conversations = list(all_conversations.keys())
    st.success(f"Conversation '{convo_name}' saved!")


# Function to load a conversation from the file
def load_conversation(convo_name):
    convo_file = CONVERSATIONS_FILE
    if os.path.exists(convo_file):
        with open(convo_file, "r") as f:
            all_conversations = json.load(f)
        if convo_name in all_conversations:
            st.session_state.messages = all_conversations[convo_name]
            st.success(f"Conversation '{convo_name}' loaded!")
        else:
            st.error(f"No conversation found with the name '{convo_name}'.")
    else:
        st.error("No conversations file found.")


# Function to list all saved conversations
def list_conversations():
    convo_file = CONVERSATIONS_FILE
    if os.path.exists(convo_file):
        try:
            with open(convo_file, "r") as f:
                all_conversations = json.load(f)
            return list(all_conversations.keys())
        except Exception:
            return []
    return []


# Configuring the chatbot using streamlit

# Page title
st.subheader("bnaGPT - Chatbot with memory and saved conversation")


# Initialize session state variables

# Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# show_confirm_save = variable that will store whether the button of
# confirm save should be seen
if "show_confirm_save" not in st.session_state:
    st.session_state.show_confirm_save = False

# saved_conversations = variable to store all conversations
if "saved_conversations" not in st.session_state:
    st.session_state.saved_conversations = list_conversations()

# Sidebar to load saved conversations
with st.sidebar:
    if st.button("Save Current Conversation"):
        st.session_state.show_confirm_save = True
    if st.session_state.show_confirm_save:
        save_convo_name = st.text_input("Enter a name to save the conversation:")
        if st.button("Confirm Save") and save_convo_name:
            save_conversation(save_convo_name)
            st.session_state.show_confirm_save = False

    # UI for saving a conversation
    st.subheader("Saved Conversations")
    for convo_name in st.session_state.saved_conversations:
        if st.sidebar.button(convo_name):
            load_conversation(convo_name)

# Output messages where:
# role = user or assistant
# content = content of the message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Receiving the input from the user
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Printing the user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Now creating the assistant response
    with st.chat_message("assistant"):
        # Using groq to get the response
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=st.session_state.messages,
            # Setting stream as True to get the response little by little
            # Set as False if you want response at once
            stream=True,
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})
