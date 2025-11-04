from project import create_website, db # Import the create_website function and db object
from project.models import Districts, Schools, PerformanceData, Subgroups # Import models to be queried
from sqlalchemy import func

# Create Flask app
app = create_website()

# All database queries must be inside app context
with app.app_context():
    # Query 1: Find all schools in Rankin County
    print("Query 1: Schools in Rankin County")
    rankin_district = Districts.query.filter(Districts.District_Name.like('%Rankin%')).first()
    if rankin_district:
        rankin_schools = Schools.query.filter_by(District_ID=rankin_district.District_ID).all()
        print(f"District: {rankin_district.District_Name}")
        print(f"Total schools: {len(rankin_schools)}")
        for school in rankin_schools:
            print(f"  - {school.School_Name}")
    else:
        print("Rankin County district not found")
    print()
    
    # Query 2: What are the top 5 performing districts by English proficiency? 
    print("Query 2: Top 5 Performing Districts by English Proficiency (Most Recent Year, All Students)")
    
    # Get the 'All' subgroup for fair comparison
    all_subgroup = Subgroups.query.filter_by(Subgroup_Name='All').first()
    
    # Get the most recent year in the data
    recent_year = db.session.query(func.max(PerformanceData.School_Year)).scalar()
    
    if all_subgroup and recent_year:
        top_districts = db.session.query(
            Districts.District_Name,
            func.avg(PerformanceData.English_Proficiency).label('avg_proficiency'),
            func.count(PerformanceData.Performance_ID).label('record_count')
        ).join(PerformanceData).filter(
            PerformanceData.English_Proficiency.isnot(None),
            PerformanceData.School_Year == recent_year,
            PerformanceData.Subgroup_ID == all_subgroup.Subgroup_ID,
            PerformanceData.Assessment_Type == 'District'
        ).group_by(Districts.District_ID).order_by(
            func.avg(PerformanceData.English_Proficiency).desc()
        ).limit(5).all()
        
        print(f"Data from {recent_year} school year:")
        for i, (district_name, avg_prof, count) in enumerate(top_districts, 1):
            print(f"  {i}. {district_name}: {avg_prof:.1f}% proficiency ({count} records)")
    else:
        print("  Could not find 'All' subgroup or recent year data")
    print()
    
    # Query 3: What are the lowest performing districts?
    print("Query 3: Lowest 5 Performing Districts by English Proficiency (Most Recent Year, All Students)")
    
    if all_subgroup and recent_year:
        lowest_districts = db.session.query(
            Districts.District_Name,
            func.avg(PerformanceData.English_Proficiency).label('avg_proficiency'),
            func.count(PerformanceData.Performance_ID).label('record_count')
        ).join(PerformanceData).filter(
            PerformanceData.English_Proficiency.isnot(None),
            PerformanceData.School_Year == recent_year,
            PerformanceData.Subgroup_ID == all_subgroup.Subgroup_ID,
            PerformanceData.Assessment_Type == 'District'
        ).group_by(Districts.District_ID).order_by(
            func.avg(PerformanceData.English_Proficiency).asc()
        ).limit(5).all()
        
        print(f"Data from {recent_year} school year:")
        for i, (district_name, avg_prof, count) in enumerate(lowest_districts, 1):
            print(f"  {i}. {district_name}: {avg_prof:.1f}% proficiency ({count} records)")
    else:
        print("  Could not find 'All' subgroup or recent year data")
    print()