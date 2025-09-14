#!/usr/bin/env python3
"""
MongoDB Migration Script
Copies data from remote MongoDB Atlas to local MongoDB instance
"""

import os
import sys
from pymongo import MongoClient
from mongoengine import connect, disconnect
import json

# Remote MongoDB connection (Atlas)
REMOTE_URI = "mongodb+srv://ishdeepsingh:change.711@cluster0.ulpu6.mongodb.net/assessment"

# Local MongoDB connection
LOCAL_URI = "mongodb://localhost:27017/assessment"

def get_remote_client():
    """Connect to remote MongoDB Atlas"""
    try:
        client = MongoClient(REMOTE_URI)
        db = client.assessment
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to remote MongoDB Atlas")
        return client, db
    except Exception as e:
        print(f"❌ Failed to connect to remote MongoDB: {e}")
        return None, None

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
        print("Make sure MongoDB is running locally on port 27017")
        return None, None

def migrate_collection(remote_db, local_db, collection_name):
    """Migrate a single collection from remote to local"""
    try:
        remote_collection = remote_db[collection_name]
        local_collection = local_db[collection_name]
        
        # Get all documents from remote collection
        documents = list(remote_collection.find())
        
        if not documents:
            print(f"⚠️  Collection '{collection_name}' is empty or doesn't exist")
            return 0
        
        # Clear local collection first
        local_collection.delete_many({})
        
        # Insert documents into local collection
        result = local_collection.insert_many(documents)
        count = len(result.inserted_ids)
        
        print(f"✅ Migrated {count} documents from '{collection_name}'")
        return count
        
    except Exception as e:
        print(f"❌ Error migrating collection '{collection_name}': {e}")
        return 0

def main():
    print("🚀 MongoDB Migration Script")
    print("=" * 40)
    
    # Connect to remote database
    remote_client, remote_db = get_remote_client()
    if not remote_client:
        sys.exit(1)
    
    # Connect to local database
    local_client, local_db = get_local_client()
    if not local_client:
        sys.exit(1)
    
    try:
        # Get list of collections from remote database
        collections = remote_db.list_collection_names()
        print(f"\n📋 Found {len(collections)} collections to migrate:")
        for collection in collections:
            print(f"   - {collection}")
        
        if not collections:
            print("⚠️  No collections found in remote database")
            return
        
        print(f"\n🔄 Starting migration...")
        
        total_migrated = 0
        for collection_name in collections:
            count = migrate_collection(remote_db, local_db, collection_name)
            total_migrated += count
        
        print(f"\n🎉 Migration completed!")
        print(f"   Total documents migrated: {total_migrated}")
        print(f"   Collections migrated: {len(collections)}")
        
        # Verify migration
        print(f"\n🔍 Verification:")
        for collection_name in collections:
            remote_count = remote_db[collection_name].count_documents({})
            local_count = local_db[collection_name].count_documents({})
            status = "✅" if remote_count == local_count else "❌"
            print(f"   {status} {collection_name}: {local_count}/{remote_count}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)
    
    finally:
        # Close connections
        remote_client.close()
        local_client.close()
        print(f"\n🔒 Database connections closed")

if __name__ == "__main__":
    main()