import socket
import ssl
import sys
from _thread import *
import hashlib
import rsa

n = len(sys.argv)

if (n != 2):
  print("\nPlease provide port number, one argument needed in total!!!\n")
  exit()

try:
  port = int(sys.argv[1])
except Exception as e:
  print("Please type the port number with digits!!!")
  exit()

serverSocket = socket.socket()
serverSocket.bind(("", port))

ThreadCount = 0
try:
    serverSocket.bind(("", port))
except socket.error as e:
    print(str(e))

with open("./public.pem", "rb") as f:
    publicKey = rsa.PublicKey.load_pkcs1(f.read())

with open("./private.pem", "rb") as f:
    privateKey = rsa.PrivateKey.load_pkcs1(f.read())

balances = dict()
users = dict()

with open("./balance", "r") as f:
    line = f.readline().strip()
    while line:
        key, val = line.split()
        balances[key] = int(val)
        line = f.readline().strip()

with open("./passwd", "r") as f:
    line = f.readline().strip()
    while line:
        key, val = line.split()
        users[key] = val
        line = f.readline().strip()

flag = False
def threadedClient(conn):
  conn.send(str.encode('\nWelcome to the Bank...\n'))
  
  try:
    while True:
      username = rsa.decrypt(conn.recv(2048), privateKey).decode()
      password = rsa.decrypt(conn.recv(2048), privateKey).decode()
      
      if username in users.keys():
        if hashlib.md5(bytes(str(password), 'utf-8')).hexdigest() == users.get(username):
          conn.send(str.encode("1"))
          break
        else:
          conn.send(str.encode("0"))
      else:
        conn.send(str.encode("0"))

    conn.send(str(balances[username]).encode())

    data = conn.recv(2048).decode()

    while data != "2":
      try:
        balances[username] = balances[username] + int(data)
        conn.send(str.encode("1"))
      except:
        conn.send(str.encode("0"))
      data = conn.recv(2048).decode()

  except KeyboardInterrupt:
      conn.close()
      flag = True

  conn.close()
  print("Connection closed!\n\nNow Listening...")

  with open("./balance", "w") as f:
    for key, value in balances.items():
      f.write(f"{key} {value}\n")

try:
  serverSocket.listen(5)
  print("\nServer has been started. Now listening...")
  while not flag:
    client, address = serverSocket.accept()

    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threadedClient, (client,))
    # ThreadCount += 1
    # print('Thread Number: ' + str(ThreadCount))
except KeyboardInterrupt:
    serverSocket.close()
