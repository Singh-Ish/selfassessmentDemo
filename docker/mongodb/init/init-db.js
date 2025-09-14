// MongoDB initialization script for self-assessment portal
// This script runs when the MongoDB container starts for the first time

print("Starting database initialization...");

// Switch to the assessment database
db = db.getSiblingDB("assessment");

// Create collections if they don't exist
db.createCollection("user");
db.createCollection("role");
db.createCollection("projects");
db.createCollection("rubics");
db.createCollection("samatrix");
db.createCollection("emailtemplate");
db.createCollection("feedback");
db.createCollection("faculty");

// Create indexes for better performance
db.user.createIndex({ userId: 1 }, { unique: true });
db.user.createIndex({ email: 1 }, { unique: true });
db.user.createIndex({ username: 1 }, { unique: true });

db.role.createIndex({ userId: 1 }, { unique: true });

db.projects.createIndex({ userId: 1 }, { unique: true });
db.projects.createIndex({ groupNo: 1 });

db.rubics.createIndex({ Indicator: 1 });

db.samatrix.createIndex({ sid: 1, fsid: 1, Indicator: 1 });

db.faculty.createIndex({ email: 1 }, { unique: true });
db.faculty.createIndex({ lastName: 1 }, { unique: true });

db.feedback.createIndex({ userId: 1 }, { unique: true });

print("Database initialization completed successfully!");
print("Collections created: " + db.getCollectionNames().length);
