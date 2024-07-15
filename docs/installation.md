# StockVision Installation Guide

## Overview

This guide provides detailed instructions for installing and setting up the StockVision application, which includes components for data collection, storage, analysis, and API access. The installation process involves setting up the PostgreSQL database, RabbitMQ server, configuring the application, and running the backend services.

## Prerequisites

- Docker installed on your machine
- Python 3.8 or later installed on your machine
- `git` installed on your machine

## Installation Steps

### 1. Install Server Components

#### Install PostgreSQL Server (Docker)

```bash
docker run --name stockvision-postgres -e POSTGRES_PASSWORD=24785699 -e POSTGRES_USER=mscs_dba -e POSTGRES_DB=stock_vision_db -p 5432:5432 -d postgres
```

#### Install RabbitMQ Server (Docker)

Add the following service definition to your `docker-compose.yml`:

```yml
rabbitmq:
  image: rabbitmq:3.13-management
  ports:
    - 5672:5672
    - 15672:15672
  restart: on-failure
```

Start the RabbitMQ server:

```bash
docker-compose up -d rabbitmq
```

### 2. Setup the Database Schema

#### Access the PostgreSQL Container

```bash
docker exec -it stockvision-postgres psql -U mscs_dba -d stock_vision_db
```

#### Create the Database and Setup Schema

```sql
\i /path/to/src/db/schema.sql
```

Replace `/path/to/src/db/schema.sql` with the actual path to the `schema.sql` file.

### 3. Setup RabbitMQ

#### Access RabbitMQ Management Interface

Open your browser and navigate to:

```
http://192.168.1.150:15672/
```

Login with the default credentials:

- Username: `guest`
- Password: `guest`

#### Create Exchanges, Queues, and Bindings

1. **Add a New Exchange:**
   - **Name:** `stockvision_exchange`
   - **Type:** `topic`
   - **Durability:** `Durable`

2. **Add a New Queue for Stock Data:**
   - **Name:** `stock_data_queue`
   - **Durability:** `Durable`

3. **Bind `stock_data_queue` to `stockvision_exchange`:**
   - Click on `stock_data_queue`.
   - Scroll to the "Bindings" section.
   - **Exchange:** `stockvision_exchange`
   - **Routing key:** `stock.data`

4. **Add a New Queue for Analysis Results:**
   - **Name:** `analysis_results_queue`
   - **Durability:** `Durable`

5. **Bind `analysis_results_queue` to `stockvision_exchange`:**
   - Click on `analysis_results_queue`.
   - Scroll to the "Bindings" section.
   - **Exchange:** `stockvision_exchange`
   - **Routing key:** `analysis.results`

### 4. Configure the Application Settings

Edit the `config/config.json` file to match your environment settings. Below is an example configuration:

```json
{
    "rabbitmq": {
        "user": "guest",
        "password": "24785699",
        "host": "192.168.1.150",
        "port": 5672
    },
    "data_collector": {
        "schedule_interval": 60,
        "stocks": [
            "AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NFLX", "NVDA", "ADBE", "INTC", 
            "AMD", "CSCO", "ORCL", "IBM", "BABA", "T", "VZ", "PYPL", "CRM", "SHOP"
        ]
    },
    "data_recorder": {
        "database": {
            "host": "localhost",
            "port": 5432,
            "user": "mscs_dba",
            "password": "24785699",
            "dbname": "stock_vision_db"
        }
    },
    "data_analyzer": {
        "analysis_interval": 300
    },
    "stock_server": {
        "host": "0.0.0.0",
        "port": 60001,
        "debug": true
    },
    "api_server": {
        "host": "0.0.0.0",
        "port": 60002,
        "debug": true
    }
}
```

### 5. Start and Stop StockVision Application

#### Starting the Application

1. **Create and Activate a Virtual Environment:**

```bash
python3 -m venv myenv && source myenv/bin/activate
```

2. **Upgrade `pip` and Install Dependencies:**

```bash
pip install --upgrade pip && pip install -r requirements.txt
```

3. **Start the Backend:**

```bash
python src/backend.py
```

#### Stopping the Application

1. **Stop the Backend:**

Press `Ctrl+C` in the terminal where `backend.py` is running.

2. **Deactivate the Virtual Environment:**

```bash
deactivate
```

## Database Schema Overview

### Introduction to the StockVision Database Schema

The StockVision database schema is designed to support the various components and functionalities of the StockVision system, including data collection, storage, analysis, and API access. The schema is composed of several tables, each serving a distinct purpose within the system. Here is an overview of the main tables in the StockVision schema:

### Tables Overview

1. **stock_data**
   - Stores raw stock data retrieved from the Yahoo Finance API, ensuring no duplicate records for the same ticker and date.

2. **stock_analysis**
   - Holds the results of data analysis performed on the stock data, allowing for flexible storage of various analysis results.

3. **analysis_types**
   - Defines different types of analyses that can be performed, providing a reference for available analysis types.

4. **api_keys**
   - Manages API keys for accessing the RESTful API, ensuring secure and managed access.

5. **users**
   - Stores user information for those accessing the system, supporting user authentication and management.

6. **logs**
   - Stores logs for data processing and analysis activities, essential for monitoring and debugging the system.

By following this installation guide, you should be able to set up the StockVision application successfully, configure its components, and run the backend services.

