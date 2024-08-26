# FYP-Smart-Grid
Smart Hybrid Nano Grid to Enable Real Time Power Sharing (Language – Python, Controller – Raspberry Pi)

This repository contains the code for a power management system that includes battery monitoring, data logging, and device control using Raspberry Pi, INA219, and other components. The system uses SQLAlchemy for database interactions and GPIO for controlling hardware components.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Modules](#modules)
  - [DeviceMeasurements](#devicemeasurements)
  - [DataService](#dataservice)
  - [DBService](#dbservice)
  - [HistoryData](#historydata)

## Project Overview
This project aims to monitor and manage the power usage of a system using various sensors and a battery management module. The data collected is logged into a database for further analysis.

## Features
- **Battery Monitoring**: Measure and log battery voltage and current.
- **Data Logging**: Store power usage data in a MariaDB database.
- **Device Control**: Control relays and other hardware components based on power requirements.
- **Real-time Data Display**: Show real-time data on an LCD connected to the Raspberry Pi.

## Setup
### Prerequisites
- Raspberry Pi with Raspbian OS
- Python 3.x
- MariaDB Server
- Required Python packages:
  - `RPi.GPIO`
  - `minimalmodbus`
  - `smbus`
  - `ina219`
  - `sqlalchemy`
  - `pytz`

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/fyp-project.git
    cd fyp-project
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the MariaDB database:
    - Create a database named `fyp_prjct`.
    - Update the `create_engine` connection string in the code with your MariaDB credentials.

4. Run the initial database migration:
    ```bash
    python -c 'from your_module import Base, engine; Base.metadata.create_all(engine)'
    ```

## Usage
1. **Running the Data Logger**:
    - Execute the main script to start logging data and controlling devices.
    ```bash
    python main.py
    ```

2. **Viewing Logs**:
    - Logs and data are stored in the `history_data` table in the MariaDB database.

## Modules

### DeviceMeasurements
Handles the reading of measurements from sensors like INA219 and manages GPIO pins for controlling relays.

### DataService
Provides methods for calculating power requirements, adding new data to the database, and determining the current time slot.

### DBService
Interacts with the MariaDB database to retrieve and store historical power usage data.

### HistoryData
Defines the SQLAlchemy model for the `history_data` table, which stores historical records of power usage.


