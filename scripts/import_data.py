import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from project import create_website, db
from project.models import (
    Locations, Districts, Schools, DemographicGroups, 
    AcademicYears, PerformanceRecords, TeacherQuality, NAEPAssessments
)

def parse_percentage(value):
    """Parse percentage values, handling special cases like <10, 0-10%, etc."""
    if pd.isna(value) or value == '' or value == 'N/A':
        return None
    
    value = str(value).strip()
    if value == '<10' or value.startswith('<'):
        return 5.0  # Use middle of range for <10
    elif '-' in value and '%' in value:
        # Handle ranges like "0-10%", "21-30%"
        range_part = value.replace('%', '')
        try:
            start, end = range_part.split('-')
            return (float(start) + float(end)) / 2
        except:
            return None
    else:
        # Regular percentage
        try:
            return float(str(value).replace('%', ''))
        except:
            return None

def categorize_subgroup(subgroup_name):
    """Categorize subgroups by type for easier filtering"""
    if subgroup_name == 'All':
        return 'All'
    elif subgroup_name in ['Male', 'Female']:
        return 'Gender'
    elif any(race in subgroup_name for race in ['White', 'Black', 'Hispanic', 'Asian', 'Native', 'Hawaiian', 'Two or More']):
        return 'Race'
    elif 'Economically' in subgroup_name:
        return 'EconStatus'
    elif 'English Learner' in subgroup_name or 'Non English Learner' in subgroup_name:
        return 'EL'
    elif 'Students with Disabilities' in subgroup_name or 'Students without Disabilities' in subgroup_name:
        return 'SPED'
    elif subgroup_name.startswith('Grade '):
        return 'Grade'
    else:
        return 'SpecialPop'

def clean_numeric_value(value):
    """Clean and convert numeric values"""
    if pd.isna(value) or value == '' or value == 'N/A':
        return None
    try:
        return float(value)
    except:
        return None

