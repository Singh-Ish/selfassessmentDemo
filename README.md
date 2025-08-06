# Self Assessment Portal Demo

A Flask-based web application for student self-assessment and peer evaluation based on defined rubrics.

## Features

- **Student Dashboard**: Allow students to submit self-assessments
- **Admin Dashboard**: Administrative interface for managing assessments
- **Dynamic Data Management**: Upload and manage projects, rubrics, and user data via Excel files
- **Email Integration**: Automated email notifications and reminders
- **Role-based Authentication**: Separate access levels for students and administrators
- **Assessment Analytics**: Export assessment results and generate reports

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB (with mongoengine ODM)
- **Frontend**: Bootstrap, jQuery, Jinja2 templates
- **Data Processing**: OpenPyXL (Excel file handling)
- **Authentication**: Flask-Login, itsdangerous
- **Email**: Flask-Mail
- **Admin Interface**: Flask-Admin

## Recent Bug Fixes and Improvements

### Fixed Issues:
1. **Dependency Compatibility**: Updated requirements.txt with compatible package versions
2. **Pandas Compatibility**: Added fallback to OpenPyXL when pandas is unavailable (Python 3.13 compatibility)
3. **Database Connection**: Fixed MongoDB connection issues and added local fallback
4. **Circular Import**: Resolved circular import issues in the application structure
5. **File Path Issues**: Fixed Windows-style path separators causing syntax warnings
6. **Missing Variable**: Fixed undefined `username` variable in authentication flow
7. **Document Model**: Updated mongoengine Document classes to work without flask-mongoengine
8. **Flask Version**: Updated to compatible Flask 2.3.3 and removed deprecated imports

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB (optional - will use local connection if available)

### 1. Clone the Repository
```bash
git clone https://github.com/Singh-Ish/selfassessmentDemo.git
cd selfassessmentDemo
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup (Optional)
The application can work with or without MongoDB:

**With MongoDB (Recommended):**
- Install MongoDB locally
- The application will automatically connect to `mongodb://localhost:27017/assessment`

**Without MongoDB:**
- The application will still run but database features will be limited
- Suitable for testing the UI and basic functionality

### 5. Configure Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
MAIL_SERVER=your-mail-server
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
```

### 6. Run the Application
```bash
python3 main.py
```

The application will start at: http://127.0.0.1:5000

## Default Login Credentials

When the application starts for the first time, it creates default accounts:

**Admin Account:**
- Username: `admin`
- Password: `admin`

**Student Account:**
- Username: `student`
- Password: `student`

## File Structure
```
selfassessmentDemo/
├── main.py                     # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── sapp/                       # Main application package
│   ├── __init__.py            # App initialization
│   ├── models.py              # Database models
│   ├── routes.py              # URL routes and views
│   ├── forms.py               # WTForms form definitions
│   ├── static/                # Static files (CSS, JS, docs)
│   │   ├── css/
│   │   ├── docs/              # Excel file uploads
│   │   └── sampleDocs/        # Sample Excel templates
│   └── templates/             # Jinja2 HTML templates
│       ├── base.html
│       ├── index.html
│       ├── auth/              # Authentication templates
│       ├── dash/              # Dashboard templates
│       └── other/             # Other templates
└── venv/                       # Virtual environment (created during setup)
```

## Usage

### For Students:
1. Log in with student credentials
2. Navigate to the student dashboard
3. Complete self-assessment forms
4. Submit peer evaluations

### For Administrators:
1. Log in with admin credentials
2. Access the admin dashboard
3. Upload Excel files for:
   - User details (`userDetails.xlsx`)
   - Project information (`projectDetails.xlsx`)
   - Rubrics matrix (`rubicsMetrix.xlsx`)
   - Faculty details (`facultyDetails.xlsx`)
4. Monitor assessment progress
5. Export results

## Excel File Formats

Sample Excel files are provided in `sapp/static/sampleDocs/`:

### userDetails.xlsx
Required columns: `userId`, `firstName`, `lastName`, `email`

### projectDetails.xlsx
Required columns: `groupNo`, `title`, `supervisor`, `coSupervisor`, `userId`, `lastName`, `firstName`, `assessmentStatus`

### rubicsMetrix.xlsx
Required columns: `Indicator`, `Level 1: Beginning`, `Level 2: Developing`, `Level 3: Accomplished`, `Level 4: Exemplary`

### facultyDetails.xlsx
Required columns: `lastName`, `firstName`, `email`

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Using Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
```

## Configuration

Key configuration options in `config.py`:

- **Database**: MongoDB connection string
- **Email**: SMTP server settings for notifications
- **File Upload**: Directory for storing uploaded Excel files
- **Security**: Secret key for session management

## Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure virtual environment is activated and all dependencies are installed
2. **Database Connection**: Check MongoDB service status or run without database
3. **Port Conflicts**: Change port in `main.py` if 5000 is occupied
4. **File Upload Issues**: Ensure `sapp/static/docs/` directory exists and is writable

### Debug Mode:
The application runs in debug mode by default. To disable:
```python
app.run(debug=False, host='127.0.0.1', port=5000)
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

GNU General Public License v3.0

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the sample Excel files for proper format

---

**Note**: This application is designed for educational assessment purposes and should be customized according to specific institutional requirements.
