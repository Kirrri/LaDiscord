import socket
import threading

# Словарь для хранения активных каналов
active_channels = {}

def handle_client(client_socket):
    global active_channels

    try:
        # Получаем имя канала от клиента
        channel_name = client_socket.recv(1024).decode('utf-8')
        password = client_socket.recv(1024).decode('utf-8')

        if channel_name not in active_channels:
            active_channels[channel_name] = {'password': password, 'clients': [client_socket]}
            client_socket.send("Канал создан.".encode('utf-8'))
        else:
            if active_channels[channel_name]['password'] == password:
                active_channels[channel_name]['clients'].append(client_socket)
                client_socket.send("Вы присоединились к каналу.".encode('utf-8'))
            else:
                client_socket.send("Неверный пароль!".encode('utf-8'))

        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                    # Передаем аудиосообщение другим клиентам в этом канале
                    for client in active_channels[channel_name]['clients']:
                        if client != client_socket:
                            client.sendall(data)
                else:
                    break
            except Exception as e:
                print(f"Ошибка в обработке данных от клиента: {e}")
                break
    except Exception as e:
        print(f"Ошибка в обработке клиента: {e}")
    
    finally:
        # Закрытие соединения
        client_socket.close()
        active_channels[channel_name]['clients'].remove(client_socket)
        if not active_channels[channel_name]['clients']:
            del active_channels[channel_name]

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 55055))  # 0.0.0.0 для внешнего доступа
    server.listen(5)
    print("Сервер запущен и слушает на порту 55055. Этот порт должен быть свободен.")

    while True:
        client_socket, addr = server.accept()
        print(f"Подключен клиент: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()