def import_data():
    """Import CSV data into the new database schema"""
    print("Starting data import...")
    
    # Load CSV data
    df = pd.read_csv('./data/Mississippi_Literacy_Dataset.csv')
    print(f"Loaded {len(df)} records from CSV")
    
    # Create Flask app context
    app = create_website()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Import Academic Years
        print("Importing academic years...")
        years = df['School_Year'].dropna().unique()
        for year in years:
            if not AcademicYears.query.filter_by(school_year=int(year)).first():
                year_obj = AcademicYears(school_year=int(year))
                db.session.add(year_obj)
        db.session.commit()
        
        # Import Locations (County/City/ZIP combinations)
        print("Importing locations...")
        location_combinations = df[['County', 'City', 'ZIP']].dropna().drop_duplicates()
        location_map = {}
        
        for _, row in location_combinations.iterrows():
            county = str(row['County']) if pd.notna(row['County']) else None
            city = str(row['City']) if pd.notna(row['City']) else None
            zip_code = str(row['ZIP']) if pd.notna(row['ZIP']) else None
            
            # Create location key for mapping
            location_key = f"{county}|{city}|{zip_code}"
            
            if location_key not in location_map:
                location = Locations(county=county, city=city, zip_code=zip_code)
                db.session.add(location)
                db.session.flush()
                location_map[location_key] = location.location_id
        
        db.session.commit()
        
        # Import Districts
        print("Importing districts...")
        district_data = df[['District#', 'District_Name', 'County', 'City', 'ZIP']].drop_duplicates()
        district_map = {}
        
        for _, row in district_data.iterrows():
            district_num = int(row['District#'])
            district_name = str(row['District_Name'])
            
            # Find location_id
            location_key = f"{row['County'] if pd.notna(row['County']) else None}|{row['City'] if pd.notna(row['City']) else None}|{row['ZIP'] if pd.notna(row['ZIP']) else None}"
            location_id = location_map.get(location_key)
            
            if district_num not in district_map:
                district = Districts(
                    district_number=district_num,
                    district_name=district_name,
                    location_id=location_id
                )
                db.session.add(district)
                db.session.flush()
                district_map[district_num] = district.district_id
        
        db.session.commit()
        
        # Import Schools
        print("Importing schools...")
        school_data = df[['School#', 'School_Name', 'District#', 'Type']].dropna().drop_duplicates()
        school_map = {}
        
        for _, row in school_data.iterrows():
            school_num = int(row['School#'])
            school_name = str(row['School_Name'])
            district_num = int(row['District#'])
            school_type = str(row['Type'])
            
            school_key = f"{school_num}_{district_num}"
            
            if school_key not in school_map:
                school = Schools(
                    school_number=school_num,
                    school_name=school_name,
                    district_id=district_map[district_num],
                    school_type=school_type
                )
                db.session.add(school)
                db.session.flush()
                school_map[school_key] = school.school_id
        
        db.session.commit()
        
        # Import Demographic Groups
        print("Importing demographic groups...")
        subgroups = df['Subgroup'].dropna().unique()
        group_map = {}
        
        for subgroup_name in subgroups:
            subgroup_type = categorize_subgroup(subgroup_name)
            
            if subgroup_name not in group_map:
                group = DemographicGroups(
                    subgroup_name=subgroup_name,
                    subgroup_type=subgroup_type
                )
                db.session.add(group)
                db.session.flush()
                group_map[subgroup_name] = group.group_id
        
        db.session.commit()
        
        # Import Performance Records
        print("Importing performance records...")
        year_map = {year.school_year: year.year_id for year in AcademicYears.query.all()}
        
        performance_columns = [
            'English Proficiency', 'English Growth', 'English Growth Lowest 25%',
            'English Performance Level 1', 'English Performance Students Level 1',
            'English Performance Level 2', 'English Performance Students Level 2',
            'English Performance Level 3', 'English Performance Students Level 3',
            'English Performance Level 4', 'English Performance Students Level 4',
            'English Performance Level 5', 'English Performance Students Level 5',
            '% Chronic Absenteeism'
        ]
        
        performance_data = df[['School_Year', 'School#', 'District#', 'Subgroup', 'Grade'] + performance_columns].dropna(subset=['School#', 'District#', 'Subgroup'])
        
        for _, row in performance_data.iterrows():
            try:
                school_key = f"{int(row['School#'])}_{int(row['District#'])}"
                
                if (school_key in school_map and 
                    row['Subgroup'] in group_map and 
                    int(row['School_Year']) in year_map):
                    
                    record = PerformanceRecords(
                        school_id=school_map[school_key],
                        group_id=group_map[row['Subgroup']],
                        year_id=year_map[int(row['School_Year'])],
                        grade_level=str(row['Grade']).strip() if pd.notna(row['Grade']) else None,
                        english_proficiency=parse_percentage(row.get('English Proficiency')),
                        english_growth=parse_percentage(row.get('English Growth')),
                        english_growth_lowest_25=parse_percentage(row.get('English Growth Lowest 25%')),
                        performance_level_1_pct=parse_percentage(row.get('English Performance Level 1')),
                        performance_level_1_count=clean_numeric_value(row.get('English Performance Students Level 1')),
                        performance_level_2_pct=parse_percentage(row.get('English Performance Level 2')),
                        performance_level_2_count=clean_numeric_value(row.get('English Performance Students Level 2')),
                        performance_level_3_pct=parse_percentage(row.get('English Performance Level 3')),
                        performance_level_3_count=clean_numeric_value(row.get('English Performance Students Level 3')),
                        performance_level_4_pct=parse_percentage(row.get('English Performance Level 4')),
                        performance_level_4_count=clean_numeric_value(row.get('English Performance Students Level 4')),
                        performance_level_5_pct=parse_percentage(row.get('English Performance Level 5')),
                        performance_level_5_count=clean_numeric_value(row.get('English Performance Students Level 5')),
                        chronic_absenteeism_pct=parse_percentage(row.get('% Chronic Absenteeism'))
                    )
                    db.session.add(record)
            except Exception as e:
                print(f"Error processing performance record: {e}")
                continue
        
        db.session.commit()
        
        # Import Teacher Quality data
        print("Importing teacher quality data...")
        teacher_columns = [
            '% of Experienced Teachers in high poverty schools',
            '% of Experienced Teachers in low poverty schools',
            '% of Emergency Provisional Teachers in high poverty schools',
            '% of Emergency Provisional Teachers in low poverty schools',
            '% of In Field Teachers in high poverty schools',
            '% of In Field Teachers in low poverty schools',
            '% of Effective Teachers in high poverty schools',
            '% of Effective Teachers in low poverty schools'
        ]
        
        teacher_data = df[['School_Year', 'District#'] + teacher_columns].dropna(subset=['District#'])
        teacher_data = teacher_data.drop_duplicates(subset=['School_Year', 'District#'])
        
        for _, row in teacher_data.iterrows():
            try:
                district_num = int(row['District#'])
                
                if (district_num in district_map and 
                    int(row['School_Year']) in year_map):
                    
                    teacher_quality = TeacherQuality(
                        district_id=district_map[district_num],
                        year_id=year_map[int(row['School_Year'])],
                        experienced_teachers_high_poverty=parse_percentage(row.get('% of Experienced Teachers in high poverty schools')),
                        experienced_teachers_low_poverty=parse_percentage(row.get('% of Experienced Teachers in low poverty schools')),
                        emergency_provisional_teachers_high_poverty=parse_percentage(row.get('% of Emergency Provisional Teachers in high poverty schools')),
                        emergency_provisional_teachers_low_poverty=parse_percentage(row.get('% of Emergency Provisional Teachers in low poverty schools')),
                        in_field_teachers_high_poverty=parse_percentage(row.get('% of In Field Teachers in high poverty schools')),
                        in_field_teachers_low_poverty=parse_percentage(row.get('% of In Field Teachers in low poverty schools')),
                        effective_teachers_high_poverty=parse_percentage(row.get('% of Effective Teachers in high poverty schools')),
                        effective_teachers_low_poverty=parse_percentage(row.get('% of Effective Teachers in low poverty schools'))
                    )
                    db.session.add(teacher_quality)
            except Exception as e:
                print(f"Error processing teacher quality record: {e}")
                continue
        
        db.session.commit()
        
        # Import NAEP Assessment data
        print("Importing NAEP assessments...")
        naep_columns = [
            'Assessment NAEP 4th Grade Reading - Below Basic',
            'Assessment NAEP 4th Grade Reading - Basic', 
            'Assessment NAEP 4th Grade Reading - Proficient',
            'Assessment NAEP 4th Grade Reading - Advanced',
            'Assessment NAEP 8th Grade Reading - Below Basic',
            'Assessment NAEP 8th Grade Reading - Basic',
            'Assessment NAEP 8th Grade Reading - Proficient',
            'Assessment NAEP 8th Grade Reading - Advanced'
        ]
        
        naep_data = df[['School_Year', 'District#', 'School#', 'Type'] + naep_columns].dropna(subset=naep_columns, how='all')
        naep_data = naep_data.drop_duplicates()
        
        for _, row in naep_data.iterrows():
            try:
                district_num = int(row['District#']) if pd.notna(row['District#']) else None
                school_num = int(row['School#']) if pd.notna(row['School#']) else None
                scope = str(row['Type'])
                
                district_id = district_map.get(district_num) if district_num else None
                school_id = None
                if school_num and district_num:
                    school_key = f"{school_num}_{district_num}"
                    school_id = school_map.get(school_key)
                
                if int(row['School_Year']) in year_map:
                    naep = NAEPAssessments(
                        year_id=year_map[int(row['School_Year'])],
                        scope=scope,
                        district_id=district_id,
                        school_id=school_id,
                        grade_4_reading_below_basic=parse_percentage(row.get('Assessment NAEP 4th Grade Reading - Below Basic')),
                        grade_4_reading_basic=parse_percentage(row.get('Assessment NAEP 4th Grade Reading - Basic')),
                        grade_4_reading_proficient=parse_percentage(row.get('Assessment NAEP 4th Grade Reading - Proficient')),
                        grade_4_reading_advanced=parse_percentage(row.get('Assessment NAEP 4th Grade Reading - Advanced')),
                        grade_8_reading_below_basic=parse_percentage(row.get('Assessment NAEP 8th Grade Reading - Below Basic')),
                        grade_8_reading_basic=parse_percentage(row.get('Assessment NAEP 8th Grade Reading - Basic')),
                        grade_8_reading_proficient=parse_percentage(row.get('Assessment NAEP 8th Grade Reading - Proficient')),
                        grade_8_reading_advanced=parse_percentage(row.get('Assessment NAEP 8th Grade Reading - Advanced'))
                    )
                    db.session.add(naep)
            except Exception as e:
                print(f"Error processing NAEP record: {e}")
                continue
        
        db.session.commit()
        
        # Print import summary
        print("\n=== Import Summary ===")
        print(f"Locations: {Locations.query.count()}")
        print(f"Districts: {Districts.query.count()}")
        print(f"Schools: {Schools.query.count()}")
        print(f"Demographic Groups: {DemographicGroups.query.count()}")
        print(f"Academic Years: {AcademicYears.query.count()}")
        print(f"Performance Records: {PerformanceRecords.query.count()}")
        print(f"Teacher Quality Records: {TeacherQuality.query.count()}")
        print(f"NAEP Assessment Records: {NAEPAssessments.query.count()}")
        
        print("\nData import completed successfully!")

if __name__ == "__main__":
    import_data()