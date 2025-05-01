# Rentoo - Property Management System

A FastAPI-based property management system that allows owners to manage their properties and tenants.

## Features

- Owner management
- Property management (up to 5 properties per owner)
- Unique property names per owner
- MySQL database integration
- RESTful API endpoints

## Prerequisites

- Python 3.9 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rentoo.git
cd rentoo
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
   - Create a MySQL database named `rentoo`
   - Run the migration scripts in order:
```bash
mysql -u your_username -p rentoo < src/main/resources/db/migration/V1__create_rentoo_tables.sql
mysql -u your_username -p rentoo < src/main/resources/db/migration/V2__add_property_name.sql
```

5. Configure environment variables:
   Create a `.env` file in the project root with the following content:
```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=rentoo
DB_PORT=3306
```

## Running the Application

1. Start the FastAPI server:
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080 --reload
```

2. Access the API documentation:
   - Open your browser and go to: http://localhost:8080/docs

## API Endpoints

### Owners
- `POST /owners/` - Create a new owner
- Request body:
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
}
```

### Properties
- `POST /properties/` - Create a new property
- Request body:
```json
{
    "owner_id": 1,
    "property_name": "Downtown Apartment",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "monthly_rent": 2000.00,
    "status": "VACANT"
}
```

## Development

### Project Structure
```
rentoo/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── run.py
│   └── main/
│       └── resources/
│           └── db/
│               └── migration/
│                   ├── V1__create_rentoo_tables.sql
│                   └── V2__add_property_name.sql
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Running Tests
```bash
python -m pytest
```

## Deployment

### AWS Deployment
1. Create an EC2 instance
2. Install required dependencies:
```bash
sudo apt update
sudo apt install python3 python3-pip mysql-server
```

3. Clone the repository and follow the installation steps above

4. Configure MySQL:
```bash
sudo mysql_secure_installation
```

5. Create the database and run migrations

6. Start the application using a process manager like PM2:
```bash
pm2 start "python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080" --name rentoo
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 