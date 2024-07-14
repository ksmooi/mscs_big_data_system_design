# StockVision System Design Document

## Introduction

### Purpose
The purpose of this document is to provide a comprehensive system design for StockVision, a system that collects, processes, analyzes, and visualizes stock market data. This document outlines the project's requirements, design decisions, system architecture, components, and testing strategies to ensure the development of a robust, scalable, and maintainable solution. StockVision aims to offer real-time insights and analysis for stock market data, catering to financial analysts, traders, and individual investors.

### Scope
StockVision encompasses the entire workflow from data collection to data visualization. The scope of this project includes:
- Collecting stock data from Yahoo Finance using a Data Collector Service.
- Managing message queues with RabbitMQ for reliable and scalable data processing.
- Storing collected data in a PostgreSQL database.
- Analyzing stock data with the Data Analyzer Service to generate meaningful insights.
- Providing a web interface through the Stock Server for data visualization.
- Offering programmatic access to data and analysis results via a RESTful API.
- Ensuring data integrity, backup, and recovery mechanisms.

## Project Requirements

### Data Collection
- **Requirement**: The system must fetch real-time stock data from the Yahoo Finance API.
- **Description**: The Data Collector Service will periodically retrieve stock data for a predefined list of stock tickers. The collected data includes open, high, low, close prices, and trading volume.
- **Schedule**: The data collection should run at regular intervals, configurable through the system settings.

### Message Queue Management
- **Requirement**: The system must handle data processing asynchronously using a message queue.
- **Description**: RabbitMQ will be used to decouple the data collection, recording, and analysis components, ensuring reliable and scalable data processing.
- **Queues**: Separate queues for raw stock data and analysis results.

### Data Storage
- **Requirement**: The system must store collected and processed data in a relational database.
- **Description**: PostgreSQL will be used to store raw stock data and analysis results. The database schema will ensure data integrity and support efficient querying.
- **Tables**: Tables for raw stock data (`stock_data`), analysis results (`stock_analysis`), analysis types (`analysis_types`), API keys (`api_keys`), users (`users`), and logs (`logs`).

### Data Analysis
- **Requirement**: The system must analyze collected stock data to generate insights.
- **Description**: The Data Analyzer Service will process the stock data to calculate metrics such as moving averages. The results will be stored in the database and made available for visualization and API access.
- **Algorithms**: Algorithms for calculating moving averages and other relevant financial metrics.

### Web Interface
- **Requirement**: The system must provide a web interface for visualizing stock data and analysis results.
- **Description**: A Flask-based web server (Stock Server) will render HTML templates to display stock data and analysis results. Users will be able to view data through a user-friendly interface.
- **Features**: Tables for displaying stock data and analysis results, with options for filtering and sorting.

### RESTful API
- **Requirement**: The system must provide a RESTful API for programmatic access to stock data and analysis results.
- **Description**: A Flask-based RESTful API server will expose endpoints for accessing stock data and analysis results. The API will support secure access through API keys.
- **Endpoints**: Endpoints for retrieving stock data (`/api/stock_data`) and analysis results (`/api/analysis_results`).

With these requirements, StockVision will deliver a comprehensive solution for collecting, processing, analyzing, and visualizing stock market data, meeting the needs of various users in the financial domain.


## System Design

### System Architecture
The system architecture of StockVision is designed to ensure scalability, reliability, and maintainability. The architecture consists of the following components:
- **Data Collector Service**: Periodically fetches stock data from the Yahoo Finance API.
- **RabbitMQ Broker**: Manages message queues for asynchronous data processing.
- **Data Recorder Service**: Consumes raw stock data from RabbitMQ and stores it in PostgreSQL.
- **Data Analyzer Service**: Analyzes stock data and stores the analysis results in PostgreSQL.
- **Stock Server (Flask Web Server)**: Provides a web interface for visualizing stock data and analysis results.
- **API Server (Flask RESTful API Server)**: Exposes RESTful endpoints for accessing stock data and analysis results.

