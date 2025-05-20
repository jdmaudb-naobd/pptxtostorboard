@echo off
echo Setting up PowerPoint Extractor environment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"

REM Download spaCy model
echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo Setup complete! Launching application...
python gui.py 