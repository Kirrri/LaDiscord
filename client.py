import socket
import threading
import pyaudio
import time

# Константы для аудио
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Для моно
RATE = 22050  # Частота пониже для улучшения передачи
CHUNK = 2048  # Увеличение буфера

def receive_audio(sock):
    global stream
    while True:
        try:
            data = sock.recv(4096)  # Увеличение размера получаемого блока данных
            if data:
                # Воспроизводим аудио
                stream.write(data)
        except Exception as e:
            print(f"Ошибка при получении аудио: {e}")
            break

def send_audio(sock):
    global stream
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)  # Чтение аудиоданных с защитой от переполнения
            sock.sendall(data)  # Отправка аудиоданных на сервер
            time.sleep(0.01)  # Небольшая пауза для сглаживания потока
        except Exception as e:
            print(f"Ошибка при отправке аудио: {e}")
            break

def main():
    global stream  # Определяем глобальную переменную
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ip = str(input("Введите ip сервака: "))
        client.connect((ip, 55055))  # Замените на IP адрес вашего сервера

        channel_name = input("Введите имя аудио канала: ")
        password = input("Введите пароль для канала: ")

        client.send(channel_name.encode('utf-8'))
        client.send(password.encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        print(response)

        if "Канал создан." in response or "присоединились в response":
            # Настройка PyAudio для захвата и воспроизведения звука
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, input=True, frames_per_buffer=CHUNK)

            # Запуск потока для получения аудиосообщений
            threading.Thread(target=receive_audio, args=(client,), daemon=True).start()

            # Запуск потока для отправки аудиоданных
            threading.Thread(target=send_audio, args=(client,), daemon=True).start()

            # Удерживаем основной поток активным
            while True:
                pass

    except Exception as e:
        print(f"Ошибка подключения к серверу: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()