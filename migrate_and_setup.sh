#!/bin/bash

# MongoDB Migration and Local Setup Script

set -e

echo "🗄️  MongoDB Migration to Local Database"
echo "======================================"

# Check if Python3 and required packages are available
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if Docker is available
if ! command -v docker >/dev/null 2>&1 || ! command -v docker-compose >/dev/null 2>&1; then
    echo "❌ Docker or Docker Compose is not installed."
    echo "Please install Docker Desktop first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Function to check if MongoDB is running in Docker
check_mongodb_running() {
    if docker ps --format "table {{.Names}}" | grep -q "self_assessment_mongo"; then
        return 0
    else
        return 1
    fi
}

# Function to wait for MongoDB to be ready
wait_for_mongodb() {
    echo "⏳ Waiting for MongoDB to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker exec self_assessment_mongo mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1; then
            echo "✅ MongoDB is ready!"
            return 0
        fi
        
        echo "   Attempt $attempt/$max_attempts - MongoDB not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ MongoDB failed to start within timeout"
    return 1
}

echo "Choose an option:"
echo "1) Start local MongoDB and migrate data from remote"
echo "2) Start local MongoDB only (skip migration)"
echo "3) Stop all services"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Starting local MongoDB and migrating data..."
        
        # Stop any existing containers
        echo "🛑 Stopping existing containers..."
        docker-compose down >/dev/null 2>&1 || true
        
        # Start only MongoDB first
        echo "🐳 Starting MongoDB container..."
        docker-compose up -d mongodb
        
        # Wait for MongoDB to be ready
        if ! wait_for_mongodb; then
            echo "❌ Failed to start MongoDB"
            exit 1
        fi
        
        # Install required Python packages if not already installed
        echo "📦 Installing Python dependencies for migration..."
        if [ -d "newenv" ]; then
            source newenv/bin/activate
        fi
        
        pip install pymongo >/dev/null 2>&1 || {
            echo "❌ Failed to install pymongo. Please install it manually:"
            echo "   pip install pymongo"
            exit 1
        }
        
        # Run migration script
        echo "🔄 Starting data migration from remote to local MongoDB..."
        if python3 migrate_db.py; then
            echo "✅ Data migration completed successfully!"
        else
            echo "⚠️  Migration failed or no data found. Continuing with empty local database..."
        fi
        
        # Start the web application
        echo "🌐 Starting web application..."
        docker-compose up -d web
        
        echo ""
        echo "🎉 Setup completed!"
        echo "🌐 Application: http://localhost:5002"
        echo "📊 MongoDB Admin: http://localhost:8081 (admin/admin123)"
        echo ""
        echo "Default login credentials:"
        echo "   Admin: admin/admin"
        echo "   Student: student/student"
        ;;
        
    2)
        echo "🚀 Starting local MongoDB only..."
        
        # Stop any existing containers
        docker-compose down >/dev/null 2>&1 || true
        
        # Start all services
        docker-compose up -d
        
        echo "✅ Local MongoDB started!"
        echo "🌐 Application: http://localhost:5002"
        echo "📊 MongoDB Admin: http://localhost:8081 (admin/admin123)"
        ;;
        
    3)
        echo "🛑 Stopping all services..."
        docker-compose down
        echo "✅ All services stopped"
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Connect to MongoDB: docker exec -it self_assessment_mongo mongosh assessment"