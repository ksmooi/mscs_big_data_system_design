

# setup RDBMS database (postgresql)
sudo -i -u postgres && createdb stock_vision_db && exit
psql -U postgres -d stock_vision_db -f src/db/schema.sql



install rabbitmq docker and add it into docker-compose
```yml
  rabbitmq:
    image: rabbitmq:3.13-management
    ports:
      - 5672:5672
      - 15672:15672
    restart: on-failure
```

Access to rabbitmq management:
http://192.168.1.150:15672/
default username and password: guest/guest



## Setup RabbitMQ

Creating exchanges, queues, and routing keys in RabbitMQ:

1. **Add a New Exchange:**
   - **Name:** `stockvision_exchange`
   - **Type:** `topic`
   - **Durability:** `Durable`
   - **Auto delete:** `No`
   - **Internal:** `No`
   - **Arguments:** Leave blank

2. **Add a New Queue for Stock Data:**
   - **Name:** `stock_data_queue`
   - **Durability:** `Durable`
   - **Arguments:** Leave blank

3. **Bind `stock_data_queue` to `stockvision_exchange`:**
   - Click on `stock_data_queue`.
   - Scroll down to the "Bindings" section.
   - In the "Add binding from this queue" section:
     - **Exchange:** `stockvision_exchange`
     - **Routing key:** `stock.data`
   - Click the "Bind" button.

4. **Add a New Queue for Analysis Results:**
   - **Name:** `analysis_results_queue`
   - **Durability:** `Durable`
   - **Arguments:** Leave blank

5. **Bind `analysis_results_queue` to `stockvision_exchange`:**
   - Click on `analysis_results_queue`.
   - Scroll down to the "Bindings" section.
   - In the "Add binding from this queue" section:
     - **Exchange:** `stockvision_exchange`
     - **Routing key:** `analysis.results`
   - Click the "Bind" button.

### Summary of Configuration of RabbitMQ

- **Exchange:**
  - Name: `stockvision_exchange`
  - Type: `topic`
  - Durability: `Durable`

- **Queues:**
  - Name: `stock_data_queue`
    - Purpose: Stores stock data fetched by the Data Collector Service.
    - Binding Key: `stock.data`
  - Name: `analysis_results_queue`
    - Purpose: Stores analysis results produced by the Data Analyzer Service.
    - Binding Key: `analysis.results`





