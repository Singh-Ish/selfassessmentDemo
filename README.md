# Self Assessment Portal

A Flask-based web application for student self-assessment and peer evaluation based on defined rubrics.

## Features

- **Student Dashboard**: Allow students to submit self-assessments
- **Admin Dashboard**: Administrative interface for managing assessments
- **Dynamic Data Management**: Upload and manage projects, rubrics, and user data via Excel files
- **Email Integration**: Automated email notifications and reminders
- **Role-based Authentication**: Separate access levels for students and administrators
- **Assessment Analytics**: Export assessment results and generate reports
- **Local MongoDB Database**: Uses local MongoDB with Docker for data persistence
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB (with mongoengine ODM)
- **Frontend**: Bootstrap, jQuery, Jinja2 templates
- **Data Processing**: OpenPyXL (Excel file handling)
- **Authentication**: Flask-Login, itsdangerous
- **Email**: Flask-Mail
- **Containerization**: Docker & Docker Compose

## Quick Start

### 🚀 **First Time Setup (Recommended - Docker)**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Singh-Ish/selfassessmentDemo.git
   cd selfassessmentDemo
   ```

2. **Run the Automated Setup**

   ```bash
   ./migrate_and_setup.sh
   ```

   Choose option 2 (Start local MongoDB only) for first-time setup.

3. **Initialize Sample Data** (Optional but recommended)

   ```bash
   source newenv/bin/activate
   python3 init_sample_data.py
   ```

4. **Access the Application**
   - **Web Application**: http://localhost:5002
   - **MongoDB Admin**: http://localhost:8081 (admin/admin123)

### ⚡ **Subsequent Runs**

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart
```

## Manual Setup Options

### Option 1: Docker Development (Recommended)

**Prerequisites:**

- Docker
- Docker Compose

**First Time Setup:**

```bash
# 1. Clone and enter directory
git clone https://github.com/Singh-Ish/selfassessmentDemo.git
cd selfassessmentDemo

# 2. Build and start services
docker-compose up -d

# 3. Initialize sample data (optional)
source newenv/bin/activate
python3 init_sample_data.py
```

**Daily Usage:**

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View application logs
docker-compose logs web -f

# View all logs
docker-compose logs -f
```

### Option 2: Local Development

**Prerequisites:**

- Python 3.8+
- MongoDB (optional)

**First Time Setup:**

```bash
# 1. Clone repository
git clone https://github.com/Singh-Ish/selfassessmentDemo.git
cd selfassessmentDemo

# 2. Create virtual environment
python3 -m venv newenv
source newenv/bin/activate  # On Windows: newenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file (optional)
cp .env.example .env
# Edit .env with your settings

# 5. Run application
python3 main.py
```

**Daily Usage:**

```bash
# Activate virtual environment
source newenv/bin/activate

# Start application
python3 main.py
```

### Option 3: Production Docker

**First Time Setup:**

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d
```

## Default Login Credentials

The application comes with pre-configured test accounts:

| Role    | Username    | Password      | Description          |
| ------- | ----------- | ------------- | -------------------- |
| Admin   | `admin`     | `admin`       | Full admin access    |
| Student | `student`   | `student`     | Basic student access |
| Student | `johndoe`   | `password123` | Test student 1       |
| Student | `janesmith` | `password123` | Test student 2       |

## Available Services

When running with Docker, these services are available:

| Service         | URL                   | Description       | Credentials      |
| --------------- | --------------------- | ----------------- | ---------------- |
| Web Application | http://localhost:5002 | Main application  | See table above  |
| MongoDB         | localhost:27017       | Database          | No auth required |
| MongoDB Express | http://localhost:8081 | Database admin UI | admin/admin123   |

## Useful Scripts

The project includes several helper scripts:

### `setup.sh` - Interactive Setup

```bash
./setup.sh
```

Choose from:

1. Local development setup
2. Docker development setup
3. Production Docker setup

### `migrate_and_setup.sh` - Database Migration

```bash
./migrate_and_setup.sh
```

Choose from:

