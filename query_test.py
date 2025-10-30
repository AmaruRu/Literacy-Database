from project import create_website
from project.models import Districts, Schools, PerformanceData

  # Create Flask app
app = create_website()

# All database queries must be inside app context
with app.app_context():
    # Get all districts
    districts = Districts.query.all()

    # Get specific district by ID
    district = Districts.query.get(1)

    # Filter districts by name
    district = Districts.query.filter_by(District_Name='Jackson Public School District').first()

    # Get performance data with filters
    performance = PerformanceData.query.filter(
        PerformanceData.School_Year == 2023,
        PerformanceData.English_Proficiency > 50.0
    ).all()

    # Get schools in specific district
    schools = Schools.query.filter_by(District_ID=1).all()

    # Print results
    for district in districts:
          print(f"District: {district.District_Name}")