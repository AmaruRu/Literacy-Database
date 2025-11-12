#!/usr/bin/env python3
"""
Database Validation Script for Mississippi Literacy Database
Performs comprehensive validation of schema consistency, data integrity, and accuracy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import create_website, db
from project.models import Districts, Schools, Subgroups, PerformanceData, TeacherQuality, NAEPAssessments
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

class DatabaseValidator:
    def __init__(self):
        self.app = None
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'schema_validation': [],
            'data_integrity': [],
            'data_quality': [],
            'summary': {
                'total_issues': 0,
                'critical_issues': 0,
                'warnings': 0
            }
        }
    
    def connect(self):
        """Establish database connection"""
        try:
            self.app = create_website()
            print("✅ Database connection established")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        pass  # Flask handles connection cleanup
    
    def add_issue(self, category, issue_type, severity, description, details=None):
        """Add validation issue to results"""
        if category not in self.validation_results:
            self.validation_results[category] = []
        
        issue = {
            'type': issue_type,
            'severity': severity,
            'description': description,
            'details': details
        }
        
        self.validation_results[category].append(issue)
        self.validation_results['summary']['total_issues'] += 1
        
        if severity == 'critical':
            self.validation_results['summary']['critical_issues'] += 1
        elif severity == 'warning':
            self.validation_results['summary']['warnings'] += 1
    
    def validate_schema_consistency(self):
        """Validate database schema against expected structure"""
        print("\n🔍 Validating Schema Consistency...")
        
        # Only check for core required columns, not all possible columns
        expected_tables = {
            'Districts': ['District_ID', 'District_Number', 'District_Name'],
            'Schools': ['School_ID', 'School_Number', 'School_Name', 'District_ID'],
            'Subgroups': ['Subgroup_ID', 'Subgroup_Name', 'Subgroup_Category'],
            'Performance_Data': ['Performance_ID', 'School_Year', 'Subgroup_ID', 'Assessment_Type', 'English_Proficiency'],
            'Teacher_Quality': ['Teacher_Quality_ID', 'School_Year'],
            'NAEP_Assessments': ['NAEP_ID', 'School_Year']
        }
        
        for table_name, expected_columns in expected_tables.items():
            try:
                with self.app.app_context():
                    result = db.session.execute(db.text(f"DESCRIBE {table_name}")).fetchall()
                    actual_columns = [row[0] for row in result]
                
                # Check for missing expected columns
                missing_columns = set(expected_columns) - set(actual_columns)
                if missing_columns:
                    self.add_issue('schema_validation', 'missing_columns', 'critical',
                                 f"Table {table_name} missing expected columns",
                                 {'missing': list(missing_columns)})
                
                # Note: We don't flag extra columns as issues since tables may have additional valid columns
                
                print(f"  ✓ {table_name}: {len(actual_columns)} columns")
                
            except Exception as e:
                self.add_issue('schema_validation', 'table_missing', 'critical',
                             f"Table {table_name} not found or inaccessible",
                             {'error': str(e)})
    
    def validate_data_integrity(self):
        """Validate referential integrity and constraints"""
        print("\n🔗 Validating Data Integrity...")
        
        # Check for orphaned records
        integrity_checks = [
            {
                'name': 'Orphaned Schools',
                'query': '''SELECT COUNT(*) FROM Schools s 
                           LEFT JOIN Districts d ON s.District_ID = d.District_ID 
                           WHERE d.District_ID IS NULL''',
                'expected': 0
            },
            {
                'name': 'Orphaned Performance Records',
                'query': '''SELECT COUNT(*) FROM Performance_Data p
                           LEFT JOIN Subgroups s ON p.Subgroup_ID = s.Subgroup_ID
                           WHERE s.Subgroup_ID IS NULL''',
                'expected': 0
            },
            {
                'name': 'Invalid Performance School References',
                'query': '''SELECT COUNT(*) FROM Performance_Data p
                           LEFT JOIN Schools s ON p.School_ID = s.School_ID
                           WHERE p.School_ID IS NOT NULL AND s.School_ID IS NULL''',
                'expected': 0
            },
            {
                'name': 'Duplicate District Numbers',
                'query': '''SELECT COUNT(*) FROM (
                              SELECT District_Number, COUNT(*) as cnt 
                              FROM Districts 
                              GROUP BY District_Number 
                              HAVING COUNT(*) > 1
                           ) as duplicates''',
                'expected': 0
            }
        ]
        
        for check in integrity_checks:
            try:
                with self.app.app_context():
                    result = db.session.execute(db.text(check['query'])).scalar()
                
                if result != check['expected']:
                    severity = 'critical' if result > 0 else 'warning'
                    self.add_issue('data_integrity', 'constraint_violation', severity,
                                 f"{check['name']}: {result} violations found",
                                 {'count': result, 'expected': check['expected']})
                    print(f"  ❌ {check['name']}: {result} issues")
                else:
                    print(f"  ✓ {check['name']}: OK")
                    
            except Exception as e:
                self.add_issue('data_integrity', 'check_failed', 'critical',
                             f"Failed to run integrity check: {check['name']}",
                             {'error': str(e)})
    
    def validate_data_quality(self):
        """Validate data quality and consistency"""
        print("\n📊 Validating Data Quality...")
        
        # Record counts
        table_counts = {}
        tables = ['Districts', 'Schools', 'Subgroups', 'Performance_Data', 'Teacher_Quality', 'NAEP_Assessments']
        
        for table in tables:
            try:
                with self.app.app_context():
                    count = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table}")).scalar()
                table_counts[table] = count
                print(f"  📋 {table}: {count:,} records")
                
                # Flag empty tables that should have data
                if table in ['Teacher_Quality', 'NAEP_Assessments'] and count == 0:
                    self.add_issue('data_quality', 'missing_data', 'warning',
                                 f"Table {table} is empty but should contain data",
                                 {'count': count})
                
            except Exception as e:
                self.add_issue('data_quality', 'count_failed', 'critical',
                             f"Failed to count records in {table}",
                             {'error': str(e)})
        
        # Check for invalid percentage values
        try:
            with self.app.app_context():
                invalid_percentages = db.session.execute(db.text('''
                SELECT COUNT(*) FROM Performance_Data 
                WHERE English_Proficiency > 100 
                   OR English_Proficiency < 0
                   OR Performance_Level_1_Percent > 100
                   OR Performance_Level_1_Percent < 0
                   OR Performance_Level_2_Percent > 100
                   OR Performance_Level_2_Percent < 0
                   OR Performance_Level_3_Percent > 100
                   OR Performance_Level_3_Percent < 0
                   OR Performance_Level_4_Percent > 100
                   OR Performance_Level_4_Percent < 0
                   OR Performance_Level_5_Percent > 100
                   OR Performance_Level_5_Percent < 0
                ''')).scalar()
            
            if invalid_percentages > 0:
                self.add_issue('data_quality', 'invalid_percentages', 'critical',
                             f"Found {invalid_percentages} records with invalid percentage values",
                             {'count': invalid_percentages})
                print(f"  ❌ Invalid percentages: {invalid_percentages}")
            else:
                print(f"  ✓ Percentage validation: OK")
                
        except Exception as e:
            self.add_issue('data_quality', 'percentage_check_failed', 'critical',
                         "Failed to validate percentage ranges",
                         {'error': str(e)})
        
        # Check NULL data patterns
        try:
            with self.app.app_context():
                null_stats = db.session.execute(db.text('''
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN English_Proficiency IS NULL THEN 1 ELSE 0 END) as null_english,
                    SUM(CASE WHEN Performance_Level_1_Percent IS NULL THEN 1 ELSE 0 END) as null_perf1,
                    SUM(CASE WHEN Performance_Level_2_Percent IS NULL THEN 1 ELSE 0 END) as null_perf2,
                    SUM(CASE WHEN Performance_Level_3_Percent IS NULL THEN 1 ELSE 0 END) as null_perf3,
                    SUM(CASE WHEN Performance_Level_4_Percent IS NULL THEN 1 ELSE 0 END) as null_perf4,
                    SUM(CASE WHEN Performance_Level_5_Percent IS NULL THEN 1 ELSE 0 END) as null_perf5
                FROM Performance_Data
                ''')).fetchone()
            total = null_stats[0]
            
            null_percentages = {
                'English_Proficiency': (null_stats[1] / total * 100) if total > 0 else 0,
                'Performance_Level_1': (null_stats[2] / total * 100) if total > 0 else 0,
                'Performance_Level_2': (null_stats[3] / total * 100) if total > 0 else 0,
                'Performance_Level_3': (null_stats[4] / total * 100) if total > 0 else 0,
                'Performance_Level_4': (null_stats[5] / total * 100) if total > 0 else 0,
                'Performance_Level_5': (null_stats[6] / total * 100) if total > 0 else 0
            }
            
            print(f"  📊 NULL Data Analysis:")
            for field, percentage in null_percentages.items():
                print(f"     {field}: {percentage:.1f}% NULL")
                
                # Flag high NULL percentages as potential issues
                if percentage > 50:
                    self.add_issue('data_quality', 'high_null_percentage', 'warning',
                                 f"High NULL percentage in {field}: {percentage:.1f}%",
                                 {'percentage': percentage, 'field': field})
            
        except Exception as e:
            self.add_issue('data_quality', 'null_analysis_failed', 'critical',
                         "Failed to analyze NULL data patterns",
                         {'error': str(e)})
    
    def validate_source_data_consistency(self):
        """Validate consistency with source data file"""
        print("\n📄 Validating Source Data Consistency...")
        
        try:
            # Count records in source file
            literacy_data_file = '/Users/kershadwooten/Desktop/Literacy-Database/literacy_data.sql'
            if os.path.exists(literacy_data_file):
                with open(literacy_data_file, 'r') as f:
                    content = f.read()
                    source_records = content.count('INSERT INTO')
                
                # Get database record count
                with self.app.app_context():
                    db_records = db.session.execute(db.text("SELECT COUNT(*) FROM Performance_Data")).scalar()
                
                print(f"  📊 Source file records: {source_records:,}")
                print(f"  📊 Database records: {db_records:,}")
                
                if abs(source_records - db_records) > 100:  # Allow small variance due to normalization
                    self.add_issue('data_quality', 'record_count_mismatch', 'warning',
                                 f"Significant difference between source ({source_records}) and database ({db_records}) record counts",
                                 {'source_count': source_records, 'db_count': db_records})
                else:
                    print(f"  ✓ Record counts are consistent")
            else:
                self.add_issue('data_quality', 'source_file_missing', 'warning',
                             "Source data file not found for comparison",
                             {'file_path': literacy_data_file})
                
        except Exception as e:
            self.add_issue('data_quality', 'source_validation_failed', 'warning',
                         "Failed to validate against source data",
                         {'error': str(e)})
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("📋 VALIDATION REPORT SUMMARY")
        print("="*60)
        
        summary = self.validation_results['summary']
        print(f"🕐 Validation completed: {self.validation_results['timestamp']}")
        print(f"📊 Total issues found: {summary['total_issues']}")
        print(f"🚨 Critical issues: {summary['critical_issues']}")
        print(f"⚠️  Warnings: {summary['warnings']}")
        
        if summary['total_issues'] == 0:
            print("\n🎉 Database validation passed with no issues!")
        else:
            print(f"\n📝 Issues by category:")
            
            for category, issues in self.validation_results.items():
                if category in ['timestamp', 'summary'] or not issues:
                    continue
                    
                print(f"\n{category.replace('_', ' ').title()}:")
                for issue in issues:
                    severity_emoji = "🚨" if issue['severity'] == 'critical' else "⚠️"
                    print(f"  {severity_emoji} {issue['description']}")
                    if issue['details']:
                        print(f"     Details: {issue['details']}")
        
        # Save detailed report to file
        report_file = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join('/Users/kershadwooten/Desktop/Literacy-Database/dev', report_file)
        
        try:
            with open(report_path, 'w') as f:
                json.dump(self.validation_results, f, indent=2)
            print(f"\n💾 Detailed report saved to: {report_path}")
        except Exception as e:
            print(f"\n❌ Failed to save report: {e}")
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print("🚀 Starting Database Validation Suite")
        print("="*60)
        
        if not self.connect():
            return False
        
        try:
            self.validate_schema_consistency()
            self.validate_data_integrity()
            self.validate_data_quality()
            self.validate_source_data_consistency()
            self.generate_report()
            
            return self.validation_results['summary']['critical_issues'] == 0
            
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            return False
        finally:
            self.close()

def main():
    """Main validation function"""
    validator = DatabaseValidator()
    success = validator.run_full_validation()
    
    if success:
        print("\n✅ Validation completed successfully")
        exit(0)
    else:
        print("\n❌ Validation completed with critical issues")
        exit(1)

if __name__ == "__main__":
    main()