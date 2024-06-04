from view.simple_chatbot import SimpleChatbot


# main function of the Simple Chatbot
def main():
    sc = SimpleChatbot()
    sc.build_config()
    chat_input = sc.build_body()
    sc.build_sidebar()
    sc.update_session()
    sc.handle_chat_input(chat_input)


if __name__ == "__main__":
    main()
