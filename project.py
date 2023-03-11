import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

nicknames=[]

question = [
    "How many states are there in India?\n a.29\n b.26\n c.28\n d.35\n",
    "How many Union territories are there in India?\n a.7\n b.8\n c.9\n d.10\n",
    "Which is the Biggest state in India?\n a.Rajasthan\n b.Karnataka\n c.Tamil Nadu\n d.Delhi\n",
    "Which is the smallest state in India?\n a.Rajasthan\n b.Goa\n c.Tamil Nadu\n d.Delhi\n",
    "Which Fruit contain Vitamin D?\n a.Apple\n b.Oranges\n c.Banana\n d.Avocados"
]
answer = ['c' , 'b' , 'a' , 'b' , 'b']
server.bind((ip_address, port))
#we want server to bind with ip address and port
#we want server to listen multpile clients
server.listen()

list_of_clients = []

print("Server has started...")

def get_question(conn):
    random_index = random.randint(0,len(question)-1)
    random_question = question[random_index]
    random_answer = answer[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def clientthread(conn,nickname):
    s = 0
    conn.send('Welcome to this quiz game!'.encode('utf-8'))
    
    index , question,answer = get_question(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower() == answer:
                    s +=1
                    conn.send(f"Bravo! Your score is {s}\n\n".encode('utf-8'))
                else:
                    conn.send('Wrong answer. Please try agin :)')
                remove_ques(index)
                index , question,answer= get_question(conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue



def remove_ques(index):
    question.pop(index)
    answer.pop(index)



def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()

