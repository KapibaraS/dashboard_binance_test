# Order Book

### binance
- задумувался як основний сервіс для роботи з api binance, щоб збирати дані і записувати у базу та чергу **rabbitmq** (функціонал запису у базу реалізован не повністтю)

### dashboard
- сервіс для віддачі статики і підтримки вебсокетів з кліентами для оновлення в ріалтаймі (зараз сам ходить на api binance за orderbook і прослуховує чергу, якщо прийшов робить розсилку змін всім вебсокетам на кліенти, але без логики оновлення orderbook та графічної підтримки)


у кінці напишу, що зробив би ще


перейти у [config.py](binance%2Fconfig.py), [config.py](dashboard%2Fconfig.py) замінити шлях до конфігу на [dev-docker.yml](configs%2Fdev-docker.yml)[dev-locally.yml](configs%2Fdev-locally.yml)


запуск у докері виконати команду
```
make run
```

запуск локально
перейти у [config.py](binance%2Fconfig.py), [config.py](dashboard%2Fconfig.py) замінити шлях до конфігу на [dev-locally.yml](configs%2Fdev-locally.yml)
підняти mongo і rabbitmq
```
make run_localy
```
запуск у терміналі 
створити virtualenv
* https://docs.python.org/3/library/venv.html

виконати команди у різних терміналах (знаходячись у корневій дерикторії проекту)
```
python -m binance
```
```
python -m dashboard
```

Сорі, за просто малюнок, до того малював тільки діаграми баз даних онлайн і нічого не згадав пристойного

* це поточна архитектура 
![Очікування :))](images%2Fcurrent_version.jpg)
* 
* це фінальний задум (не працював з influxDB, але гадаю вона підходить саме для цієї задачі) 
![Реальність:))](images%2Ffinally_version.jpg)


Знаю про сваггер, але просто не встигав 
## endpoints

Rest API:

Базовый урл: https://localhost:8080
    
Методи запита
* GET /  
* Стартова сторінка з дашбордом

Websockets:

Базовый урл: ws://localhost:8080

Update depth:  
* WS /ws/update_depth
* Отримання Updatedepth

