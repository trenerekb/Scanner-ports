import json
import socket





def scan(ip, begin_port, end_port, server_socket):

    result_scan = []

    try:
        for port_num in range(begin_port, end_port+1):
            result = server_socket.connect_ex((ip, port_num))
            
            if result == 0:
                result_scan.append({"port": port_num, "state": 'OPEN'})
                
            else:
                result_scan.append({"port": port_num, "state": 'CLOSE'})

        return json.dumps(result_scan)
        
    except Exception as ex:
        print(ex)
        


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # создаем субъекта для соединения по IP4 и TCP
    #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # создаем опциональные параметры для нашего сокеты на уровне сокетов 
    server_socket.bind(('localhost', 5000))                                 # связываем субъекта с локальным сервером и портом
    server_socket.listen()                                                  # даем субъекту задание в виде прослушки входящих сигналов

    while True:                                                             # создаем бесконечный цикл для постоянного получения инфы
        client_socket, addr = server_socket.accept()                        # принимаем картеж с данными в 2 переменные (клиентский сокет, адрес)
        request = client_socket.recv(1024)                                  # принимаем запрос от клиента
        response = request.decode('utf-8').split('/')                       # декодируем запрос клиента

        begin_port = int(response[2])
        end_port = int(response[3].split(' ')[0])
        ip = response[1]                                                        
        
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        result = scan(ip, begin_port, end_port, target_socket).encode()
        
        
        client_socket.sendall(f'HTTP/1.1 200 OK\n\n {result}'.encode())     # приобразум данные в байты и отвечаем клиентскому сокету 
        client_socket.close()                                               # закрываем соединение
        break


if __name__ == '__main__':
    run()