### Components Description
- **Data Collector Service**: This service retrieves stock data for a predefined list of stock tickers from the Yahoo Finance API. It publishes the raw stock data to a RabbitMQ queue for further processing.
- **RabbitMQ Broker**: Acts as a middleware to manage message queues. It decouples the data collection, recording, and analysis processes, ensuring reliable message delivery and fault tolerance.
- **Data Recorder Service**: This service listens to the RabbitMQ queue for raw stock data messages, processes the data, and stores it in the PostgreSQL database.
- **Data Analyzer Service**: This service retrieves stock data from the PostgreSQL database, performs data analysis (e.g., calculating moving averages), and stores the results back in the database.
- **Stock Server (Flask Web Server)**: This server provides a web interface for users to view stock data and analysis results. It renders HTML templates and serves static files.
- **API Server (Flask RESTful API Server)**: This server provides RESTful endpoints for accessing stock data and analysis results. It supports secure access through API keys and returns data in JSON format.

### Data Flow Diagram
The data flow diagram illustrates the flow of data through the system components:
1. The **Data Collector Service** fetches stock data from the Yahoo Finance API and publishes it to a RabbitMQ queue.
2. The **Data Recorder Service** consumes messages from the RabbitMQ queue, processes the stock data, and stores it in the PostgreSQL database.
3. The **Data Analyzer Service** retrieves stock data from the PostgreSQL database, performs analysis, and stores the results back in the database.
4. The **Stock Server** retrieves data from the PostgreSQL database and displays it on a web interface.
5. The **API Server** provides endpoints for external clients to access stock data and analysis results.

## Design Decisions

### Justification of Design Decisions
1. **Use of RabbitMQ**: RabbitMQ is used to decouple the data collection, recording, and analysis processes. This ensures that each component can operate independently, improving system reliability and scalability. RabbitMQ provides robust message queuing and delivery guarantees, which are critical for handling real-time stock data.
2. **PostgreSQL Database**: PostgreSQL is chosen for its robustness, scalability, and support for complex queries. It ensures data integrity and provides efficient storage and retrieval of stock data and analysis results. PostgreSQL's support for JSONB allows for flexible storage of analysis results.
3. **Flask Framework**: Flask is used for both the web server and the API server due to its simplicity and flexibility. Flask allows rapid development and easy integration with other components. Its lightweight nature makes it suitable for microservices architecture.
4. **Yahoo Finance API**: The Yahoo Finance API is chosen for its comprehensive and reliable stock market data. It provides real-time data for a wide range of stock tickers, which is essential for accurate analysis and visualization.
5. **Modular Architecture**: The system is designed with a modular architecture, where each component handles a specific aspect of the workflow. This improves maintainability and allows individual components to be scaled independently based on demand.

### Attainability of Design Decisions
1. **Scalability**: The use of RabbitMQ ensures that the system can handle increased data volume by scaling individual components. Each service can be deployed on separate instances, and additional instances can be added as needed.
2. **Reliability**: RabbitMQ provides reliable message delivery, ensuring that stock data is not lost during transmission. PostgreSQL ensures data integrity with ACID compliance, and Flask provides a stable platform for web and API services.
3. **Maintainability**: The modular architecture allows for easy maintenance and updates. Each component can be developed, tested, and deployed independently. The use of Flask and PostgreSQL, both well-documented and widely used technologies, further enhances maintainability.
4. **Security**: The API server supports secure access through API keys, ensuring that only authorized clients can access the data. PostgreSQL provides robust security features for data protection.
5. **Performance**: The system is designed to handle real-time stock data with low latency. RabbitMQ ensures fast and reliable message queuing, and PostgreSQL provides efficient data storage and retrieval. The Flask framework supports high-performance web and API services.

By making these design decisions, the StockVision system is well-equipped to meet its goals of providing reliable, scalable, and maintainable stock market data analysis and visualization.


## System Components

