import socket

# IP-Adresse und Port des Microcontrollers anpassen!
HOST = '192.168.137.146'  # Beispiel: IP des Microcontrollers
PORT = 12345          # Muss mit Server-Port übereinstimmen

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode('utf-8'))
        response = s.recv(1024)
        print("Antwort vom Server:", response)

if __name__ == "__main__":
    while True:
        cmd = input("Befehl an Microcontroller senden: ")
        send_command(cmd)
