import sys
import socket
import ssl
import rsa

n = len(sys.argv)

if (n != 3):
  print("\nPlease provide domain and port number in order <domain> <port>, two arguments needed in total!!!\n")
  exit(0)

try:
  server_domain = sys.argv[1]
  server_port = int(sys.argv[2])
except Exception as e:
  print("Please type the port number with digits!!!")
  exit(0)

try:
  server_domain = socket.gethostbyname(server_domain)
except:
  print("\n\tInvalid server domain!!!!\n")
  exit(0)

# context = ssl.SSLContext(ssl.PROTOCOL_TLS)
secure_socket_client = socket.socket()
# secure_socket_client = context.wrap_socket(socket_client)
secure_socket_client.connect((server_domain, server_port))

with open("./public.pem", "rb") as f:
    publicKey = rsa.PublicKey.load_pkcs1(f.read())

print(secure_socket_client.recv(1024).decode('utf-8'))

while True:
    data = input("Enter your id:\t")
    if (data == ""): continue
    secure_socket_client.send(rsa.encrypt(data.encode(), publicKey))
    data = input("Enter your password:\t")
    if (data == ""): continue
    secure_socket_client.send(rsa.encrypt(data.encode(), publicKey))
    r = secure_socket_client.recv(8192)
    # print(r)
    if r.decode() != "0":
      break
    else:
        print("\nWrong id or password! Please enter your id and password again!!!\n")

try:
  currentBalance = int(secure_socket_client.recv(1024).decode())

  while True:
    data = input(f"\nYour account balance is {currentBalance}. Please select one of the following actions:\n\t1. Deposit\n\t2. Exit\n\tChoice: ")
    if (data == ""): continue
    if data == "1":
      data = input("\tEnter Deposit Amount: ")
      secure_socket_client.send(data.encode())
      r = secure_socket_client.recv(8192).decode()
      if r == "0": print("Deposit is not succeed. Try again!")
      else: currentBalance += int(data)
    elif data == "2":
      secure_socket_client.send(('2').encode())
      secure_socket_client.close()
      break
    else: print("\nInvalid Action Number!!!")

  secure_socket_client.close()
  # socket_client.close()

except KeyboardInterrupt:
    secure_socket_client.close()