### Data Collector Service
- **Description**: The Data Collector Service is responsible for periodically fetching stock data from the Yahoo Finance API.
- **Responsibilities**:
  - Fetch real-time stock data for a predefined list of stock tickers.
  - Parse and format the collected data.
  - Publish the collected data to a RabbitMQ queue for further processing.
- **Implementation Details**:
  - Uses the `yfinance` Python library to retrieve stock data.
  - Configured to run at regular intervals using a scheduler (e.g., APScheduler).
  - Publishes messages to the `stock_data_queue` in RabbitMQ.

### Message Queue (RabbitMQ Broker)
- **Description**: RabbitMQ acts as a message broker, managing queues for asynchronous communication between system components.
- **Responsibilities**:
  - Handle message queues for raw stock data and analysis results.
  - Ensure reliable message delivery and persistence.
  - Decouple the data collection, recording, and analysis processes to enhance scalability and reliability.
- **Implementation Details**:
  - RabbitMQ is configured with a topic exchange (`stockvision_exchange`) and multiple queues (`stock_data_queue`, `analysis_results_queue`).
  - Binding keys (`stock.data`, `analysis.results`) are used to route messages appropriately.

### Data Recorder Service
- **Description**: The Data Recorder Service consumes raw stock data from RabbitMQ and stores it in the PostgreSQL database.
- **Responsibilities**:
  - Listen to the `stock_data_queue` for new stock data messages.
  - Parse and validate the received data.
  - Insert or update the stock data in the PostgreSQL database.
- **Implementation Details**:
  - Uses the `pika` library to consume messages from RabbitMQ.
  - Connects to PostgreSQL using the `psycopg2` library.
  - Implements data integrity checks and handles duplicates based on unique constraints in the database schema.

### Data Analyzer Service
- **Description**: The Data Analyzer Service retrieves stock data from the PostgreSQL database, performs analysis, and stores the results back in the database.
- **Responsibilities**:
  - Periodically fetch stock data for analysis.
  - Perform financial analysis (e.g., calculating moving averages).
  - Store the analysis results in the `stock_analysis` table in PostgreSQL.
- **Implementation Details**:
  - Uses SQL queries to retrieve stock data and store analysis results.
  - Performs data analysis using pandas and other relevant Python libraries.
  - Can be triggered by a scheduler or directly from RabbitMQ messages.

### Stock Server (Flask Web Server)
- **Description**: The Stock Server provides a web interface for visualizing stock data and analysis results.
- **Responsibilities**:
  - Serve HTML templates and static files for the web interface.
  - Fetch stock data and analysis results from the PostgreSQL database.
  - Render data in user-friendly tables and charts.
- **Implementation Details**:
  - Built using the Flask web framework.
  - Templates are stored in the `templates` directory and use Jinja2 for rendering.
  - Static files (CSS, JavaScript) are stored in the `static` directory.

### API Server (Flask RESTful API Server)
- **Description**: The API Server provides RESTful endpoints for accessing stock data and analysis results programmatically.
- **Responsibilities**:
  - Expose endpoints for retrieving stock data (`/api/stock_data`) and analysis results (`/api/analysis_results`).
  - Handle requests and return data in JSON format.
  - Implement secure access through API keys.
- **Implementation Details**:
  - Built using the Flask web framework and the Flask-RESTful extension.
  - Routes are defined in the `routes.py` module.
  - Uses PostgreSQL for data storage and retrieval.

With these detailed descriptions, responsibilities, and implementation details, the System Components section of the StockVision System Design Document is now complete. Each component's role within the overall system architecture is clearly defined, providing a comprehensive understanding of how StockVision operates.


## Data Management

