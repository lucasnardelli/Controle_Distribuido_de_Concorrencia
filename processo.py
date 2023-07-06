import socket
import threading
import time
import random

HOST = '10.226.0.90'  # Endereço IP do servidor
PORT = 1234  # Porta que será utilizada para a comunicação

# Número de clientes a serem simulados
num_clientes = 5

def processo():
    cont = random.randint(1, 100)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     # Conecta ao servidor
    cliente.connect((HOST, PORT))
    # Envia a mensagem para o servidor
    mensagem = 'REQUEST ' + str(cont)
    cliente.send(mensagem.encode())
    # Recebe a resposta do servidor
    resposta = cliente.recv(1024).decode()
    while(True):
        aux = resposta.split(' ')
        if(str(aux[0]) == 'GRANT'):
            time.sleep(10)
            print("Acesso concedido ao processo " + aux[1])
            mensagem = 'RELEASE'
            cliente.send(mensagem.encode())
            break

    # Fecha a conexão com o servidor
    cliente.close()

# Loop para simular vários clientes
for i in range(num_clientes):
    threading.Thread(target=processo).start()
    # Cria o socket TCP/IP
