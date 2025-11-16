#!/usr/bin/env python3
"""
Data Import Script for Mississippi Literacy Database
Imports data from literacy_data.sql into normalized MySQL schema
"""

import mysql.connector
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
    'autocommit': False
}

def connect_to_database():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def parse_literacy_data_file(filename):
    """Parse the literacy_data.sql file and extract INSERT statements"""
    records = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        for line in lines:
            line = line.strip()
            if line.startswith('INSERT INTO "literacy_data" VALUES'):
                # Extract values between parentheses
                start_paren = line.find('(')
                end_paren = line.rfind(')')
                
                if start_paren != -1 and end_paren != -1:
                    values_str = line[start_paren + 1:end_paren]
                    
                    # Parse CSV-like values, handling quotes and NULLs
                    values = parse_csv_values(values_str)
                    
                    if len(values) >= 21:  # At least the main fields we need
                        records.append(values)
    
    except Exception as e:
        print(f"Error parsing file: {e}")
    
    return records

def parse_csv_values(values_str):
    """Parse CSV-like values handling quotes and special cases"""
    values = []
    current_value = ""
    in_quotes = False
    quote_char = None
    
    i = 0
    while i < len(values_str):
        char = values_str[i]
        
        if not in_quotes:
            if char in ("'", '"'):
                in_quotes = True
                quote_char = char
            elif char == ',':
                values.append(clean_value(current_value.strip()))
                current_value = ""
            else:
                current_value += char
        else:
            if char == quote_char:
                in_quotes = False
                quote_char = None
            else:
                current_value += char
        
        i += 1
    
    # Add the last value
    if current_value.strip():
        values.append(clean_value(current_value.strip()))
    
    return values

def clean_value(value):
    """Clean and convert value to appropriate type"""
    if value is None:
        return None
    
    value = str(value).strip()
    
    # Handle NULL values
    if value.upper() == 'NULL':
        return None
    
    # Remove quotes from strings
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    
    # Handle special cases
    if value == '<10':
        return 5.0  # Use midpoint for ranges like "<10"
    elif '-' in value and '%' in value:  # Handle ranges like "0-10%"
        # Extract numeric range and use midpoint
        range_match = re.match(r'(\d+)-(\d+)%?', value)
        if range_match:
            start, end = range_match.groups()
            return (float(start) + float(end)) / 2
    
    # Try to convert to float
    try:
        return float(value)
    except (ValueError, TypeError):
        return value

def get_or_create_district(cursor, district_number, district_name):
    """Get existing district ID or create new district"""
    if district_number == 0:  # State-level data
        return None
        
    # Check if district exists
    cursor.execute(
        "SELECT District_ID FROM Districts WHERE District_Number = %s",
        (district_number,)
    )
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Create new district
    cursor.execute(
        "INSERT INTO Districts (District_Number, District_Name) VALUES (%s, %s)",
        (district_number, district_name)
    )
    return cursor.lastrowid

def get_or_create_school(cursor, school_number, school_name, district_id):
    """Get existing school ID or create new school"""
    if school_number == 0 or district_id is None:  # District-level or state-level data
        return None
    
    # Check if school exists
    cursor.execute(
        "SELECT School_ID FROM Schools WHERE School_Number = %s AND District_ID = %s",
        (school_number, district_id)
    )
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Create new school
    cursor.execute(
        "INSERT INTO Schools (School_Number, School_Name, District_ID) VALUES (%s, %s, %s)",
        (school_number, school_name, district_id)
    )
    return cursor.lastrowid

def get_subgroup_id(cursor, subgroup_name):
    """Get subgroup ID by name"""
    cursor.execute(
        "SELECT Subgroup_ID FROM Subgroups WHERE Subgroup_Name = %s",
        (subgroup_name,)
    )
    result = cursor.fetchone()
    return result[0] if result else None

