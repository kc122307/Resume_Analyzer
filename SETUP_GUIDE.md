# Setup Guide for AI Resume Intelligence Platform

## Prerequisites

1. Python 3.12 or higher
2. pip (Python package installer)
3. Virtual environment tool (venv)

## Step-by-Step Setup

### 1. Clone or Download the Project

If you haven't already, download the project files to your local machine.

### 2. Create a Virtual Environment

Open a terminal/command prompt and navigate to the project directory:

```bash
cd path/to/ai_resume_analyzer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory with the following content:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
OPENROUTER_API_KEY=your-openrouter-api-key
```

**Important:** Replace the placeholder values with your actual credentials:
- For Cloudinary credentials, sign up at [Cloudinary](https://cloudinary.com/)
- For OpenRouter API key, sign up at [OpenRouter](https://openrouter.ai/)

### 5. Run Database Migrations

Apply the database migrations:

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 7. Run the Development Server

Start the development server:

```bash
python manage.py runserver
```

### 8. Access the Application

Open your web browser and navigate to:

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Using the Application

1. **Sign Up**: Create a new account using the signup page
2. **Log In**: Use your credentials to log in
3. **Upload Resume**: Go to the dashboard and upload your PDF resume
4. **Use AI Tools**:
   - **Analyzer**: Get AI-powered analysis of your resume
   - **Job Matching**: Match your resume against job descriptions
   - **Resume Builder**: Generate a new professional resume
   - **Career Path**: Get personalized career recommendations

## Stopping the Server

To stop the development server, press `Ctrl+C` in the terminal.

To deactivate the virtual environment, run:

```bash
deactivate
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you've activated your virtual environment and installed all dependencies.

2. **Database Errors**: Ensure you've run the migrations with `python manage.py migrate`.

3. **Environment Variables**: Double-check that your `.env` file is correctly configured with valid API keys.

4. **Port Conflicts**: If port 8000 is already in use, you can specify a different port:
   ```bash
   python manage.py runserver 8001
   ```

### Need Help?

If you encounter any issues during setup or usage:

1. Check the console output for error messages
2. Verify all environment variables are correctly set
3. Ensure all dependencies are installed
4. Confirm you're using Python 3.12 or higher

For additional support, refer to the Django documentation or contact the development team.