from dataclasses import dataclass, field
from llama_index.llms.groq import Groq
from llama_index.core.chat_engine import SimpleChatEngine
from settings import DEFAULT_LLM_NAME, DEFAULT_LLM_PROVIDER, GROQ_API_KEY
from view.general import print_error


@dataclass(slots=True)
class Llama:
    llm: dict = field(
        default_factory=lambda: {
            "llm_provider": DEFAULT_LLM_PROVIDER,
            "llm_name": DEFAULT_LLM_NAME,
        }
    )

    def create_llm(self):
        if self.llm.get("llm_provider") == "groq":
            try:
                llm = Groq(model=self.llm.get("llm_name", ""), api_key=GROQ_API_KEY)
            except Exception as e:
                print_error("Error to create the llm: " + str(e))

        else:
            print_error("We only accept groq models right now")

        return llm

    def create_simple_chat_engine(self):
        llm = self.create_llm()
        simple_chat_engine = SimpleChatEngine.from_defaults(llm=llm)
        return simple_chat_engine

    def simple_chat(self, user_input):
        simple_chat_engine = self.create_simple_chat_engine()
        stream = simple_chat_engine.stream_chat(user_input)
        return stream