def import_performance_data(cursor, record):
    """Import performance data from a record"""
    (school_year, district_num, district_name, school_num, school_name, 
     subgroup, grade, assessment_type, english_prof, english_growth, english_growth_25,
     perf_1_pct, perf_1_students, perf_2_pct, perf_2_students, perf_3_pct, perf_3_students,
     perf_4_pct, perf_4_students, perf_5_pct, perf_5_students) = record[:21]
    
    # Get or create district and school
    district_id = get_or_create_district(cursor, district_num, district_name)
    school_id = get_or_create_school(cursor, school_num, school_name, district_id)
    
    # Get subgroup ID
    subgroup_id = get_subgroup_id(cursor, subgroup)
    if not subgroup_id:
        print(f"Warning: Unknown subgroup '{subgroup}', skipping record")
        return
    
    # Convert percentage strings to numbers for performance levels
    def convert_percent(val):
        if val is None or val == '':
            return None
        try:
            # Handle range formats like "0-10%"
            if isinstance(val, str) and '-' in val:
                range_match = re.match(r'(\d+)-(\d+)', val)
                if range_match:
                    start, end = range_match.groups()
                    return (float(start) + float(end)) / 2
            return float(str(val).replace('%', ''))
        except (ValueError, TypeError):
            return None
    
    def convert_students(val):
        if val is None or val == '' or val == '<10':
            return None
        try:
            return int(float(str(val)))
        except (ValueError, TypeError):
            return None
    
    # Prepare data for insertion
    performance_data = {
        'school_year': int(school_year),
        'district_id': district_id,
        'school_id': school_id,
        'subgroup_id': subgroup_id,
        'grade_level': grade.strip() if grade else None,
        'assessment_type': assessment_type,
        'english_proficiency': english_prof,
        'english_growth': english_growth,
        'english_growth_lowest_25_percent': english_growth_25,
        'performance_level_1_percent': convert_percent(perf_1_pct),
        'performance_level_1_students': convert_students(perf_1_students),
        'performance_level_2_percent': convert_percent(perf_2_pct),
        'performance_level_2_students': convert_students(perf_2_students),
        'performance_level_3_percent': convert_percent(perf_3_pct),
        'performance_level_3_students': convert_students(perf_3_students),
        'performance_level_4_percent': convert_percent(perf_4_pct),
        'performance_level_4_students': convert_students(perf_4_students),
        'performance_level_5_percent': convert_percent(perf_5_pct),
        'performance_level_5_students': convert_students(perf_5_students),
    }
    
    # Add chronic absenteeism if available (field 32 in original data)
    if len(record) > 32 and record[32] is not None:
        performance_data['chronic_absenteeism_percent'] = record[32]
    
    # Insert performance data
    try:
        placeholders = ', '.join(['%s'] * len(performance_data))
        columns = ', '.join(performance_data.keys())
        
        cursor.execute(
            f"INSERT INTO Performance_Data ({columns}) VALUES ({placeholders}) "
            f"ON DUPLICATE KEY UPDATE "
            f"English_Proficiency = VALUES(English_Proficiency), "
            f"English_Growth = VALUES(English_Growth), "
            f"Updated_At = CURRENT_TIMESTAMP",
            list(performance_data.values())
        )
    except mysql.connector.Error as e:
        print(f"Error inserting performance data: {e}")
        print(f"Data: {performance_data}")

def main():
    """Main import function"""
    print("Starting data import process...")
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        cursor = conn.cursor()
        
        # Parse the literacy data file
        print("Parsing literacy_data.sql...")
        records = parse_literacy_data_file('MS_Lit/literacy_data.sql')
        print(f"Found {len(records)} records to import")
        
        # Import data in batches
        batch_size = 100
        imported_count = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            
            for record in batch:
                try:
                    import_performance_data(cursor, record)
                    imported_count += 1
                except Exception as e:
                    print(f"Error processing record {imported_count + 1}: {e}")
                    continue
            
            # Commit every batch
            conn.commit()
            print(f"Imported {min(imported_count, i + batch_size)} / {len(records)} records")
        
        print(f"Import completed! Total records imported: {imported_count}")
        
        # Print summary statistics
        cursor.execute("SELECT COUNT(*) FROM Districts")
        district_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Schools")
        school_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Performance_Data")
        performance_count = cursor.fetchone()[0]
        
        print(f"Summary:")
        print(f"  Districts: {district_count}")
        print(f"  Schools: {school_count}")
        print(f"  Performance Records: {performance_count}")
        
    except Exception as e:
        print(f"Import failed: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()