import socket
import queue
from threading import Thread

S_ip = "127.0.0.1"
s_port = 1658

def get_input(Queue):
    while True:
        msg = input()
        Queue.put(msg)
        if msg == "q":
            break
def get_msg(s):
    data = s.recv(1024)
    print(data.decode())

if __name__ == "__main__":
    print("client:")
    print("To quit enter letter q")
    Queue = queue.Queue()
    thread = Thread(target=get_input, args=(Queue,))
    thread.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((S_ip,s_port))
        recive_thread = Thread(target=get_msg, args=(s,))
        recive_thread.start()
        while True:
            try:
                msg = Queue.get(timeout=5)
                if msg != None:
                    s.sendall(msg.encode())
                    if msg == 'q':
                        break
            except queue.Empty as e:
                pass
                # print("wating for massage")
    thread.join()