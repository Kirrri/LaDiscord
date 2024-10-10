import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.31.64', 12345))  # Замените на IP адрес вашего сервера

    channel_name = input("Введите имя аудио канала: ")
    password = input("Введите пароль для канала: ")

    client.send(channel_name.encode('utf-8'))
    client.send(password.encode('utf-8'))

    response = client.recv(1024).decode('utf-8')
    print(response)

    # Если канал создан или пользователь присоединился, запускаем поток для получения сообщений
    if "Канал создан." in response or "присоединились" in response:
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

        # Основной цикл для ввода сообщений
        while True:
            message = input("")
            if message:
                client.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()