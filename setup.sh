 #!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed. Please install MySQL and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit the .env file with your database credentials."
fi

# Create database and run migrations
echo "Setting up database..."
read -p "Enter MySQL root password: " mysql_password
mysql -u root -p"$mysql_password" -e "CREATE DATABASE IF NOT EXISTS rentoo;"
mysql -u root -p"$mysql_password" rentoo < src/main/resources/db/migration/V1__create_rentoo_tables.sql
mysql -u root -p"$mysql_password" rentoo < src/main/resources/db/migration/V2__add_property_name.sql

echo "Setup complete! You can now run the application using:"
echo "source venv/bin/activate"
echo "python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080 --reload"