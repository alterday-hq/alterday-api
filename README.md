# Project Name

Short description of what the app does.

## Requirements

- Python 3.10+

## Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-user/your-project.git
cd your-project
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
```
Open `.env` and fill in the required values.

**5. Run the app**
```bash
uvicorn app.main:app --reload
```

App is running at: http://127.0.0.1:8000

## API Docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc