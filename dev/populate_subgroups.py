#!/usr/bin/env python3
"""
Populate Subgroups table with all required subgroups
"""

import pymysql
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
    'charset': 'utf8mb4',
}

# Subgroups to insert
SUBGROUPS = [
    # Basic categories
    ('All', 'All'),
    ('Female', 'Gender'),
    ('Male', 'Gender'),
    ('Black or African American', 'Race_Ethnicity'),
    ('White', 'Race_Ethnicity'),
    ('Alaskan Native or Native American', 'Race_Ethnicity'),
    ('Asian', 'Race_Ethnicity'),
    ('Hispanic or Latino', 'Race_Ethnicity'),
    ('Native Hawaiian or Pacific Islander', 'Race_Ethnicity'),
    ('Two or More Races', 'Race_Ethnicity'),
    ('Economically Disadvantaged', 'Special_Population'),
    ('Non Economically Disadvantaged', 'Special_Population'),
    ('English Learners', 'Special_Population'),
    ('Non English Learners', 'Special_Population'),
    ('Homeless', 'Special_Population'),
    ('Non Homeless', 'Special_Population'),
    ('Migrant', 'Special_Population'),
    ('Non Migrant', 'Special_Population'),
    ('Foster Care', 'Special_Population'),
    ('Students with Disabilities', 'Special_Population'),
    ('Students without Disabilities', 'Special_Population'),
    ('Military Connected', 'Special_Population'),

    # Grade levels
    ('Grade 3  ', 'Special_Population'),
    ('Grade 4  ', 'Special_Population'),
    ('Grade 5  ', 'Special_Population'),
    ('Grade 6  ', 'Special_Population'),
    ('Grade 7  ', 'Special_Population'),
    ('Grade 8  ', 'Special_Population'),
    ('Grade 10  ', 'Special_Population'),

    # Intersectional subgroups - Race/Ethnicity + Gender
    ('Alaskan Native or Native American Female', 'Race_Ethnicity'),
    ('Alaskan Native or Native American Male', 'Race_Ethnicity'),
    ('Asian Female', 'Race_Ethnicity'),
    ('Asian Male', 'Race_Ethnicity'),
    ('Black or African American Female', 'Race_Ethnicity'),
    ('Black or African American Male', 'Race_Ethnicity'),
    ('Hispanic or Latino Female', 'Race_Ethnicity'),
    ('Hispanic or Latino Male', 'Race_Ethnicity'),
    ('Native Hawaiian or Pacific Islander Female', 'Race_Ethnicity'),
    ('Native Hawaiian or Pacific Islander Male', 'Race_Ethnicity'),
    ('Two or More Races Female', 'Race_Ethnicity'),
    ('Two or More Races Male', 'Race_Ethnicity'),
    ('White Female', 'Race_Ethnicity'),
    ('White Male', 'Race_Ethnicity'),

    # Intersectional subgroups - Race/Ethnicity + English Learners
    ('Alaskan Native or Native American English Learners', 'Race_Ethnicity'),
    ('Alaskan Native or Native American Non English Learners', 'Race_Ethnicity'),
    ('Asian English Learners', 'Race_Ethnicity'),
    ('Asian Non English Learners', 'Race_Ethnicity'),
    ('Black or African American English Learners', 'Race_Ethnicity'),
    ('Black or African American Non English Learners', 'Race_Ethnicity'),
    ('Hispanic or Latino English Learners', 'Race_Ethnicity'),
    ('Hispanic or Latino Non English Learners', 'Race_Ethnicity'),
    ('Native Hawaiian or Pacific Islander English Learners', 'Race_Ethnicity'),
    ('Native Hawaiian or Pacific Islander Non English Learners', 'Race_Ethnicity'),
    ('Two or More Races English Learners', 'Race_Ethnicity'),
    ('Two or More Races Non English Learners', 'Race_Ethnicity'),
    ('White English Learners', 'Race_Ethnicity'),
    ('White Non English Learners', 'Race_Ethnicity'),

    # Intersectional subgroups - Race/Ethnicity + Disabilities
    ('Alaskan Native or Native American Students with Disabilities', 'Race_Ethnicity'),
    ('Alaskan Native or Native American Students without Disabilities', 'Race_Ethnicity'),
    ('Asian Students with Disabilities', 'Race_Ethnicity'),
    ('Asian Students without Disabilities', 'Race_Ethnicity'),
    ('Black or African American Students with Disabilities', 'Race_Ethnicity'),
    ('Black or African American Students without Disabilities', 'Race_Ethnicity'),
    ('Hispanic or Latino Students with Disabilities', 'Race_Ethnicity'),
    ('Hispanic or Latino Students without Disabilities', 'Race_Ethnicity'),
    ('Native Hawaiian or Pacific Islander Students with Disabilities', 'Race_Ethnicity'),
    ('Native Hawaiian or Pacific Islander Students without Disabilities', 'Race_Ethnicity'),
    ('Two or More Races Students with Disabilities', 'Race_Ethnicity'),
    ('Two or More Races Students without Disabilities', 'Race_Ethnicity'),
    ('White Students with Disabilities', 'Race_Ethnicity'),
    ('White Students without Disabilities', 'Race_Ethnicity'),
]

def main():
    """Insert subgroups into database"""
    print("Connecting to database...")

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Inserting subgroups...")

        for subgroup_name, category in SUBGROUPS:
            try:
                cursor.execute(
                    "INSERT INTO Subgroups (Subgroup_Name, Subgroup_Category) VALUES (%s, %s)",
                    (subgroup_name, category)
                )
                print(f"  ✓ Added: {subgroup_name} ({category})")
            except pymysql.IntegrityError:
                print(f"  - Skipped (already exists): {subgroup_name}")

        conn.commit()

        # Verify results
        cursor.execute("SELECT COUNT(*) FROM Subgroups")
        count = cursor.fetchone()[0]
        print(f"\nTotal subgroups in database: {count}")

        cursor.close()
        conn.close()

        print("✓ Subgroups populated successfully!")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
