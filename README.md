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

- **OS**: Linux (Ubuntu 20.04+ recommended) / macOS / Windows with WSL2
- **Python**: 3.12.x (3.12.3 tested)
- **Node.js**: 18.x or higher (v22.17.1 tested)
- **Database**: PostgreSQL 13+ (Supabase hosted)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/fatimaamjad01/FYP-PROJECT.git
cd FYP-PROJECT
```

### 2. Install Python Dependencies

#### Create Virtual Environment

```bash
python -m venv .venv
```

#### Activate Virtual Environment

```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
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
.venv/bin/prisma generate
```

### 6. Push Database Schema to Supabase

```bash
.venv/bin/prisma db push
```

### 7. Run the Application

```bash
.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the deploy script:

```bash
chmod +x deploy-to-supabase.sh
./deploy-to-supabase.sh
```

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
├── .env                    # Environment variables (not in git)
├── .gitignore              # Git ignore rules
├── .venv/                  # Python virtual environment
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies (Prisma CLI)
├── package-lock.json       # Node.js lock file
├── node_modules/           # Node.js packages
├── prisma/
│   └── schema.prisma       # Database schema definition
├── deploy-to-supabase.sh   # Deployment script
├── SUPABASE_SETUP.md       # Supabase setup guide
└── README.md               # This file
```

## 🔧 Development

### Running in Development Mode

```bash
.venv/bin/uvicorn main:app --reload
```

The `--reload` flag enables hot-reloading during development.

### Accessing API Documentation

Once the server is running, visit:

- http://localhost:8000/docs - Interactive Swagger UI
- http://localhost:8000/redoc - Alternative ReDoc UI

### Database Management

#### View Current Schema

```bash
.venv/bin/prisma db pull
```

#### Push Schema Changes

```bash
.venv/bin/prisma db push
```

#### Reset Database (⚠️ Destructive)

```bash
.venv/bin/prisma db push --force-reset
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
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Prisma Client Not Generated

```bash
.venv/bin/prisma generate
```

### Database Connection Errors

1. Check `.env` file has correct credentials
2. Verify Supabase project is active
3. Ensure IP address is whitelisted in Supabase
4. Test connection string format

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
.venv/bin/uvicorn main:app --reload --port 8001
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
