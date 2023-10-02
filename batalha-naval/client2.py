import socket

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(('localhost', 12345))

board_size = int(tcp_client_socket.recv(1024).decode())
print(f"Tabuleiro do jogo: {board_size}x{board_size}")

def play_game():
    while True:
        guess = input("Faça um palpite (linha coluna): ")
        tcp_client_socket.send(guess.encode())
        response = tcp_client_socket.recv(1024).decode()
        print(response)
        if "Todos os navios foram afundados!" in response:
            print("Você venceu!")
            break

play_game()

tcp_client_socket.close()
