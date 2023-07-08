import socket
import threading
import time
import random
import datetime

HOST = '10.226.0.90'  # Endereço IP do servidor
PORT = 1234  # Porta que será utilizada para a comunicação

# Número de processos a serem simulados
n = 16
#repetições
r = 100
#tempo de cada processo
k = 1

def processo():
    cont = random.randint(1, 100)
    for i in range(r):
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
                print("Acesso concedido ao processo " + aux[1])
                # Obtém a data e hora atual
                data_hora_atual = datetime.datetime.now()

                # Formata a data e hora com milissegundos
                data_hora_formatada = data_hora_atual.strftime("%Y-%m-%d %H:%M:%S.%f")

                # Abre o arquivo em modo append e grava a data e hora
                with open("resultado.txt", "a") as arquivo:
                    arquivo.write("Processo " + str(aux[1]) + " " + data_hora_formatada + "\n")

                time.sleep(k)
                mensagem = 'RELEASE'
                cliente.send(mensagem.encode())
                break

    # Fecha a conexão com o servidor
    cliente.close()

# Loop para simular vários clientes
for i in range(n):
    threading.Thread(target=processo).start()
    # Cria o socket TCP/IP
