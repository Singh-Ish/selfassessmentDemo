#!/usr/bin/env python3
"""
Sample Data Initialization Script
Populates the local MongoDB with basic sample data for testing
"""

import os
import sys
from pymongo import MongoClient

# Local MongoDB connection
LOCAL_URI = "mongodb://localhost:27017/assessment"

def get_local_client():
    """Connect to local MongoDB"""
    try:
        client = MongoClient(LOCAL_URI)
        db = client.assessment
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to local MongoDB")
        return client, db
    except Exception as e:
        print(f"❌ Failed to connect to local MongoDB: {e}")
        return None, None

def create_sample_data(db):
    """Create sample data for testing"""
    
    # Sample users
    users_data = [
        {
            "userId": 1,
            "firstName": "Admin",
            "lastName": "User",
            "email": "admin@sce.carleton.ca",
            "username": "admin",
            "password": "admin"
        },
        {
            "userId": 2,
            "firstName": "Student",
            "lastName": "User",
            "email": "student@carleton.ca",
            "username": "student", 
            "password": "student"
        },
        {
            "userId": 1001,
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@carleton.ca",
            "username": "johndoe",
            "password": "password123"
        },
        {
            "userId": 1002,
            "firstName": "Jane",
            "lastName": "Smith",
            "email": "jane.smith@carleton.ca",
            "username": "janesmith",
            "password": "password123"
        }
    ]
    
    # Sample roles
    roles_data = [
        {"userId": 1, "rname": "admin"},
        {"userId": 2, "rname": "student"},
        {"userId": 1001, "rname": "student"},
        {"userId": 1002, "rname": "student"}
    ]
    
    # Sample projects
    projects_data = [
        {
            "groupNo": 1,
            "title": "AI-Powered Web Application",
            "supervisor": "Dr. Smith",
            "coSupervisor": "Dr. Johnson",
            "userId": 1001,
            "lastName": "Doe",
            "firstName": "John",
            "assessmentStatus": 0
        },
        {
            "groupNo": 1,
            "title": "AI-Powered Web Application", 
            "supervisor": "Dr. Smith",
            "coSupervisor": "Dr. Johnson",
            "userId": 1002,
            "lastName": "Smith",
            "firstName": "Jane",
            "assessmentStatus": 0
        }
    ]
    
    # Sample rubrics
    rubrics_data = [
        {
            "Indicator": "Problem Analysis",
            "Beginning": "Basic understanding of the problem",
            "Developing": "Good understanding with minor gaps",
            "Accomplished": "Strong understanding and analysis",
            "Exemplary": "Exceptional analysis and insight"
        },
        {
            "Indicator": "Technical Skills",
            "Beginning": "Basic technical implementation",
            "Developing": "Good technical skills with guidance",
            "Accomplished": "Strong technical implementation",
            "Exemplary": "Advanced technical excellence"
        },
        {
            "Indicator": "Communication",
            "Beginning": "Basic communication skills",
            "Developing": "Clear communication with minor issues",
            "Accomplished": "Effective and professional communication",
            "Exemplary": "Outstanding communication and presentation"
        }
    ]
    
    # Sample faculty
    faculty_data = [
        {
            "lastName": "Smith",
            "firstName": "Dr. John",
            "email": "john.smith@sce.carleton.ca"
        },
        {
            "lastName": "Johnson", 
            "firstName": "Dr. Sarah",
            "email": "sarah.johnson@sce.carleton.ca"
        }
    ]
    
    # Sample email template
    email_template_data = {
        "sender": "saportal@sce.carleton.ca",
        "subject": "Self Assessment Portal - Action Required",
        "message": "Please complete your self assessment for your project. Log in to the portal to submit your evaluation."
    }
    
    try:
        # Clear existing data
        collections = ["user", "role", "projects", "rubics", "faculty", "emailtemplate"]
        for collection_name in collections:
            result = db[collection_name].delete_many({})
            print(f"🗑️  Cleared {result.deleted_count} documents from '{collection_name}'")
        
        # Insert sample data
        db.user.insert_many(users_data)
        print(f"✅ Inserted {len(users_data)} users")
        
        db.role.insert_many(roles_data) 
        print(f"✅ Inserted {len(roles_data)} user roles")
        
        db.projects.insert_many(projects_data)
        print(f"✅ Inserted {len(projects_data)} projects")
        
        db.rubics.insert_many(rubrics_data)
        print(f"✅ Inserted {len(rubrics_data)} rubrics")
        
        db.faculty.insert_many(faculty_data)
        print(f"✅ Inserted {len(faculty_data)} faculty members")
        
        db.emailtemplate.insert_one(email_template_data)
        print(f"✅ Inserted email template")
        
        print(f"\n🎉 Sample data initialization completed!")
        print(f"\n📋 Available test accounts:")
        print(f"   Admin: admin/admin")
        print(f"   Student: student/student") 
        print(f"   Student: johndoe/password123")
        print(f"   Student: janesmith/password123")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False
    
    return True

def main():
    print("🎯 Sample Data Initialization")
    print("=" * 30)
    
    # Connect to local database
    client, db = get_local_client()
    if not client:
        sys.exit(1)
    
    try:
        if create_sample_data(db):
            print(f"\n✅ Initialization completed successfully!")
        else:
            print(f"\n❌ Initialization failed!")
            sys.exit(1)
    
    finally:
        client.close()
        print(f"\n🔒 Database connection closed")

if __name__ == "__main__":
    main()