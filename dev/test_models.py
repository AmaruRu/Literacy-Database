#!/usr/bin/env python3
"""
Test script for SQLAlchemy models
"""

from project import create_website
from project.models import Districts, Schools, Subgroups, PerformanceData

def test_models():
    """Test database models and relationships"""
    
    # Create Flask app context
    app = create_website()
    
    with app.app_context():
        try:
            # Test basic queries
            print("Testing SQLAlchemy Models...")
            print("=" * 50)
            
            # Test Districts
            district_count = Districts.query.count()
            print(f"✅ Districts table: {district_count} records")
            
            # Get a sample district
            sample_district = Districts.query.first()
            if sample_district:
                print(f"   Sample: {sample_district.District_Name}")
                print(f"   Schools: {len(sample_district.schools)}")
            
            # Test Schools
            school_count = Schools.query.count()
            print(f"✅ Schools table: {school_count} records")
            
            # Test Subgroups
            subgroup_count = Subgroups.query.count()
            print(f"✅ Subgroups table: {subgroup_count} records")
            
            # List some subgroups
            subgroups = Subgroups.query.limit(5).all()
            for sg in subgroups:
                print(f"   - {sg.Subgroup_Name} ({sg.Subgroup_Category})")
            
            # Test Performance Data
            performance_count = PerformanceData.query.count()
            print(f"✅ Performance Data table: {performance_count} records")
            
            # Test relationships
            print("\nTesting Relationships...")
            print("=" * 30)
            
            # Find a district with performance data
            district_with_data = Districts.query.join(PerformanceData).first()
            if district_with_data:
                print(f"✅ District '{district_with_data.District_Name}' has {len(district_with_data.performance_data)} performance records")
            
            # Test subgroup relationships
            all_subgroup = Subgroups.query.filter_by(Subgroup_Name='All').first()
            if all_subgroup:
                print(f"✅ 'All' subgroup has {len(all_subgroup.performance_data)} performance records")
            
            # Test advanced query - Average English proficiency by district
            print("\nSample Data Query...")
            print("=" * 25)
            
            from sqlalchemy import func
            
            avg_proficiency = PerformanceData.query.join(Districts).join(Subgroups).filter(
                Subgroups.Subgroup_Name == 'All',
                PerformanceData.English_Proficiency.isnot(None)
            ).with_entities(
                Districts.District_Name,
                func.avg(PerformanceData.English_Proficiency).label('avg_proficiency')
            ).group_by(Districts.District_ID).order_by(
                func.avg(PerformanceData.English_Proficiency).desc()
            ).limit(5).all()
            
            print("Top 5 Districts by Average English Proficiency:")
            for district_name, avg_prof in avg_proficiency:
                print(f"   {district_name}: {float(avg_prof):.1f}%")
            
            print("\n🎉 All model tests passed successfully!")
            
        except Exception as e:
            print(f"❌ Error testing models: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_models()