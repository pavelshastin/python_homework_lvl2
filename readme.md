Сервер запускается в файле server.py -a <address> -p <port> По умолчанию "":7777

Клиент на чтение запускается client.py -r -ns <username> -ps <password> По умолчанию <Pavel><Password>

Клиент на запись client.py -w -ns <username> -ps <password> По умолчанию <Pavel><Password>
    После запуска предлаются 2 поля To Chat: и Message.
    В поле To chat писать new
    
При запуске клиента он добавляется в чат

При запуске сервера создается чат "new" в которой добавляют 6 пользователей с именами Pavel, Pavel_2, Sveta, 
                                                                            Girl, Me, Alex
                                                                            
В файле MessageHandler попытка реализовать шаблон Посредник Mediator