
# AI Resume Intelligence Platform

A comprehensive Django-based platform that leverages AI to analyze resumes, match jobs, build professional resumes, and provide career path recommendations.

## Features

- **User Authentication**: Secure signup, login, and logout functionality
- **Resume Management**: Upload and store resumes securely using Cloudinary
- **AI-Powered Analysis**: Get detailed feedback on your resume's ATS compatibility
- **Job Matching**: Match your resume against job descriptions
- **Resume Builder**: Generate professional resumes tailored to specific roles
- **Career Path Planning**: Receive personalized career recommendations
- **Responsive UI**: Mobile-friendly interface built with TailwindCSS

## Prerequisites

- Python 3.12+
- Django 6.0
- Cloudinary Account
- OpenRouter API Key

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai_resume_analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your actual credentials:
   - **Cloudinary Credentials**: Sign up at [Cloudinary](https://cloudinary.com/users/register_free)
   - **OpenRouter API Key**: Get your key at [OpenRouter](https://openrouter.ai/keys)

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## API Key Configuration

To enable all AI-powered features, you must configure the following API keys in your `.env` file:

### Cloudinary Configuration
1. Sign up for a free account at [Cloudinary](https://cloudinary.com/users/register_free)
2. Navigate to your Dashboard to find your credentials
3. Update the following values in `.env`:
   ```
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

### OpenRouter API Configuration
1. Sign up for an account at [OpenRouter](https://openrouter.ai/)
2. Navigate to the [API Keys](https://openrouter.ai/keys) page
3. Create a new API key
4. Update the following value in `.env`:
   ```
   OPENROUTER_API_KEY=your-openrouter-api-key
   ```

## Usage Guide

1. **Sign Up**: Create a new account
2. **Upload Resume**: Upload your PDF resume
3. **Analyze Resume**: Get AI-powered feedback on your resume
4. **Match Jobs**: Compare your resume against job descriptions
5. **Build Resume**: Generate a professional resume for specific roles
6. **Plan Career**: Receive personalized career path recommendations

## Privacy & Data Handling

We prioritize your privacy:
- Only user account data and resume Cloudinary URLs are stored
- Job details, job analysis results, AI-generated resumes, and career path outputs are never saved
- All AI operations are temporary and stateless

## Technology Stack

- **Backend**: Django 6.0 + Python 3.12
- **Database**: SQLite
- **Storage**: Cloudinary for resume file handling
- **AI Integration**: OpenRouter API with free-tier models (Llama/Mistral/Claude)
- **Frontend**: HTML, TailwindCSS, Vanilla JavaScript
- **PDF Processing**: PyPDF2 for text extraction

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
=======
# Resume_Analyzer
>>>>>>> 3b193869072d22058ea2c17f169fb2efa7a19ae8
