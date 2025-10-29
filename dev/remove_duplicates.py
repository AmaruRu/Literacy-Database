#!/usr/bin/env python3
"""
Remove Duplicate Records Script for Mississippi Literacy Database
Identifies and removes duplicate records while preserving data integrity
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import create_website, db
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class DuplicateRemover:
    def __init__(self):
        self.app = None
        self.removal_stats = {
            'timestamp': datetime.now().isoformat(),
            'before_count': 0,
            'after_count': 0,
            'duplicates_removed': 0,
            'operations': []
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
    
    def analyze_duplicates(self):
        """Analyze duplicate patterns before removal"""
        print("\n🔍 Analyzing Duplicate Patterns...")
        
        with self.app.app_context():
            # Get initial count
            total_before = db.session.execute(db.text('SELECT COUNT(*) FROM Performance_Data')).scalar()
            self.removal_stats['before_count'] = total_before
            print(f"Total records before cleanup: {total_before:,}")
            
            # Analyze duplicates by assessment type
            duplicates_by_type = db.session.execute(db.text('''
                SELECT Assessment_Type, 
                       COUNT(*) as total_records,
                       COUNT(DISTINCT School_Year, District_ID, School_ID, Subgroup_ID, Grade_Level) as unique_records,
                       COUNT(*) - COUNT(DISTINCT School_Year, District_ID, School_ID, Subgroup_ID, Grade_Level) as duplicates
                FROM Performance_Data 
                GROUP BY Assessment_Type
                ORDER BY duplicates DESC
            ''')).fetchall()
            
            print(f"\n📊 Duplicate Analysis by Assessment Type:")
            total_duplicates = 0
            for row in duplicates_by_type:
                duplicates = row[3]
                total_duplicates += duplicates
                print(f"  {row[0]:10s}: {row[1]:6,} total, {row[2]:6,} unique, {duplicates:6,} duplicates")
            
            print(f"\nTotal duplicates to remove: {total_duplicates:,}")
            return total_duplicates > 0
    
    def remove_duplicates(self):
        """Remove duplicate records keeping only one copy of each unique combination"""
        print("\n🧹 Removing Duplicate Records...")
        
        try:
            with self.app.app_context():
                # Create a temporary table with unique records
                print("Creating temporary table with unique records...")
                
                # Step 1: Create temporary table with unique records (keeping the first occurrence)
                db.session.execute(db.text('''
                    CREATE TEMPORARY TABLE Performance_Data_Unique AS
                    SELECT MIN(Performance_ID) as keep_id,
                           School_Year, District_ID, School_ID, Subgroup_ID, Grade_Level, Assessment_Type,
                           COUNT(*) as duplicate_count
                    FROM Performance_Data
                    GROUP BY School_Year, District_ID, School_ID, Subgroup_ID, Grade_Level, Assessment_Type
                '''))
                
                # Step 2: Count records to be kept
                records_to_keep = db.session.execute(db.text('''
                    SELECT COUNT(*) FROM Performance_Data_Unique
                ''')).scalar()
                
                print(f"Records to keep: {records_to_keep:,}")
                
                # Step 3: Count total duplicates that will be removed
                total_duplicates = db.session.execute(db.text('''
                    SELECT SUM(duplicate_count - 1) FROM Performance_Data_Unique
                    WHERE duplicate_count > 1
                ''')).scalar() or 0
                
                print(f"Duplicates to remove: {total_duplicates:,}")
                
                # Step 4: Remove duplicates (keep only the records with IDs in the temp table)
                result = db.session.execute(db.text('''
                    DELETE FROM Performance_Data 
                    WHERE Performance_ID NOT IN (
                        SELECT keep_id FROM Performance_Data_Unique
                    )
                '''))
                
                removed_count = result.rowcount
                db.session.commit()
                
                # Step 5: Verify results
                final_count = db.session.execute(db.text('SELECT COUNT(*) FROM Performance_Data')).scalar()
                
                self.removal_stats['after_count'] = final_count
                self.removal_stats['duplicates_removed'] = removed_count
                
                print(f"✅ Successfully removed {removed_count:,} duplicate records")
                print(f"Final record count: {final_count:,}")
                
                # Drop temporary table
                db.session.execute(db.text('DROP TEMPORARY TABLE Performance_Data_Unique'))
                
                return True
                
        except Exception as e:
            print(f"❌ Error removing duplicates: {e}")
            db.session.rollback()
            return False
    
    def verify_integrity(self):
        """Verify data integrity after duplicate removal"""
        print("\n✅ Verifying Data Integrity...")
        
        with self.app.app_context():
            # Check for remaining duplicates
            remaining_duplicates = db.session.execute(db.text('''
                SELECT COUNT(*) - COUNT(DISTINCT School_Year, District_ID, School_ID, Subgroup_ID, Grade_Level, Assessment_Type)
                FROM Performance_Data
            ''')).scalar()
            
            if remaining_duplicates == 0:
                print("✅ No remaining duplicates found")
            else:
                print(f"⚠️ {remaining_duplicates} duplicates still remain")
            
            # Check referential integrity
            orphaned_records = db.session.execute(db.text('''
                SELECT COUNT(*) FROM Performance_Data p
                LEFT JOIN Districts d ON p.District_ID = d.District_ID
                LEFT JOIN Subgroups s ON p.Subgroup_ID = s.Subgroup_ID
                WHERE (p.District_ID IS NOT NULL AND d.District_ID IS NULL)
                   OR s.Subgroup_ID IS NULL
            ''')).scalar()
            
            if orphaned_records == 0:
                print("✅ Referential integrity maintained")
            else:
                print(f"⚠️ {orphaned_records} orphaned records found")
            
            # Show final statistics
            final_stats = db.session.execute(db.text('''
                SELECT Assessment_Type, COUNT(*) as count
                FROM Performance_Data
                GROUP BY Assessment_Type
                ORDER BY count DESC
            ''')).fetchall()
            
            print(f"\n📊 Final Record Counts by Assessment Type:")
            for row in final_stats:
                print(f"  {row[0]:10s}: {row[1]:6,} records")
    
    def generate_report(self):
        """Generate removal summary report"""
        print("\n" + "="*60)
        print("🧹 DUPLICATE REMOVAL REPORT")
        print("="*60)
        
        stats = self.removal_stats
        print(f"🕐 Cleanup completed: {stats['timestamp']}")
        print(f"📊 Records before: {stats['before_count']:,}")
        print(f"📊 Records after: {stats['after_count']:,}")
        print(f"🗑️ Duplicates removed: {stats['duplicates_removed']:,}")
        
        percentage_reduction = (stats['duplicates_removed'] / stats['before_count'] * 100) if stats['before_count'] > 0 else 0
        print(f"📉 Reduction: {percentage_reduction:.1f}%")
        
        expected_final = 18162  # Expected based on source file
        if abs(stats['after_count'] - expected_final) <= 200:  # Allow small variance
            print(f"🎯 Final count ({stats['after_count']:,}) is now close to expected ({expected_final:,})")
        else:
            print(f"⚠️ Final count ({stats['after_count']:,}) still differs from expected ({expected_final:,})")
        
        # Save report
        import json
        report_file = f"duplicate_removal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join('/Users/kershadwooten/Desktop/Literacy-Database/dev', report_file)
        
        try:
            with open(report_path, 'w') as f:
                json.dump(self.removal_stats, f, indent=2)
            print(f"\n💾 Report saved to: {report_path}")
        except Exception as e:
            print(f"\n❌ Failed to save report: {e}")
    
    def run_duplicate_removal(self):
        """Run complete duplicate removal process"""
        print("🚀 Starting Duplicate Removal Process")
        print("="*60)
        
        if not self.connect():
            return False
        
        try:
            # Analyze duplicates
            has_duplicates = self.analyze_duplicates()
            
            if not has_duplicates:
                print("\n✅ No duplicates found - database is clean!")
                return True
            
            # Confirm before proceeding
            print(f"\n⚠️ This will permanently remove duplicate records.")
            print(f"📝 Original data will be preserved by keeping the first occurrence of each unique combination.")
            
            # Remove duplicates
            success = self.remove_duplicates()
            
            if success:
                # Verify integrity
                self.verify_integrity()
                
                # Generate report
                self.generate_report()
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Duplicate removal failed: {e}")
            return False

def main():
    """Main function"""
    remover = DuplicateRemover()
    success = remover.run_duplicate_removal()
    
    if success:
        print("\n✅ Duplicate removal completed successfully")
        exit(0)
    else:
        print("\n❌ Duplicate removal failed")
        exit(1)

if __name__ == "__main__":
    main()