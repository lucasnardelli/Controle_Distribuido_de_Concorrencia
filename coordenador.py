import socket
import threading
import time

HOST = '10.226.0.90'  # Endereço IP do servidor
PORT = 1234  # Porta que será utilizada para a comunicação

# Cria o socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz a associação do socket com o endereço e porta
servidor.bind((HOST, PORT))

# Lista para armazenar os clientes conectados
clientes = []
mutex = []
processos_atendidos = {}

def handle_cliente():
    while True:
        if(len(clientes) != 0):
            cliente = clientes[0]
            # Recebe a mensagem do cliente
            mensagem = cliente.recv(1024).decode()
            aux = str(mensagem).split(' ')
            # Envia uma resposta para o cliente
            if(len(mutex) == 0):
                resposta = 'GRANT ' + str(aux[1])
                mutex.append(str(aux[1]))
                if (str(aux[1]) in processos_atendidos):
                    processos_atendidos[str(aux[1])] += 1
                else:
                    processos_atendidos[str(aux[1])] = 1
                cliente.send(resposta.encode())

            while(mensagem != 'RELEASE'):
                mensagem = cliente.recv(1024).decode()
            
            mutex.pop()
            clientes.pop(0)
        

def handle_interface():
    while True:
        command = input("Digite o comando (1: imprimir fila, 2: imprimir processos atendidos): ")
        if command == '1':
            print(f"Fila de processos: {clientes}")
        elif command == '2':
            for chave, valor in processos_atendidos.items():
                print("Processo " + str(chave) + " foi atendido " + str(valor) + " vezez!")

        else:
            print("Comando inválido.")


# Habilita o servidor para receber conexões
threading.Thread(target=handle_interface).start()
servidor.listen()

print('Aguardando conexões...')
threading.Thread(target=handle_cliente).start()

while True:
    # Aceita a conexão do cliente
    cliente, endereco = servidor.accept()
    print('Conexão estabelecida de:', endereco)
    # Adiciona o cliente à lista de clientes
    clientes.append(cliente)

    # Cria uma thread para lidar com a comunicação do cliente