1. Start local MongoDB and migrate from remote
2. Start local MongoDB only
3. Stop all services

### `init_sample_data.py` - Sample Data

```bash
python3 init_sample_data.py
```

Populates the database with test data for development.

## Database Management

### Connecting to MongoDB

```bash
# Via Docker container
docker exec -it self_assessment_mongo mongosh assessment

# Direct connection (if MongoDB is running locally)
mongosh mongodb://localhost:27017/assessment
```

### Viewing Data

```bash
# List all users
docker exec self_assessment_mongo mongosh assessment --eval "db.user.find()"

# List all projects
docker exec self_assessment_mongo mongosh assessment --eval "db.projects.find()"

# Database statistics
docker exec self_assessment_mongo mongosh assessment --eval "db.stats()"
```

### Backup and Restore

```bash
# Backup database
docker exec self_assessment_mongo mongodump --db assessment --out /data/backup

# Restore database
docker exec self_assessment_mongo mongorestore --db assessment /data/backup/assessment
```

## Project Structure

```
selfassessmentDemo/
├── main.py                     # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── setup.sh                    # Interactive setup script
├── migrate_and_setup.sh       # Database migration script
├── init_sample_data.py         # Sample data initialization
├── migrate_db.py              # Database migration utility
├── docker-compose.yml         # Docker development setup
├── docker-compose.prod.yml    # Docker production setup
├── Dockerfile                 # Docker image (development)
├── Dockerfile.prod            # Docker image (production)
├── .dockerignore              # Docker build ignore rules
├── .env.example               # Environment variables template
├── sapp/                      # Main application package
│   ├── __init__.py           # App initialization
│   ├── models.py             # Database models
│   ├── routes.py             # URL routes and views
│   ├── forms.py              # WTForms form definitions
│   ├── static/               # Static files (CSS, JS, docs)
│   │   ├── css/
│   │   ├── docs/             # Excel file uploads
│   │   └── sampleDocs/       # Sample Excel templates
│   └── templates/            # Jinja2 HTML templates
│       ├── base.html
│       ├── index.html
│       ├── auth/             # Authentication templates
│       ├── dash/             # Dashboard templates
│       └── other/            # Other templates
├── docker/                   # Docker configuration
│   └── mongodb/
│       └── init/            # MongoDB initialization scripts
└── newenv/                  # Python virtual environment
```

## Application Features

### For Students:

1. **Login** with student credentials
2. **View Project Details** - See assigned projects and group members
3. **Complete Self-Assessment** - Evaluate yourself and peers using rubrics
4. **Submit Feedback** - Provide comments and suggestions
5. **Track Status** - Monitor assessment completion

### For Administrators:

1. **Dashboard Overview** - Monitor assessment progress across all students
2. **User Management** - View and manage student accounts
3. **Project Management** - Upload and manage project assignments
4. **Assessment Status** - Track who has completed assessments
5. **Data Export** - Export results to Excel files
6. **Email Notifications** - Send reminders to students
7. **Database Administration** - Manage all application data

## Excel File Upload Formats

Sample Excel files are provided in `sapp/static/sampleDocs/`:

### userDetails.xlsx

| Column    | Description           | Required |
| --------- | --------------------- | -------- |
| userId    | Unique student ID     | Yes      |
| firstName | Student first name    | Yes      |
| lastName  | Student last name     | Yes      |
| email     | Student email address | Yes      |

### projectDetails.xlsx

| Column           | Description            | Required |
| ---------------- | ---------------------- | -------- |
| groupNo          | Project group number   | Yes      |
| title            | Project title          | Yes      |
| supervisor       | Faculty supervisor     | Yes      |
| coSupervisor     | Co-supervisor (if any) | No       |
| userId           | Student ID             | Yes      |
| lastName         | Student last name      | Yes      |
| firstName        | Student first name     | Yes      |
| assessmentStatus | 0=Pending, 1=Complete  | Yes      |

### rubicsMetrix.xlsx

