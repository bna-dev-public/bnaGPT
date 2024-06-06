from view.simple_chatbot import SimpleChatbotView


# main function of the Simple Chatbot
def main():
    sc = SimpleChatbotView()
    sc.build_config()
    chat_input = sc.build_body()
    sc.build_sidebar()
    sc.initialize_session()
    sc.handle_chat_input(chat_input)


if __name__ == "__main__":
    main()