### Database Design
- **Schema Overview**: The PostgreSQL database schema is designed to store raw stock data, analysis results, user information, and logs. The main tables include `stock_data`, `stock_analysis`, `analysis_types`, `api_keys`, `users`, and `logs`.
- **Tables**:
  - **stock_data**:
    ```sql
    CREATE TABLE stock_data (
        id SERIAL PRIMARY KEY,
        ticker VARCHAR(10) NOT NULL,
        date DATE NOT NULL,
        open DECIMAL(10, 2) DEFAULT 0,
        high DECIMAL(10, 2) DEFAULT 0,
        low DECIMAL(10, 2) DEFAULT 0,
        close DECIMAL(10, 2) DEFAULT 0,
        volume BIGINT DEFAULT 0,
        UNIQUE (ticker, date)
    );
    ```
    - Stores raw stock data retrieved from Yahoo Finance.
  - **stock_analysis**:
    ```sql
    CREATE TABLE stock_analysis (
        id SERIAL PRIMARY KEY,
        stock_data_id INTEGER NOT NULL,
        analysis_date DATE NOT NULL,
        analysis_type VARCHAR(50) NOT NULL,
        result JSONB NOT NULL,
        FOREIGN KEY (stock_data_id) REFERENCES stock_data (id)
    );
    ```
    - Stores the results of data analysis.
  - **analysis_types**:
    ```sql
    CREATE TABLE analysis_types (
        id SERIAL PRIMARY KEY,
        type_name VARCHAR(50) UNIQUE NOT NULL,
        description TEXT
    );
    ```
    - Defines different types of analyses that can be performed.
  - **api_keys**:
    ```sql
    CREATE TABLE api_keys (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        api_key VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
    ```
    - Stores API keys for accessing the RESTful API.
  - **users**:
    ```sql
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    );
    ```
    - Stores user information.
  - **logs**:
    ```sql
    CREATE TABLE logs (
        id SERIAL PRIMARY KEY,
        log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        level VARCHAR(10) NOT NULL,
        message TEXT NOT NULL,
        details JSONB
    );
    ```
    - Stores logs for data processing and analysis activities.

### Data Storage and Retrieval
- **Data Insertion**: The Data Recorder Service inserts raw stock data into the `stock_data` table. The Data Analyzer Service inserts analysis results into the `stock_analysis` table.
- **Data Querying**: The Stock Server and API Server retrieve data from the `stock_data` and `stock_analysis` tables using SQL queries.
- **Indexes**: Indexes are used on frequently queried columns to optimize data retrieval, such as `ticker`, `date`, and `analysis_date`.

### Data Backup and Recovery
- **Backup Strategy**: Regular backups of the PostgreSQL database are scheduled to ensure data durability. Backups are stored securely and periodically tested for integrity.
- **Recovery Plan**: In case of data loss or corruption, a recovery plan is in place to restore the database from the latest backup. The recovery plan includes steps for minimizing downtime and data loss.

## Data Analysis

### Analysis Algorithms
- **Moving Averages**: The primary analysis performed by the Data Analyzer Service is the calculation of moving averages (e.g., 5-day and 10-day moving averages). Moving averages are used to smooth out short-term fluctuations and highlight longer-term trends.
  - **Algorithm**:
    ```python
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    ```

### Analysis Metrics
- **MA5 (5-day Moving Average)**: Represents the average closing price of a stock over the last 5 trading days.
- **MA10 (10-day Moving Average)**: Represents the average closing price of a stock over the last 10 trading days.
- **Other Potential Metrics**: Additional metrics such as relative strength index (RSI), exponential moving average (EMA), and Bollinger Bands can be integrated into the analysis pipeline in the future.

### Data Visualization
- **Web Interface**: The Stock Server provides a web interface for visualizing stock data and analysis results. The interface includes tables and charts to present the data in a user-friendly manner.
- **Charts**: Interactive charts are used to display trends and patterns in stock data. These charts are generated using JavaScript libraries like Chart.js or D3.js.
- **Data Tables**: Tabular views of raw stock data and analysis results allow users to sort and filter data based on their preferences.

By completing the Data Management and Data Analysis sections, the StockVision System Design Document now provides a detailed overview of how data is stored, managed, and analyzed within the system. This ensures that all stakeholders have a clear understanding of the system's capabilities and design.


