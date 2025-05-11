import socket
import os

#hostname = socket.gethostname()

localhost = socket.gethostbyname(socket.gethostname())
TARGET = os.getenv('TARGET', f'{localhost}:4000')

#print("Your Computer Name is: " + hostname)

print("Your Computer IP Address is: " + localhost)

print(f"http://{TARGET}/recipe/42")