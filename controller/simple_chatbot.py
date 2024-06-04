from dataclasses import dataclass, field
from utils.llama import Llama


@dataclass(slots=True)
class SimpleChatEngine:
    llama: Llama = field(default_factory=Llama)

    def get_simple_chat_response(self, user_input):
        stream = self.llama.simple_chat(user_input)
        return stream
