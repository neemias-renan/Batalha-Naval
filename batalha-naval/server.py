import socket
import random

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(('0.0.0.0', 12345))
tcp_server_socket.listen(2)

# Função para gerar o tabuleiro do jogo
def generate_board(size):
    board = [[0 for _ in range(size)] for _ in range(size)]
    for _ in range(size):
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        board[row][col] = 1
    return board

# Função para verificar o palpite do cliente
def guess_ship_position(board, row, col):
    if board[row-1][col-1] == 1:
        board[row-1][col-1] = "X"  # Navio atingido
        print("Tabuleiro do jogo:")
        for row in board:
            print(" ".join(map(str, row)))
        return "Acertou!"
    
    else:
        return "Errou!"

# Defina o tamanho do tabuleiro aqui
board_size = 3

# Gere o tabuleiro do jogo
board = generate_board(board_size)
print("Tabuleiro do jogo:")
for row in board:
    print(" ".join(map(str, row)))

# Espere por duas conexões TCP
clients = []

for _ in range(2):
    conn, addr = tcp_server_socket.accept()
    print(f"Conexão TCP de {addr}")
    clients.append(conn)

# Envie o tamanho do tabuleiro para os clientes
for conn in clients:
    conn.send(str(board_size).encode())

# Inicie o jogo
turn = 0
while True:
    conn = clients[turn]

    guess = conn.recv(1024).decode()
    if not guess:
        print(f"Cliente {turn+1} desconectado")
        break

    row, col = map(int, guess.split())
    
    result = guess_ship_position(board, row, col)
    print(f"Palpite de Cliente {turn+1}: ({row}, {col}) -> {result}")
            
    if all(all(cell != 1 for cell in row) for row in board):
        result = "Todos os navios foram afundados!"
        print(result)
        for conn in clients:
            conn.send(result.encode())
        break
        
    for conn in clients:
        conn.send(result.encode())

    turn = (turn + 1) % 2

# Feche os sockets quando o jogo terminar
for conn in clients:
    conn.close()

tcp_server_socket.close()
