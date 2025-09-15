# ETL-Airflow Project

A comprehensive Apache Airflow ETL pipeline project built with Astronomer CLI, featuring weather data extraction, transformation, and loading into PostgreSQL database.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [DAGs Description](#dags-description)
- [Database Schema](#database-schema)
- [Commands Reference](#commands-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🌟 Overview

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline using Apache Airflow. The main pipeline extracts weather data from the Open-Meteo API for London, transforms the data into a structured format, and loads it into a PostgreSQL database.

## 📁 Project Structure

```
ETL-Airflow/
├── dags/                           # Airflow DAGs directory
│   ├── etlweather.py              # Main weather ETL pipeline
│   ├── exampledag.py              # Example astronaut DAG
│   └── __pycache__/               # Python cache files
├── include/                        # Additional project files
├── plugins/                        # Custom Airflow plugins
├── tests/                          # Test files
│   └── dags/
│       └── test_dag_example.py    # DAG unit tests
├── airflow_settings.yaml          # Local Airflow connections & variables
├── docker-compose.yml             # PostgreSQL database setup
├── Dockerfile                     # Astro Runtime Docker image
├── packages.txt                   # OS-level packages
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## ✨ Features

- **Weather Data ETL Pipeline**: Automated daily extraction of weather data from Open-Meteo API
- **PostgreSQL Integration**: Structured data storage with automatic table creation
- **Docker Support**: Containerized environment for easy deployment
- **Astronomer CLI**: Professional Airflow development environment
- **TaskFlow API**: Modern Airflow task definition and dependency management
- **Error Handling**: Robust error handling and logging
- **Testing**: Unit tests for DAG validation

## 🔧 Prerequisites

Before running this project, ensure you have the following installed:

- **Docker Desktop**: For containerization
- **Astronomer CLI**: For Airflow development
- **Python 3.8+**: For local development
- **PowerShell**: For Windows terminal commands

### Install Astronomer CLI

```powershell
# Install via PowerShell (Windows)
winget install Astronomer.AstroCLI

# Or via curl
curl -sSL install.astronomer.io | sudo bash -s
```

## 🚀 Installation & Setup

### 1. Clone the Repository

```powershell
git clone <your-repository-url>
cd ETL-Airflow
```

### 2. Initialize Astronomer Project (if not already done)

```powershell
astro dev init
```

### 3. Install Dependencies

The required Python packages are defined in `requirements.txt`:
- `apache-airflow-providers-http`: For API connections
- `apache-airflow-providers-postgres`: For PostgreSQL connections

### 4. Set Up PostgreSQL Database

Start the PostgreSQL container:

```powershell
docker-compose up -d
```

This will create a PostgreSQL instance with:
- **Host**: localhost
- **Port**: 5432
- **Database**: postgres
- **Username**: postgres
- **Password**: postgres

## ⚙️ Configuration

### Airflow Connections

Configure the following connections in `airflow_settings.yaml` or through the Airflow UI:

#### 1. PostgreSQL Connection
- **Connection ID**: `postgres_default`
- **Connection Type**: `postgres`
- **Host**: `host.docker.internal` (for Docker) or `localhost`
- **Database**: `postgres`
- **Username**: `postgres`
- **Password**: `postgres`
- **Port**: `5432`

#### 2. Open-Meteo API Connection
- **Connection ID**: `open_meteo_api`
- **Connection Type**: `http`
- **Host**: `https://api.open-meteo.com`

### Environment Variables

The weather DAG uses the following coordinates (configurable in `etlweather.py`):
- **Latitude**: 51.5074 (London)
- **Longitude**: -0.1278 (London)

## 🏃 Running the Project

### Start Airflow Development Environment

```powershell
# Start all Airflow services
astro dev start

# View logs
astro dev logs

# Restart services (useful after changes)
astro dev restart

# Stop services
astro dev stop
```

### Access Airflow UI

Once started, access the Airflow web interface at:
- **URL**: http://localhost:8080
- **Username**: admin
- **Password**: admin

### Enable and Trigger DAGs

1. Navigate to the Airflow UI
2. Enable the `etl_weather_pipeline` DAG
3. Trigger a manual run or wait for the scheduled execution

## 📊 DAGs Description

### 1. ETL Weather Pipeline (`etlweather.py`)

**Schedule**: Daily (`@daily`)
**Purpose**: Extract, transform, and load weather data

**Tasks**:
1. **extract_weather_data**: Fetches current weather data from Open-Meteo API
2. **transform_weather_data**: Transforms raw API response into structured format
3. **load_weather_data**: Inserts transformed data into PostgreSQL

**Data Points Collected**:
- Latitude/Longitude
- Temperature (°C)
- Wind Speed (km/h)
- Wind Direction (degrees)
- Weather Code
- Timestamp

### 2. Example Astronaut DAG (`exampledag.py`)

**Purpose**: Demonstrates dynamic task mapping with astronaut data from Open Notify API

## 🗄️ Database Schema

The weather data is stored in the `weather_data` table:

```sql
CREATE TABLE weather_data (
    latitude FLOAT,
    longitude FLOAT,
    temperature FLOAT,
    windspeed FLOAT,
    winddirection FLOAT,
    weathercode INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Query Weather Data

```sql
-- Connect to PostgreSQL
psql -h localhost -p 5432 -U postgres -d postgres

-- View recent weather data
SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 10;

-- Average temperature by day
SELECT DATE(timestamp) as date, AVG(temperature) as avg_temp 
FROM weather_data 
GROUP BY DATE(timestamp) 
ORDER BY date DESC;
```

## 📚 Commands Reference

### Astronomer CLI Commands

```powershell
# Project initialization
astro dev init                     # Initialize new Airflow project

# Development
astro dev start                    # Start Airflow locally
astro dev stop                     # Stop local Airflow
astro dev restart                  # Restart Airflow services
astro dev kill                     # Force stop all containers

# Logs and debugging
astro dev logs                     # View all service logs
astro dev logs -f scheduler        # Follow scheduler logs
astro dev logs -f webserver        # Follow webserver logs

# Project management
astro dev parse                    # Parse DAGs for syntax errors
astro dev pytest                  # Run pytest tests
astro deploy                       # Deploy to Astronomer (requires account)
```

### Docker Commands

```powershell
# PostgreSQL database
docker-compose up -d               # Start PostgreSQL container
docker-compose down                # Stop PostgreSQL container
docker-compose logs                # View PostgreSQL logs

# Container management
docker ps                          # List running containers
docker exec -it my_postgres2 psql -U postgres  # Connect to PostgreSQL
```

### Database Commands

```powershell
# Connect to PostgreSQL
docker exec -it my_postgres2 psql -U postgres -d postgres

# Or using psql directly (if installed)
psql -h localhost -p 5432 -U postgres -d postgres
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```powershell
# Check what's using port 8080
netstat -ano | findstr :8080

# Kill process using the port
taskkill /PID <PID_NUMBER> /F
```

#### 2. Database Connection Issues
- Ensure PostgreSQL container is running: `docker ps`
- Check connection settings in Airflow UI
- Verify host is set to `host.docker.internal` for Docker environments

#### 3. DAG Import Errors
```powershell
# Check for syntax errors
astro dev parse

# View scheduler logs
astro dev logs -f scheduler
```

#### 4. API Connection Issues
- Verify internet connectivity
- Check Open-Meteo API status
- Ensure HTTP connection is properly configured

### Logs Location

- **Airflow Logs**: Available through `astro dev logs`
- **Task Logs**: Visible in Airflow UI under each task instance
- **PostgreSQL Logs**: `docker-compose logs`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit changes: `git commit -m "Add feature"`
5. Push to branch: `git push origin feature-name`
6. Submit a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code style
- Add unit tests for new DAGs in the `tests/` directory
- Update documentation for any new features
- Test DAGs locally before submitting

## 📞 Support

- **Astronomer Documentation**: https://www.astronomer.io/docs/
- **Apache Airflow Documentation**: https://airflow.apache.org/docs/
- **Open-Meteo API**: https://open-meteo.com/

---

**Built with ❤️ using Apache Airflow and Astronomer CLI**
