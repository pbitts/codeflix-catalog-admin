# Codeflix Catalog Admin

Catalog Administration service built with **Python** as part of the **FullCycle 3.0 Final Project**.
This project follows **Clean Architecture principles** and leverages modern tools to ensure scalability, security, and maintainability.

## 🚀 Technologies

* **Django** – Web framework for rapid development
* **RabbitMQ** – Message broker for asynchronous communication
* **Kafka** – Event streaming platform for scalability and resilience
* **Keycloak** – Identity and access management

## 📂 Project Overview

The service provides an administrative interface for managing the **Codeflix catalog**.
It integrates with a microservices ecosystem using message brokers and secure authentication, following domain-driven design and clean architecture practices.

## ⚙️ Setup & Running

### 1. Clone the repository

```bash
git clone https://github.com/pbitts/codeflix-catalog-admin.git
cd codeflix-catalog-admin
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Start RabbitMQ (via Docker)

```bash
docker run -d --hostname rabbitmq --name rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management
```

### 6. Start the consumer

```bash
python manage.py startconsumer
```

### 7. Run the development server

```bash
python manage.py runserver
```

## 📖 Notes

* The project is designed to be **modular and extensible**.
* Follows **Clean Architecture** to separate business logic from frameworks.
* Works seamlessly as part of a **microservices environment**.
