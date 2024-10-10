import socket
import threading

# Словарь для хранения активных каналов
active_channels = {}

def handle_client(client_socket):
    global active_channels

    # Получаем имя канала от клиента
    channel_name = client_socket.recv(1024).decode('utf-8')
    password = client_socket.recv(1024).decode('utf-8')

    if channel_name not in active_channels:
        active_channels[channel_name] = {'password': password, 'clients': [client_socket]}
        client_socket.send("Канал создан.".encode('utf-8'))  # Кодируем строку в байты
    else:
        if active_channels[channel_name]['password'] == password:
            active_channels[channel_name]['clients'].append(client_socket)
            client_socket.send("Вы присоединились к каналу.".encode('utf-8'))  # Кодируем строку в байты
        else:
            client_socket.send("Неверный пароль!".encode('utf-8'))  # Кодируем строку в байты

    # Поддержка связи с клиентом
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                for client in active_channels[channel_name]['clients']:
                    if client != client_socket:
                        client.send(message)
            else:
                break
        except:
            break

    # Закрытие соединения
    client_socket.close()
    active_channels[channel_name]['clients'].remove(client_socket)
    if not active_channels[channel_name]['clients']:
        del active_channels[channel_name]

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))  # 0.0.0.0 для внешнего доступа
    server.listen(5)
    print("Сервер запущен и слушает на порту 12345...")

    while True:
        client_socket, addr = server.accept()
        print(f"Подключен клиент: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()