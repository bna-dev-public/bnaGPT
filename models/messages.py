from dataclasses import dataclass
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.core.base.llms.types import ChatMessage, MessageRole


@dataclass(slots=True)
class Message:
    role: MessageRole
    content: str

    def create_message(self):
        message = {"role": self.role.value, "content": self.content}
        return message

    def convert_message_to_chat_message(self) -> ChatMessage:
        chat_message = ChatMessage(role=self.role, content=self.content)
        return chat_message


@dataclass(slots=True)
class StreamingMessage:
    streaming_response: StreamingAgentChatResponse

    def stream_message(self):
        for token in self.streaming_response.response_gen:
            yield token + ""