## Testing

### Testing Strategy
The testing strategy for StockVision involves a combination of unit testing, integration testing, and end-to-end testing to ensure the correctness, performance, and reliability of the system. The goal is to identify and resolve issues early in the development process and maintain a high level of quality in the delivered product.

### Test Cases
- **Unit Tests**: Verify the functionality of individual components in isolation.
  - **Data Collector Service**: Test fetching stock data from the Yahoo Finance API.
  - **Data Recorder Service**: Test consuming messages from RabbitMQ and storing data in PostgreSQL.
  - **Data Analyzer Service**: Test retrieving data from PostgreSQL, performing analysis, and storing results.
  - **Stock Server**: Test rendering web pages and retrieving data from PostgreSQL.
  - **API Server**: Test API endpoints for retrieving stock data and analysis results.
  
- **Integration Tests**: Verify the interactions between multiple components.
  - Test the entire data pipeline from data collection, message queuing, data recording, and data analysis.
  - Test the interaction between the Stock Server and the database.
  - Test the interaction between the API Server and the database.
  
- **End-to-End Tests**: Verify the system as a whole.
  - Simulate real-world scenarios and user interactions to ensure the system behaves as expected.
  - Test the full workflow from fetching stock data to displaying it on the web interface and via API endpoints.

### Automated Testing
- **Test Framework**: Use `unittest` for writing and running unit tests. Integration and end-to-end tests can also be written using `unittest` or a framework like `pytest`.
- **Continuous Integration**: Integrate automated tests into the CI/CD pipeline using tools like GitLab CI/CD. Ensure tests are run automatically on code commits and before deployments.
- **Test Coverage**: Use tools like `coverage.py` to measure test coverage and ensure critical parts of the codebase are well-tested.

## Sample Unit Test Case

Here is an example of a unit test case for the API Server using `unittest`:

```python
import unittest
import json
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from api.api_server import create_app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_get_stock_data(self):
        response = self.client.get('/api/stock_data?ticker=AAPL')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:
            self.assertIn('ticker', data[0])
            self.assertIn('date', data[0])
            self.assertIn('open', data[0])
            self.assertIn('high', data[0])
            self.assertIn('low', data[0])
            self.assertIn('close', data[0])
            self.assertIn('volume', data[0])

    def test_get_analysis_results(self):
        response = self.client.get('/api/analysis_results?ticker=AAPL')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:
            self.assertIn('ticker', data[0])
            self.assertIn('analysis_date', data[0])
            self.assertIn('ma5', data[0])
            self.assertIn('ma10', data[0])

if __name__ == '__main__':
    unittest.main()
```

## Conclusion

StockVision is a comprehensive system designed to collect, process, analyze, and visualize stock market data. This system design document outlines the requirements, design decisions, architecture, and components necessary to build and maintain StockVision. 

### Key Points:
- **Modular Architecture**: The system's modular architecture ensures scalability, maintainability, and reliability. Each component handles a specific aspect of the workflow, allowing for independent development and scaling.
- **Robust Data Management**: PostgreSQL is used to store raw stock data and analysis results, ensuring data integrity and efficient querying. Regular backups and a recovery plan safeguard against data loss.
- **Effective Data Analysis**: The Data Analyzer Service performs financial analyses, generating insights that are stored and visualized. The analysis algorithms are designed to highlight trends and patterns in stock data.
- **User-Friendly Interfaces**: The Stock Server provides a web interface for visualizing data, while the API Server offers programmatic access to data and analysis results. Both interfaces are designed to be intuitive and responsive.
- **Comprehensive Testing**: A rigorous testing strategy, including unit, integration, and end-to-end tests, ensures the system's functionality and reliability. Automated testing and continuous integration further enhance the development process.

By following this design, StockVision aims to provide a powerful tool for financial analysts, traders, and investors, offering real-time insights and detailed analysis of stock market data. The system's scalability and flexibility make it well-suited to adapt to future requirements and technological advancements.

