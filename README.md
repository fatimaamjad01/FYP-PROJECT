# FYP Project - GraphQL API Backend

Modern GraphQL API built with **FastAPI**, **Strawberry GraphQL**, **Prisma ORM**, and **Supabase PostgreSQL**.

## 📋 Overview

Learning Management System (LMS) backend with Student management, Instructor profiles, Admin accounts, Course management, and more.

## 🛠️ Tech Stack

- **FastAPI** `0.115.0` + **Uvicorn** `0.32.0` - Web framework & ASGI server
- **Strawberry GraphQL** `0.289.8` - GraphQL library with type hints
- **Prisma** `0.15.0` - Type-safe ORM
- **Supabase** - PostgreSQL database (hosted)
- **Pydantic** `2.10.0` - Data validation
- **bcrypt** `5.0.0` - Password hashing

## 📦 Requirements

- **Python**: 3.12.3
- **Node.js**: 18.x+ (for Prisma CLI)
- **OS**: Linux / macOS / Windows (native or WSL2)

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/fatimaamjad01/FYP-PROJECT.git

# 2. Navigate to project root folder
cd FYP-PROJECT

# 3. Create virtual environment
python -m venv .venv

# 4. Activate virtual environment
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\Activate.ps1         # Windows PowerShell

# 5. Install dependencies
pip install -r requirements.txt
npm install

# 6. Create .env file with your Supabase credentials
# DATABASE_URL="postgresql://..."
# DIRECT_URL="postgresql://..."

# 7. Setup database
prisma generate
prisma db push

# 8. Run server
uvicorn main:app --reload

# 9. Open GraphQL Playground
# Visit: http://localhost:8000/graphql
```

**Windows Note**: If script execution error occurs, run in PowerShell as Admin:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📂 Navigation

To navigate to the project root folder, use these commands:

**If you haven't cloned the repository yet:**
```bash
git clone https://github.com/fatimaamjad01/FYP-PROJECT.git
cd FYP-PROJECT
```

**If you're already in a subdirectory of the project:**
```bash
# Navigate to project root from any subdirectory
cd /path/to/FYP-PROJECT

# Or use relative path to go up directories
cd ..              # Go up one directory
cd ../..           # Go up two directories
```

**To verify you're in the project root:**
```bash
pwd                # Print current directory (Linux/macOS)
cd                 # Print current directory (Windows CMD)
ls                 # List files (should see main.py, README.md, etc.)
```

## 📚 GraphQL API

**Endpoint**: `http://localhost:8000/graphql`

### Example Queries

```graphql
# Get all students
query {
  listStudents {
    id
    firstName
    lastName
    email
  }
}

# Get specific student
query {
  getStudent(id: "1") {
    id
    firstName
    email
    bio
  }
}
```

### Example Mutations

```graphql
# Register student
mutation {
  registerStudent(
    input: {
      firstName: "John"
      lastName: "Doe"
      email: "john@example.com"
      password: "SecurePass123"
    }
  ) {
    id
    email
  }
}

# Update student
mutation {
  updateStudent(
    id: 1
    input: {
      firstName: "Jane"
      lastName: "Smith"
      email: "jane@example.com"
      password: "NewPass456"
    }
  ) {
    id
    email
  }
}
```

## 📁 Project Structure

```
FYP-PROJECT/
├── main.py                 # FastAPI app + GraphQL router
├── schema.py               # GraphQL schema (types, queries, mutations)
├── prisma/schema.prisma    # Database models
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── package.json            # Node.js dependencies (Prisma CLI)
```

## 📝 Database Models

**Implemented**: Student (with GraphQL queries/mutations)  
**Available**: Instructor, Admin, Course, Company, Roadmap, Resume, Invoice, CourseCategory

See `prisma/schema.prisma` and `schema.py` for details.

## 🔐 Security

- ✅ Password hashing (bcrypt)
- ✅ Email validation
- ✅ Password requirements (8+ chars)
- ⚠️ TODO: JWT authentication, rate limiting, CORS

## 🐛 Troubleshooting

**Port in use:**

```bash
lsof -ti:8000 | xargs kill -9                    # Linux/macOS
netstat -ano | findstr :8000                     # Windows (find PID)
taskkill /PID <PID_NUMBER> /F                    # Windows (kill)
# Or use different port: uvicorn main:app --reload --port 8001
```

**Module not found:**

```bash
pip install -r requirements.txt
```

**Prisma client not generated:**

```bash
prisma generate
```

**Database connection error:**

- Check `.env` credentials
- Verify Supabase project is active
- Whitelist your IP in Supabase

**Windows script error:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 👥 Contributors

Fatima Amjad (@fatimaamjad01) • Waqar (Developer)

---

**Last Updated**: January 30, 2026 • **Python**: 3.12.3 • **FastAPI**: 0.115.0 • **Strawberry**: 0.289.8 • **Prisma**: 0.15.0
