import json
import os

from dataclasses import dataclass, field
from typing import List, Tuple

from settings import CONVERSATIONS_FILE

from llama_index.agent.openai import OpenAIAgent
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.base.llms.types import MessageRole

from models.messages import Message

from utils.llama import Llama


@dataclass
class ChatBotWithMemoryEngine:
    llama: Llama = field(default_factory=Llama)

    def get_simple_chat_response(self, user_input) -> StreamingAgentChatResponse:
        try:
            stream = self.llama.simple_chat(user_input)
            return stream
        except Exception as e:
            raise ValueError(str(e))

    def create_openAI_agent(
        self, memory: ChatMemoryBuffer = ChatMemoryBuffer.from_defaults()
    ) -> OpenAIAgent:
        openAI_agent = self.llama.create_openAI_agent(memory)
        return openAI_agent

    @staticmethod
    def create_memory_from_historical_messages(
        messages: List[Message],
    ) -> ChatMemoryBuffer:
        chat_history = []
        for message in messages:
            chat_history.append(message.convert_message_to_chat_message())
        memory = ChatMemoryBuffer.from_defaults(chat_history=chat_history)
        return memory

    @staticmethod
    def chat_with_openAI_agent(openAI_agent, user_input) -> StreamingAgentChatResponse:
        if openAI_agent is not None:
            try:
                streaming_response = openAI_agent.stream_chat(user_input)
                return streaming_response
            except Exception as e:
                raise ValueError(str(e))
        else:
            raise ValueError("No OpenAI agent was found")


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


# Function to save all conversations to a single file
def save_conversation(convo_name, messages: List[Message]):
    convo_file = CONVERSATIONS_FILE
    if os.path.exists(convo_file):
        with open(convo_file, "r") as f:
            all_conversations = json.load(f)
    else:
        all_conversations = {}
    formatted_messages = []
    for message in messages:
        formatted_messages.append(message.create_message())
    all_conversations[convo_name] = formatted_messages
    with open(convo_file, "w") as f:
        json.dump(all_conversations, f)
    return list(all_conversations.keys())


# Function to load a conversation from the file
def load_conversation(convo_name) -> Tuple[List[Message], str]:
    convo_file = CONVERSATIONS_FILE
    if os.path.exists(convo_file):
        with open(convo_file, "r") as f:
            all_conversations = json.load(f)
        if convo_name in all_conversations:
            messages = []
            print(all_conversations[convo_name])
            for message in all_conversations[convo_name]:
                if message.get("role", "") == "user":
                    messages.append(
                        Message(MessageRole.USER, message.get("content", ""))
                    )
                if message.get("role", "") == "assistant":
                    messages.append(
                        Message(MessageRole.ASSISTANT, message.get("content", ""))
                    )
            return messages, "success"
        else:
            return [], "wrong convo name"
    else:
        return [], "no file found"


# Function to delete a conversation from the file
def delete_conversation(convo_name) -> Tuple[int, str]:
    convo_file = CONVERSATIONS_FILE
    if os.path.exists(convo_file):
        with open(convo_file, "r") as f:
            all_conversations = json.load(f)
        if convo_name in all_conversations:
            del all_conversations[convo_name]
            with open(convo_file, "w") as f:
                json.dump(all_conversations, f)
            return 200, "success"
        else:
            return 400, "no conversation found"
    else:
        return 400, "no conversations file found"
