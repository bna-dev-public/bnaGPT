import os
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


# Function to make streaming work with groq
def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


# Configuring the chatbot using streamlit

# Page title
st.title("bnaGPT - Chat Simples")

# Streamlit has a session element that you can create and save variables in it

# So that way we can create a variable called messages
# to save and output the messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# output messages where:
# role = user or assistant
# content = content of the message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# receving the input from the user
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # printing the user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # now creating the assistant response
    with st.chat_message("assistant"):

        # using groq to get the response
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            # setting stream as True to get the response little by little
            # set as False if you want response at once
            stream=True,
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})
