from dataclasses import dataclass
from llama_index.core.chat_engine.types import StreamingAgentChatResponse


@dataclass(slots=True)
class Message:
    role: str
    content: str

    def create_message(self):
        message = {"role": self.role, "content": self.content}
        return message


@dataclass(slots=True)
class StreamingMessage:
    streaming_response: StreamingAgentChatResponse

    def stream_message(self):
        for token in self.streaming_response.response_gen:
            yield token + ""
