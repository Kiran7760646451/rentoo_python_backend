@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Check if MySQL is installed
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo MySQL is not installed. Please install MySQL and try again.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit the .env file with your database credentials.
)

REM Create database and run migrations
echo Setting up database...
set /p mysql_password=Enter MySQL root password: 
mysql -u root -p%mysql_password% -e "CREATE DATABASE IF NOT EXISTS rentoo;"
mysql -u root -p%mysql_password% rentoo < src\main\resources\db\migration\V1__create_rentoo_tables.sql
mysql -u root -p%mysql_password% rentoo < src\main\resources\db\migration\V2__add_property_name.sql

echo Setup complete! You can now run the application using:
echo venv\Scripts\activate
echo python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080 --reload 