| Column                | Description              | Required |
| --------------------- | ------------------------ | -------- |
| Indicator             | Assessment criteria name | Yes      |
| Level 1: Beginning    | Description for level 1  | Yes      |
| Level 2: Developing   | Description for level 2  | Yes      |
| Level 3: Accomplished | Description for level 3  | Yes      |
| Level 4: Exemplary    | Description for level 4  | Yes      |

### facultyDetails.xlsx

| Column    | Description           | Required |
| --------- | --------------------- | -------- |
| lastName  | Faculty last name     | Yes      |
| firstName | Faculty first name    | Yes      |
| email     | Faculty email address | Yes      |

## Environment Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Key environment variables:

```env
# Application settings
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database settings (choose one)
# Local MongoDB (recommended for development)
MONGODB_URI=mongodb://localhost:27017/assessment
# Docker MongoDB
# MONGODB_URI=mongodb://mongodb:27017/assessment
# Remote MongoDB Atlas
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/assessment

# Email settings (optional)
MAIL_SERVER=your-mail-server.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

## Troubleshooting

### Common Issues:

**Port Already in Use:**

```bash
# Check what's using the port
lsof -i :5002

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
```

**Docker Issues:**

```bash
# Rebuild containers
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v

# View detailed logs
docker-compose logs web --tail=50
```

**Database Connection Issues:**

```bash
# Check MongoDB container status
docker-compose ps mongodb

# View MongoDB logs
docker-compose logs mongodb

# Connect directly to MongoDB
docker exec -it self_assessment_mongo mongosh
```

**Permission Issues:**

```bash
# Fix script permissions
chmod +x setup.sh migrate_and_setup.sh init_sample_data.py

# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
```

**Python Environment Issues:**

```bash
# Recreate virtual environment
rm -rf newenv
python3 -m venv newenv
source newenv/bin/activate
pip install -r requirements.txt
```

### Debug Mode:

Enable detailed logging by setting environment variables:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
```

## Performance and Scaling

### Resource Requirements:

- **Development**: 2GB RAM, 1 CPU core
- **Production**: 4GB RAM, 2 CPU cores
- **Storage**: 1GB for application, 5GB for database

### Scaling Options:

1. **Horizontal Scaling**: Multiple Flask workers with load balancer
2. **Database Scaling**: MongoDB replica sets or sharding
3. **Caching**: Redis for session storage and caching

## Security Considerations

### Production Deployment:

1. **Change Default Passwords**: Update all default login credentials
2. **Environment Variables**: Use secure secret keys and database passwords
3. **HTTPS**: Configure SSL/TLS certificates
4. **Database Security**: Enable MongoDB authentication
5. **Firewall**: Restrict access to necessary ports only

### Security Headers:

The application includes basic security measures. For production, consider:

- Content Security Policy (CSP)
- HTTP Strict Transport Security (HSTS)
- X-Frame-Options
- X-Content-Type-Options

## Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Make** your changes and test thoroughly
4. **Commit** changes: `git commit -am 'Add feature description'`
5. **Push** to branch: `git push origin feature-name`
6. **Submit** a pull request

### Development Guidelines:

- Follow PEP 8 Python style guide
- Add tests for new features
- Update documentation
- Test with both Docker and local development

## License

GNU General Public License v3.0

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation.

## Support

For issues and questions:

📧 **Email**: ishdeep.711@gmail.com
🐛 **Bug Reports**: Create an issue on GitHub
📖 **Documentation**: Check this README and inline code comments
💬 **Discussions**: Use GitHub Discussions for questions

---

**Note**: This application is designed for educational assessment purposes and should be customized according to specific institutional requirements.

### Quick Reference Commands

```bash
# First time setup (Docker)
./migrate_and_setup.sh

# Daily usage
docker-compose up -d    # Start
docker-compose down     # Stop
docker-compose logs -f  # View logs

# Development
source newenv/bin/activate  # Activate Python environment
python3 main.py            # Run locally

# Database management
python3 init_sample_data.py                    # Add sample data
docker exec -it self_assessment_mongo mongosh  # MongoDB shell
```
