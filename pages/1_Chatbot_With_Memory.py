from view.chatbot_with_memory import ChatbotWithMemoryView


# main function of the Simple Chatbot
def main():
    sc = ChatbotWithMemoryView()
    sc.build_config()
    chat_input = sc.build_body()
    sc.initialize_session()
    sc.build_sidebar()
    sc.handle_chat_input(chat_input)


if __name__ == "__main__":
    main()
