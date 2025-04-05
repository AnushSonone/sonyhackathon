# Smart Dual-Line Entry System

## Overview

The Smart Dual-Line Entry System is an innovative solution designed to ease congestion in transportation hubs by using real-time data, facial recognition, and dynamic signage to create efficient and flexible queues for locals and tourists. The system intelligently adjusts lines to improve the overall travel experience, ensuring locals are prioritized during peak times while tourists are efficiently managed to prevent overcrowding.

## Key Features

- **Real-Time Data Processing**: The system uses edge AI visual sensors to monitor real-time data of individuals in the transportation hub.
- **Dynamic Signage**: Signage changes color (red, yellow, green) based on whether the individual is a local or a tourist.
- **Facial Recognition & ID Integration**: Locals are identified via facial recognition, with the option to use an ID if facial recognition fails.
- **Efficient Queue Management**: In peak times, a dedicated line is reserved for locals. If there are fewer locals, the system adjusts and opens the general line for all passengers to optimize the flow.
- **Scalable and Secure Architecture**: The system uses scalable cloud solutions (e.g., Firebase or S3 buckets) to securely store local data, ensuring the solution grows with future demand.

## Architecture Overview

The system uses the following components:

1. **Edge AI Sensors**: Capture video feeds and process them in real-time to identify locals and tourists.
2. **Local and Tourist Queue Management**: Dynamically adjusts the flow based on the number of locals and the congestion level.
3. **Real-Time Signage**: Display instructions on the queue flow, changing colors based on conditions.
4. **Cloud Database**: A cloud database stores local information, ensuring scalability, security, and redundancy.

### Database Solutions:

- **ScyllaDB / DynamoDB** for fast, distributed database management.
- **S3 Buckets** for storing metadata and large files (e.g., images).

### Data Flow:

1. **Camera Feed**: Edge AI sensors send real-time data to the system.
2. **Identification**: The system determines if the individual is a local (via facial recognition) or a tourist.
3. **Queue Assignment**: Based on the individual’s status, they are routed to the appropriate line (local or tourist).
4. **Signage Update**: The signage displays directions or warnings (e.g., yellow if a tourist is in the wrong line).
5. **Cloud Sync**: Data is securely stored in the cloud for future analysis and scalability.

## Getting Started

### Prerequisites

- **Python 3.x**
- **FastAPI** for the backend
- **Socket.io** for real-time communication
- **ScyllaDB / DynamoDB** (or another scalable database)
- **TensorFlow / OpenCV** for facial recognition (if used locally)
- **Firebase** or **AWS S3** for cloud storage (if applicable)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/smart-dual-line-entry-system.git
   cd smart-dual-line-entry-system
   ```
2. Set up virtual env (optional)
   ```
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```
3. Install required dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables (e.g., for cloud storage credentials, API keys, etc.). Use .env file if required.

### Scalability & Security

The system is designed to scale horizontally with cloud-based storage (e.g., S3 or Firebase) to ensure that the database can handle large datasets of local information.

- ScyllaDB or DynamoDB provide high availability and reliability for storing local data in real-time.

- End-to-End Encryption ensures that personal data (facial recognition and local information) is securely transmitted and stored.

- API Rate Limiting & Authentication to ensure secure access to the backend and prevent unauthorized access.

### Future Enhancements

- Cloud Migration: Transitioning from local database storage to fully cloud-based solutions (e.g., Firebase, AWS S3, DynamoDB) for increased scalability.

- Machine Learning Models: Use advanced machine learning models for more accurate facial recognition and behavior prediction.

- Real-Time Analytics: Introduce analytics dashboards for transportation agencies to track queue efficiency and congestion patterns.

- Mobile App Integration: Develop a mobile application that allows users to check real-time data, view signage, and get notified of any changes.
