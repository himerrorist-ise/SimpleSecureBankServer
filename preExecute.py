import rsa
import os

# creating public and private keys for encryption and decryption
publicKey, privateKey = rsa.newkeys(1024)

with open("./server/public.pem", "wb") as f:
  f.write(publicKey.save_pkcs1("PEM"))

with open("./server/private.pem", "wb") as f:
  f.write(privateKey.save_pkcs1("PEM"))

# copying public key to the client for using it to encrypt login info
os.system("cp ./server/public.pem ./client")


users = {
  "alice": 1234,
  "bob" : 5678,
  "tom" : 9012,
}

# creating balance file
with open("./server/balance", "w") as f:
  for usr in users.keys():
    f.write(f"{usr} 10000\n")

# creating passwd file
# hashing the passwords by using MD5 which can be used with hashlib library
import hashlib
with open("./server/passwd", "w") as f:
  for key,val in users.items():
    f.write(f"{key} {hashlib.md5(bytes(str(val), 'utf-8')).hexdigest()}\n")
    # f.write(f"{key} {hashlib.md5(str(val).encode())}\n")

# with open("./server/passwd", "r") as f:
#   line = f.readline()
#   while line:
#     print(line.strip().split())
#     line = f.readline()
  