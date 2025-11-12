#!/usr/bin/env python3
"""
Mississippi Literacy Database Setup Script
Automates database creation, schema setup, and data import
"""

import os
import sys
import mysql.connector
import subprocess
from dotenv import load_dotenv
import time

class DatabaseSetup:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database = os.getenv('MYSQL_DB', 'literacy_db')
        
    def print_status(self, message, status="info"):
        """Print colored status messages"""
        colors = {
            "info": "\033[94m",     # Blue
            "success": "\033[92m",   # Green
            "warning": "\033[93m",   # Yellow
            "error": "\033[91m",     # Red
            "reset": "\033[0m"       # Reset
        }
        print(f"{colors.get(status, '')}{message}{colors['reset']}")
    
    def check_prerequisites(self):
        """Check if all required files and dependencies exist"""
        self.print_status("🔍 Checking prerequisites...", "info")
        
        missing_items = []
        
        # Check .env file
        if not os.path.exists('.env'):
            missing_items.append(".env file (copy .env.example and configure)")
        
        # Check required files
        required_files = ['literacy_tables.sql', 'literacy_data.sql', 'requirements.txt']
        for file in required_files:
            if not os.path.exists(file):
                missing_items.append(f"{file}")
        
        # Check environment variables
        if not all([self.user, self.password]):
            missing_items.append("MYSQL_USER and MYSQL_PASSWORD in .env")
        
        if missing_items:
            self.print_status("❌ Missing requirements:", "error")
            for item in missing_items:
                print(f"   - {item}")
            return False
            
        self.print_status("✅ All prerequisites found", "success")
        return True
    
    def test_mysql_connection(self):
        """Test MySQL server connection"""
        self.print_status("🔌 Testing MySQL connection...", "info")
        
        try:
            # Test connection without database first
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            conn.close()
            self.print_status("✅ MySQL connection successful", "success")
            return True
        except mysql.connector.Error as e:
            self.print_status(f"❌ MySQL connection failed: {e}", "error")
            self.print_status("💡 Make sure MySQL is running and credentials are correct", "warning")
            return False
    
    def create_database(self):
        """Create the literacy_db database if it doesn't exist"""
        self.print_status("🗄️  Creating database...", "info")
        
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.print_status(f"✅ Database '{self.database}' ready", "success")
            
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            self.print_status(f"❌ Database creation failed: {e}", "error")
            return False
    
    def run_schema(self):
        """Run the database schema creation"""
        self.print_status("📋 Creating database schema...", "info")
        
        try:
            # Use mysql command to run the schema
            cmd = [
                'mysql',
                f'-h{self.host}',
                f'-u{self.user}',
                f'-p{self.password}',
                self.database
            ]
            
            with open('literacy_tables.sql', 'r') as schema_file:
                result = subprocess.run(
                    cmd,
                    input=schema_file.read(),
                    text=True,
                    capture_output=True
                )
            
            if result.returncode == 0:
                self.print_status("✅ Database schema created successfully", "success")
                return True
            else:
                self.print_status(f"❌ Schema creation failed: {result.stderr}", "error")
                return False
                
        except Exception as e:
            self.print_status(f"❌ Schema creation error: {e}", "error")
            return False
    
    def import_data(self):
        """Import literacy data using the import script"""
        self.print_status("📊 Importing literacy data...", "info")
        
        try:
            # Run the import script
            result = subprocess.run(
                [sys.executable, 'dev/import_data.py'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Parse output to get record count
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if 'records imported successfully' in line.lower():
                        self.print_status(f"✅ {line}", "success")
                        return True
                
                self.print_status("✅ Data import completed", "success")
                return True
            else:
                self.print_status(f"❌ Data import failed: {result.stderr}", "error")
                return False
                
        except Exception as e:
            self.print_status(f"❌ Data import error: {e}", "error")
            return False
    
    def validate_installation(self):
        """Validate the complete installation"""
        self.print_status("🔍 Validating installation...", "info")
        
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conn.cursor()
            
            # Check tables exist
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            expected_tables = ['Districts', 'Schools', 'Subgroups', 'Performance_Data', 'Teacher_Quality', 'NAEP_Assessments']
            
            missing_tables = [table for table in expected_tables if table not in tables]
            if missing_tables:
                self.print_status(f"❌ Missing tables: {missing_tables}", "error")
                return False
            
            # Check data counts
            data_counts = {}
            for table in expected_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                data_counts[table] = count
            
            self.print_status("📊 Database validation results:", "info")
            for table, count in data_counts.items():
                status = "success" if count > 0 else "warning"
                self.print_status(f"   {table}: {count:,} records", status)
            
            total_records = sum(data_counts.values())
            if total_records > 0:
                self.print_status(f"✅ Installation validated - {total_records:,} total records", "success")
                return True
            else:
                self.print_status("⚠️  Tables created but no data imported", "warning")
                return False
                
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as e:
            self.print_status(f"❌ Validation failed: {e}", "error")
            return False
    
    def run_setup(self):
        """Run the complete setup process"""
        self.print_status("🚀 Starting Mississippi Literacy Database Setup", "info")
        print("=" * 60)
        
        steps = [
            ("Prerequisites", self.check_prerequisites),
            ("MySQL Connection", self.test_mysql_connection),
            ("Database Creation", self.create_database),
            ("Schema Setup", self.run_schema),
            ("Data Import", self.import_data),
            ("Validation", self.validate_installation)
        ]
        
        for step_name, step_function in steps:
            if not step_function():
                self.print_status(f"❌ Setup failed at: {step_name}", "error")
                return False
            print()  # Add spacing between steps
        
        print("=" * 60)
        self.print_status("🎉 Setup completed successfully!", "success")
        self.print_status("🌐 Run 'python3 website.py' to start the application", "info")
        return True

def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
Mississippi Literacy Database Setup

Usage:
    python3 setup.py              # Run full setup
    python3 setup.py --help       # Show this help

This script will:
1. Check prerequisites (.env, required files)
2. Test MySQL connection
3. Create literacy_db database
4. Create database schema
5. Import literacy data (19,377+ records)
6. Validate installation

Prerequisites:
- MySQL server running
- .env file with database credentials
- literacy_data.sql file in project root
        """)
        return
    
    setup = DatabaseSetup()
    setup.run_setup()

if __name__ == '__main__':
    main()