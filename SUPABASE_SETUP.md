# Supabase Setup Guide

## Step 1: Get your Supabase Connection String

1. Go to your Supabase project dashboard
2. Click on "Project Settings" (gear icon)
3. Navigate to "Database" section
4. Find "Connection string" and select "URI"
5. Copy the connection string (it looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

## Step 2: Create .env file

Create a `.env` file in the project root with your connection string:

```bash
DATABASE_URL="postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres"
```

**Replace:**

- `your-password` with your actual database password
- `your-project-ref` with your project reference ID

## Step 3: Install Python dependencies

Using `uv` (recommended for faster installation):

```bash
uv pip install -r requirements.txt
```

Or using pip:

```bash
pip install -r requirements.txt
```

## Step 4: Generate Prisma Client

```bash
prisma generate
```

## Step 5: Push schema to Supabase

This will create the tables in your Supabase database:

```bash
prisma db push
```

## Step 6: Run your application

```bash
uvicorn main:app --reload
```

Your API will be available at: http://localhost:8000

## API Endpoints

- GET `/` - Health check
- POST `/students` - Create a new student
- GET `/students` - Get all students

## Troubleshooting

If you get connection errors:

1. Make sure your IP is whitelisted in Supabase (Project Settings > Database > Connection pooling)
2. Verify your DATABASE_URL is correct
3. Check that your database password is correct
