# FYP Project - FastAPI Backend

A FastAPI-based backend application with Prisma ORM and Supabase PostgreSQL database.

## 📋 Project Overview

This is a learning management system (LMS) backend that handles:

- Student management
- Instructor profiles
- Admin accounts
- Course management
- Company/Organization management
- Roadmap generation
- Resume builder
- Invoice and payment tracking

## 🛠️ Technology Stack

### Backend Framework

- **FastAPI** `0.115.0` - Modern, fast web framework for building APIs
- **Uvicorn** `0.32.0` - ASGI server for running FastAPI

### Database & ORM

- **Prisma** `0.15.0` - Next-generation Python ORM
- **Supabase** - PostgreSQL database (cloud-hosted)
- **PostgreSQL** - Relational database

### Data Validation

- **Pydantic** `2.10.0` - Data validation using Python type hints

### Environment & Configuration

- **python-dotenv** `1.0.1` - Environment variable management

## 📦 Environment Requirements

### Python Environment

```
Python Version: 3.12.3
Virtual Environment: .venv (recommended)
Package Manager: pip 24.0
```

### Node.js Environment (for Prisma CLI)

```
Node.js Version: v22.17.1
Prisma CLI: 6.19.2
@prisma/client: 6.19.2
```

### System Requirements

- **OS**: Linux (Ubuntu 20.04+) / macOS / **Windows 10/11 (native or WSL2)**
- **Python**: 3.12.x (3.12.3 tested and recommended)
- **Node.js**: 18.x or higher (v22.17.1 tested)
- **Database**: PostgreSQL 13+ (Supabase hosted)

**✅ Windows Native Support**: This project works on native Windows (PowerShell/CMD) without WSL2. However, WSL2 is recommended for better compatibility with the deployment scripts.

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/fatimaamjad01/FYP-PROJECT.git
cd FYP-PROJECT
```

### 2. Install Python Dependencies

#### Create Virtual Environment

```bash
# Linux/macOS/Windows
python -m venv .venv

# Or on Windows, you might need:
python3 -m venv .venv
# Or if Python is in PATH:
py -m venv .venv
```

#### Activate Virtual Environment

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# Windows (Git Bash)
source .venv/Scripts/activate
```

**Note**: On Windows, if you get a script execution error, run this in PowerShell as Administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies (for Prisma CLI)

```bash
npm install
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Supabase Database Connection
DATABASE_URL="postgresql://postgres.xxxxx:password@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"

# Direct Database Connection (for migrations)
DIRECT_URL="postgresql://postgres.xxxxx:password@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
```

**Note**: Replace the connection strings with your actual Supabase credentials.

### 5. Generate Prisma Client

```bash
# Linux/macOS
.venv/bin/prisma generate

# Windows (PowerShell/CMD)
.venv\Scripts\prisma generate

# Or activate venv first, then just:
prisma generate
```

### 6. Push Database Schema to Supabase

```bash
# Linux/macOS
.venv/bin/prisma db push

# Windows (PowerShell/CMD)
.venv\Scripts\prisma db push

# Or with activated venv:
prisma db push
```

### 7. Run the Application

```bash

# Linux/macOS

.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Windows (PowerShell/CMD)

.venv\Scripts\uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or with activated venv (all platforms):

uvicorn main:app --reload --host 0.0.0.0 --port 8000

```

**Note**: The deploy script (`deploy-to-supabase.sh`) is a bash script and requires WSL2 or Git Bash on Windows.

## 📚 API Endpoints

### Health Check

- `GET /` - Check if API is running

### Student Management

- `POST /students` - Create a new student
- `GET /students` - Get all students

### Documentation

- `GET /docs` - Swagger UI (Interactive API documentation)
- `GET /redoc` - ReDoc (Alternative API documentation)

## 📁 Project Structure

```

FYP-PROJECT/
├── .env # Environment variables (not in git)
├── .gitignore # Git ignore rules
├── .venv/ # Python virtual environment
├── main.py # FastAPI application entry point
├── requirements.txt # Python dependencies
├── package.json # Node.js dependencies (Prisma CLI)
├── package-lock.json # Node.js lock file
├── node_modules/ # Node.js packages
├── prisma/
│ └── schema.prisma # Database schema definition
├── deploy-to-supabase.sh # Deployment script
├── SUPABASE_SETUP.md # Supabase setup guide
└── README.md # This file

```

## 🔧 Development

### Running in Development Mode

```bash
# After activating virtual environment (recommended)
uvicorn main:app --reload

# Or without activating venv:
# Linux/macOS: .venv/bin/uvicorn main:app --reload
# Windows: .venv\Scripts\uvicorn main:app --reload
```

The `--reload` flag enables hot-reloading during development.

### Accessing API Documentation

Once the server is running, visit:

- http://localhost:8000/docs - Interactive Swagger UI
- http://localhost:8000/redoc - Alternative ReDoc UI

### Database Management

#### View Current Schema

```bash
# With activated venv (all platforms)
prisma db pull

# Or: .venv/bin/prisma (Linux/macOS) or .venv\Scripts\prisma (Windows)
```

#### Push Schema Changes

```bash
# With activated venv (all platforms)
prisma db push
```

#### Reset Database (⚠️ Destructive)

```bash
# With activated venv (all platforms)
prisma db push --force-reset
```

## 📝 Database Models

The application includes the following models:

1. **Student** - Student accounts and profiles
2. **Instructor** - Instructor accounts and expertise
3. **Admin** - Administrative accounts
4. **Course** - Course catalog and content
5. **Company** - Organization/company accounts
6. **Roadmap** - Learning path management
7. **Resume** - Resume builder data
8. **Invoice** - Payment and billing records
9. **CourseCategory** - Course categorization

See `prisma/schema.prisma` for complete schema definitions.

## 🔐 Security Notes

- Never commit `.env` file to version control
- Store sensitive credentials in environment variables
- Use strong passwords for database connections
- Enable SSL for production database connections
- Implement proper authentication before deploying to production

## 🐛 Troubleshooting

### Virtual Environment Not Found

```bash
# Create venv
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Prisma Client Not Generated

```bash
# With activated venv
prisma generate

# Or direct call:
# Linux/macOS: .venv/bin/prisma generate
# Windows: .venv\Scripts\prisma generate
```

### PowerShell Execution Policy Error (Windows)

If you see "cannot be loaded because running scripts is disabled":

```powershell
# Run in PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Database Connection Errors

1. Check `.env` file has correct credentials
2. Verify Supabase project is active
3. Ensure IP address is whitelisted in Supabase
4. Test connection string format

### Port Already in Use

```bash
# Linux/macOS - Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Or just use a different port (all platforms)
uvicorn main:app --reload --port 8001
```

## 📦 Dependency Management

### Update All Dependencies

```bash
# Python packages
pip list --outdated
pip install --upgrade -r requirements.txt

# Node.js packages
npm outdated
npm update
```

### Add New Python Dependency

```bash
pip install package-name
pip freeze > requirements.txt
```

### Add New Node.js Dependency

```bash
npm install package-name
```

## 🚢 Deployment

See `SUPABASE_SETUP.md` for Supabase deployment instructions.

## 👥 Contributors

- Fatima Amjad (@fatimaamjad01)
- Waqar (Developer)

## 📄 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

For issues and questions:

- Create an issue on GitHub
- Contact: [Add contact information]

---

**Last Updated**: January 26, 2026
**Python Version**: 3.12.3
**FastAPI Version**: 0.115.0
**Prisma Version**: 0.15.0
