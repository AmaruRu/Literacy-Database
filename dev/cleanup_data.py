#!/usr/bin/env python3
"""
Data Cleanup Script for Mississippi Literacy Database
Handles NULL values, sub-1% data standardization, and data quality improvements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import create_website, db
from project.models import Districts, Schools, Subgroups, PerformanceData, TeacherQuality, NAEPAssessments
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class DataCleaner:
    def __init__(self):
        self.app = None
        self.cleanup_stats = {
            'timestamp': datetime.now().isoformat(),
            'operations': [],
            'summary': {
                'total_operations': 0,
                'records_affected': 0,
                'errors': 0
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
    
    def log_operation(self, operation, description, records_affected=0, error=None):
        """Log cleanup operation"""
        op = {
            'operation': operation,
            'description': description,
            'records_affected': records_affected,
            'timestamp': datetime.now().isoformat(),
            'error': str(error) if error else None
        }
        
        self.cleanup_stats['operations'].append(op)
        self.cleanup_stats['summary']['total_operations'] += 1
        self.cleanup_stats['summary']['records_affected'] += records_affected
        
        if error:
            self.cleanup_stats['summary']['errors'] += 1
            print(f"❌ {operation}: {error}")
        else:
            print(f"✅ {operation}: {description} ({records_affected} records)")
    
    def standardize_sub_one_percent_values(self):
        """
        Standardize handling of sub-1% values
        Options:
        1. Convert NULL to 0.5 (midpoint estimate)
        2. Convert NULL to 0.0 (conservative estimate)  
        3. Leave as NULL but add metadata
        
        We'll use option 2 (conservative) for now
        """
        print("\n🔧 Standardizing Sub-1% Values...")
        
        try:
            with self.app.app_context():
                # Get count of NULL English_Proficiency records that might be <1%
                null_count = db.session.execute(db.text('''
                    SELECT COUNT(*) FROM Performance_Data 
                    WHERE English_Proficiency IS NULL
                ''')).scalar()
                
                print(f"Found {null_count:,} NULL English_Proficiency records")
                
                # Option: Convert NULL to 0.0 for percentage fields (conservative approach)
                # This assumes NULL values represent <1% cases
                
                # Update English_Proficiency
                result = db.session.execute(db.text('''
                    UPDATE Performance_Data 
                    SET English_Proficiency = 0.0 
                    WHERE English_Proficiency IS NULL
                '''))
                
                english_updated = result.rowcount
                
                # Update Performance Level percentages
                perf_level_fields = [
                    'Performance_Level_1_Percent',
                    'Performance_Level_2_Percent', 
                    'Performance_Level_3_Percent',
                    'Performance_Level_4_Percent',
                    'Performance_Level_5_Percent'
                ]
                
                total_perf_updated = 0
                for field in perf_level_fields:
                    result = db.session.execute(db.text(f'''
                        UPDATE Performance_Data 
                        SET {field} = 0.0 
                        WHERE {field} IS NULL
                    '''))
                    total_perf_updated += result.rowcount
                
                db.session.commit()
                
                self.log_operation('standardize_null_percentages', 
                                 f'Converted NULL percentages to 0.0 (conservative sub-1% estimate)',
                                 english_updated + total_perf_updated)
                
        except Exception as e:
            db.session.rollback()
            self.log_operation('standardize_null_percentages', 
                             'Failed to standardize NULL percentages', error=e)
    
    def add_data_quality_metadata(self):
        """Add metadata to track data quality flags"""
        print("\n📋 Adding Data Quality Metadata...")
        
        try:
            with self.app.app_context():
                # Check if we need to add a data quality flag column
                columns = db.session.execute(db.text('DESCRIBE Performance_Data')).fetchall()
                column_names = [col[0] for col in columns]
                
                if 'Data_Quality_Flags' not in column_names:
                    # Add a column to track data quality issues
                    db.session.execute(db.text('''
                        ALTER TABLE Performance_Data 
                        ADD COLUMN Data_Quality_Flags TEXT DEFAULT NULL
                    '''))
                    
                    # Flag records that likely had sub-1% values
                    result = db.session.execute(db.text('''
                        UPDATE Performance_Data 
                        SET Data_Quality_Flags = 'sub_one_percent' 
                        WHERE English_Proficiency = 0.0 
                           OR Performance_Level_1_Percent = 0.0
                           OR Performance_Level_2_Percent = 0.0
                           OR Performance_Level_3_Percent = 0.0
                           OR Performance_Level_4_Percent = 0.0
                           OR Performance_Level_5_Percent = 0.0
                    '''))
                    
                    db.session.commit()
                    
                    self.log_operation('add_quality_metadata', 
                                     'Added Data_Quality_Flags column and flagged sub-1% records',
                                     result.rowcount)
                else:
                    print("  ℹ️ Data_Quality_Flags column already exists")
                    
        except Exception as e:
            db.session.rollback()
            self.log_operation('add_quality_metadata', 
                             'Failed to add data quality metadata', error=e)
    
    def validate_percentage_constraints(self):
        """Ensure all percentages are within 0-100 range"""
        print("\n✅ Validating Percentage Constraints...")
        
        try:
            with self.app.app_context():
                # Check for any values outside 0-100 range
                invalid_count = db.session.execute(db.text('''
                    SELECT COUNT(*) FROM Performance_Data 
                    WHERE English_Proficiency > 100 OR English_Proficiency < 0
                       OR Performance_Level_1_Percent > 100 OR Performance_Level_1_Percent < 0
                       OR Performance_Level_2_Percent > 100 OR Performance_Level_2_Percent < 0
                       OR Performance_Level_3_Percent > 100 OR Performance_Level_3_Percent < 0
                       OR Performance_Level_4_Percent > 100 OR Performance_Level_4_Percent < 0
                       OR Performance_Level_5_Percent > 100 OR Performance_Level_5_Percent < 0
                ''')).scalar()
                
                if invalid_count > 0:
                    self.log_operation('validate_percentages', 
                                     f'Found {invalid_count} records with invalid percentages',
                                     error=f'{invalid_count} constraint violations')
                else:
                    self.log_operation('validate_percentages', 
                                     'All percentage values are within valid range (0-100)', 0)
                    
        except Exception as e:
            self.log_operation('validate_percentages', 
                             'Failed to validate percentage constraints', error=e)
    
    def optimize_database_performance(self):
        """Add missing indexes and optimize queries"""
        print("\n⚡ Optimizing Database Performance...")
        
        try:
            with self.app.app_context():
                # Add composite indexes for common query patterns
                index_queries = [
                    'CREATE INDEX idx_perf_district_subgroup ON Performance_Data(District_ID, Subgroup_ID)',
                    'CREATE INDEX idx_perf_school_subgroup ON Performance_Data(School_ID, Subgroup_ID)',
                    'CREATE INDEX idx_perf_year_type ON Performance_Data(School_Year, Assessment_Type)',
                    'CREATE INDEX idx_subgroup_category ON Subgroups(Subgroup_Category)'
                ]
                
                indexes_created = 0
                for query in index_queries:
                    try:
                        db.session.execute(db.text(query))
                        indexes_created += 1
                    except Exception as idx_error:
                        # Index might already exist
                        if 'already exists' not in str(idx_error).lower():
                            print(f"  ⚠️ Index creation warning: {idx_error}")
                
                db.session.commit()
                
                self.log_operation('optimize_indexes', 
                                 f'Created/verified {indexes_created} performance indexes',
                                 indexes_created)
                
        except Exception as e:
            db.session.rollback()
            self.log_operation('optimize_indexes', 
                             'Failed to optimize database indexes', error=e)
    
    def generate_cleanup_report(self):
        """Generate cleanup summary report"""
        print("\n" + "="*60)
        print("🧹 DATA CLEANUP REPORT SUMMARY")
        print("="*60)
        
        summary = self.cleanup_stats['summary']
        print(f"🕐 Cleanup completed: {self.cleanup_stats['timestamp']}")
        print(f"📊 Total operations: {summary['total_operations']}")
        print(f"📝 Records affected: {summary['records_affected']:,}")
        print(f"❌ Errors: {summary['errors']}")
        
        if summary['errors'] == 0:
            print("\n🎉 Data cleanup completed successfully!")
        else:
            print(f"\n⚠️ Cleanup completed with {summary['errors']} errors")
        
        print(f"\n📋 Operations performed:")
        for op in self.cleanup_stats['operations']:
            status = "✅" if not op['error'] else "❌"
            print(f"  {status} {op['operation']}: {op['description']}")
            if op['error']:
                print(f"     Error: {op['error']}")
        
        # Save detailed report
        import json
        report_file = f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join('/Users/kershadwooten/Desktop/Literacy-Database/dev', report_file)
        
        try:
            with open(report_path, 'w') as f:
                json.dump(self.cleanup_stats, f, indent=2)
            print(f"\n💾 Detailed report saved to: {report_path}")
        except Exception as e:
            print(f"\n❌ Failed to save report: {e}")
    
    def run_full_cleanup(self):
        """Run complete data cleanup suite"""
        print("🚀 Starting Data Cleanup Suite")
        print("="*60)
        
        if not self.connect():
            return False
        
        try:
            # Run cleanup operations
            self.standardize_sub_one_percent_values()
            self.add_data_quality_metadata()
            self.validate_percentage_constraints()
            self.optimize_database_performance()
            
            # Generate report
            self.generate_cleanup_report()
            
            return self.cleanup_stats['summary']['errors'] == 0
            
        except Exception as e:
            print(f"❌ Cleanup failed with error: {e}")
            return False

def main():
    """Main cleanup function"""
    cleaner = DataCleaner()
    success = cleaner.run_full_cleanup()
    
    if success:
        print("\n✅ Data cleanup completed successfully")
        exit(0)
    else:
        print("\n❌ Data cleanup completed with errors")
        exit(1)

if __name__ == "__main__":
    main()