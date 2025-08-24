@echo off
REM Django OAuth Hub - Quick Setup Script for Windows
REM This script helps set up the development environment quickly

echo 🔗 Django OAuth Hub - Quick Setup
echo ==================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is required but not installed.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is required but not installed.
    echo Please install pip and try again.
    pause
    exit /b 1
)

echo ✅ Python found
echo ✅ pip found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
if not exist ".env" (
    echo ⚙️ Creating environment configuration...
    copy .env.example .env
    echo ✅ Created .env file from template
    echo 🔧 Please edit .env file with your OAuth credentials
) else (
    echo ✅ .env file already exists
)

REM Generate encryption key
echo 🔐 Generating secure keys...
python generate_keys.py > keys.txt
echo ✅ Generated secure keys (saved to keys.txt)
echo 🔧 Please add these keys to your .env file

REM Run migrations
echo 🗄️ Setting up database...
python manage.py makemigrations
python manage.py migrate

echo.
echo 🎉 Setup Complete!
echo.
echo Next steps:
echo 1. Edit .env file with your OAuth platform credentials
echo 2. Add the generated keys from keys.txt to your .env file
echo 3. Create a superuser: python manage.py createsuperuser
echo 4. Run the development server: python manage.py runserver
echo.
echo 📖 For detailed instructions, see README.md
echo 🚀 For deployment instructions, see DEPLOYMENT.md
echo.
pause
