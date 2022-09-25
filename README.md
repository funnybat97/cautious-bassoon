# cautious-bassoon

# Installation

Notice, that Project modules situated in 3 different folders and should be placed in same parent folder.


# Postgres Installation

 Install [PostgreSQL 14](https://www.postgresql.org/download/)


Connect to **postgres** Data Base and execute:
```sql
CREATE DATABASE navigate_db;
CREATE USER navigator WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE navigate_db TO navigator;
```
Connect to **navigate_db** Data Base and execute:
```sql
CREATE EXTENSION postgis;
```

# Docker Installation
Install [docker](https://www.docker.com/)

Install [docker-compose](https://docs.docker.com/compose/install/)

# Run App 
## Linux
 Build 
```sh
docker-compose build
```
 Run Docker
```sh
docker-compose up
```
# Mac OS

Here we have local DB, [but host networking works only for Linux](https://github.com/docker/for-mac/issues/6185#issuecomment-1068490007)

In this case flask API inside container would see postgres database...
## Local run
Install python
```shell
brew install python@3.9.12
```
[Windows](https://www.python.org/downloads/windows/)
create env
```shell
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
```
run app
```shell
 python3 navigate/run.py
```

## Solution

You can find orders in http://127.0.0.1:8000/api or http://127.0.0.1:8000/

BONUS

You can find the farthest rider in http://127.0.0.1:8000/api/farthest_rider

BONUS

You can find the busiest restaurant in http://127.0.0.1:8000/api/farthest_rider
You can find the customer with the biggest appetite in http://127.0.0.1:8000/api/biggest_appetite

SUPERBONUS

Use POST requset http://127.0.0.1:8000/api/add_new_order
with body 
```json
{
    "customer_id": 2,
    "directions_to_customer": "NESWWWWW",
    "id": 41,
    "order_delivery_distance": 6,
    "order_delivery_time": "Thu, 09 Jun 2022 12:56:17 GMT",
    "order_id": "aa5895329a4b2a59dfd5e5714deb23eaa7207431e69b692bb8567fa1796217f6",
    "order_pickup_time": "Thu, 09 Jun 2022 12:43:23 GMT",
    "restaurant_id": 1,
    "rider_name": "Edith"
}
```
You will see new order in http://127.0.0.1:8000/api or http://127.0.0.1:8000/.
You will also receive it in response.