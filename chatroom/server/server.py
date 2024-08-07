from chat_server import chatServer

if __name__ == "__main__":
    print("in server:")
    chat_server = chatServer()
    chat_server.listen()
    chat_server.accept()