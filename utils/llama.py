from dataclasses import dataclass, field
from typing import Dict
from llama_index.llms.groq import Groq
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.memory import ChatMemoryBuffer

# from llama_index.core.storage.chat_store import SimpleChatStore
from settings import GROQ_API_KEY, DEFAULT_LLM
from view.general import print_error


@dataclass(slots=True)
class Llama:
    llm: Dict[str, str] = field(default_factory=lambda: DEFAULT_LLM)

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

    def create_openAI_agent(
        self,
        memory: ChatMemoryBuffer = ChatMemoryBuffer.from_defaults(),
    ) -> OpenAIAgent:
        llm = self.create_llm()
        agent = OpenAIAgent.from_tools(
            llm=llm,
            memory=memory,
        )
        return agent
