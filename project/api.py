"""
API endpoints for Mississippi Literacy Database
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_
from .models import Districts, Schools, Subgroups, PerformanceData, TeacherQuality, NAEPAssessments, Books
from . import db

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/districts', methods=['GET'])
def get_districts():
    """Get all districts with basic information"""
    try:
        districts = Districts.query.all()
        
        result = []
        for district in districts:
            result.append({
                'district_id': district.District_ID,
                'district_number': district.District_Number,
                'district_name': district.District_Name,
                'school_count': len(district.schools),
                'created_at': district.Created_At.isoformat() if district.Created_At else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/districts/<int:district_id>', methods=['GET'])
def get_district_detail(district_id):
    """Get detailed information for a specific district"""
    try:
        district = Districts.query.get_or_404(district_id)
        
        # Get performance summary for 'All' students
        all_subgroup = Subgroups.query.filter_by(Subgroup_Name='All').first()
        
        performance_summary = None
        if all_subgroup:
            perf_data = PerformanceData.query.filter_by(
                District_ID=district_id,
                Subgroup_ID=all_subgroup.Subgroup_ID
            ).filter(PerformanceData.English_Proficiency.isnot(None)).first()
            
            if perf_data:
                performance_summary = {
                    'english_proficiency': float(perf_data.English_Proficiency) if perf_data.English_Proficiency else None,
                    'english_growth': float(perf_data.English_Growth) if perf_data.English_Growth else None,
                    'assessment_type': perf_data.Assessment_Type,
                    'school_year': perf_data.School_Year
                }
        
        result = {
            'district_id': district.District_ID,
            'district_number': district.District_Number,
            'district_name': district.District_Name,
            'school_count': len(district.schools),
            'schools': [
                {
                    'school_id': school.School_ID,
                    'school_name': school.School_Name,
                    'school_number': school.School_Number
                }
                for school in district.schools
            ],
            'performance_summary': performance_summary,
            'created_at': district.Created_At.isoformat() if district.Created_At else None
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/schools', methods=['GET'])
def get_schools():
    """Get all schools with optional district filtering"""
    try:
        district_id = request.args.get('district_id', type=int)
        
        query = Schools.query.join(Districts)
        
        if district_id:
            query = query.filter(Schools.District_ID == district_id)
        
        schools = query.all()
        
        result = []
        for school in schools:
            result.append({
                'school_id': school.School_ID,
                'school_number': school.School_Number,
                'school_name': school.School_Name,
                'district_id': school.District_ID,
                'district_name': school.district.District_Name
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/subgroups', methods=['GET'])
def get_subgroups():
    """Get all subgroups"""
    try:
        subgroups = Subgroups.query.all()
        
        result = []
        for subgroup in subgroups:
            result.append({
                'subgroup_id': subgroup.Subgroup_ID,
                'subgroup_name': subgroup.Subgroup_Name,
                'subgroup_category': subgroup.Subgroup_Category,
                'record_count': len(subgroup.performance_data)
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/performance', methods=['GET'])
def get_performance_data():
    """Get performance data with filtering options"""
    try:
        # Query parameters
        district_id = request.args.get('district_id', type=int)
        school_id = request.args.get('school_id', type=int)
        subgroup_id = request.args.get('subgroup_id', type=int)
        school_year = request.args.get('school_year', type=int)
        limit = request.args.get('limit', default=100, type=int)
        
        # Build query
        query = PerformanceData.query.join(Subgroups)
        
        # Add joins for names
        if district_id or not school_id:
            query = query.outerjoin(Districts)
        if school_id or district_id:
            query = query.outerjoin(Schools)
        
        # Apply filters
        if district_id:
            query = query.filter(PerformanceData.District_ID == district_id)
        if school_id:
            query = query.filter(PerformanceData.School_ID == school_id)
        if subgroup_id:
            query = query.filter(PerformanceData.Subgroup_ID == subgroup_id)
        if school_year:
            query = query.filter(PerformanceData.School_Year == school_year)
        
        # Limit results
        performance_data = query.limit(limit).all()
        
        result = []
        for perf in performance_data:
            result.append({
                'performance_id': perf.Performance_ID,
                'school_year': perf.School_Year,
                'district_name': perf.district.District_Name if perf.district else None,
                'school_name': perf.school.School_Name if perf.school else None,
                'subgroup_name': perf.subgroup.Subgroup_Name,
                'grade_level': perf.Grade_Level,
                'assessment_type': perf.Assessment_Type,
                'english_proficiency': float(perf.English_Proficiency) if perf.English_Proficiency else None,
                'english_growth': float(perf.English_Growth) if perf.English_Growth else None,
                'performance_levels': {
                    'level_1': {
                        'percent': float(perf.Performance_Level_1_Percent) if perf.Performance_Level_1_Percent else None,
                        'students': perf.Performance_Level_1_Students
                    },
                    'level_2': {
                        'percent': float(perf.Performance_Level_2_Percent) if perf.Performance_Level_2_Percent else None,
                        'students': perf.Performance_Level_2_Students
                    },
                    'level_3': {
                        'percent': float(perf.Performance_Level_3_Percent) if perf.Performance_Level_3_Percent else None,
                        'students': perf.Performance_Level_3_Students
                    },
                    'level_4': {
                        'percent': float(perf.Performance_Level_4_Percent) if perf.Performance_Level_4_Percent else None,
                        'students': perf.Performance_Level_4_Students
                    },
                    'level_5': {
                        'percent': float(perf.Performance_Level_5_Percent) if perf.Performance_Level_5_Percent else None,
                        'students': perf.Performance_Level_5_Students
                    }
                },
                'chronic_absenteeism': float(perf.Chronic_Absenteeism_Percent) if perf.Chronic_Absenteeism_Percent else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'filters_applied': {
                'district_id': district_id,
                'school_id': school_id,
                'subgroup_id': subgroup_id,
                'school_year': school_year,
                'limit': limit
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analytics/district-rankings', methods=['GET'])
def get_district_rankings():
    """Get district rankings by English proficiency"""
    try:
        # Get 'All' subgroup for fair comparison
        all_subgroup = Subgroups.query.filter_by(Subgroup_Name='All').first()
        
        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404
        
        # Calculate average English proficiency by district
        rankings = db.session.query(
            Districts.District_Name,
            Districts.District_ID,
            func.avg(PerformanceData.English_Proficiency).label('avg_english_proficiency'),
            func.count(PerformanceData.Performance_ID).label('record_count')
        ).join(PerformanceData).filter(
            PerformanceData.Subgroup_ID == all_subgroup.Subgroup_ID,
            PerformanceData.English_Proficiency.isnot(None)
        ).group_by(
            Districts.District_ID, Districts.District_Name
        ).order_by(
            func.avg(PerformanceData.English_Proficiency).desc()
        ).limit(20).all()
        
        result = []
        for rank, (district_name, district_id, avg_proficiency, record_count) in enumerate(rankings, 1):
            result.append({
                'rank': rank,
                'district_id': district_id,
                'district_name': district_name,
                'average_english_proficiency': round(float(avg_proficiency), 1),
                'record_count': record_count
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analytics/subgroup-performance', methods=['GET'])
def get_subgroup_performance():
    """Get performance comparison across subgroups"""
    try:
        district_id = request.args.get('district_id', type=int)
        
        # Build query for subgroup performance comparison
        query = db.session.query(
            Subgroups.Subgroup_Name,
            Subgroups.Subgroup_Category,
            func.avg(PerformanceData.English_Proficiency).label('avg_english_proficiency'),
            func.count(PerformanceData.Performance_ID).label('record_count')
        ).join(PerformanceData).filter(
            PerformanceData.English_Proficiency.isnot(None)
        )
        
        if district_id:
            query = query.filter(PerformanceData.District_ID == district_id)
        
        subgroup_performance = query.group_by(
            Subgroups.Subgroup_ID, Subgroups.Subgroup_Name, Subgroups.Subgroup_Category
        ).order_by(
            Subgroups.Subgroup_Category, func.avg(PerformanceData.English_Proficiency).desc()
        ).all()
        
        result = []
        for subgroup_name, category, avg_proficiency, record_count in subgroup_performance:
            result.append({
                'subgroup_name': subgroup_name,
                'subgroup_category': category,
                'average_english_proficiency': round(float(avg_proficiency), 1) if avg_proficiency else None,
                'record_count': record_count
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'district_id': district_id
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/map/districts', methods=['GET'])
def get_map_districts():
    """Get district literacy data for map visualization (grouped by county)"""
    try:
        # Mapping of city/district name keywords to counties
        # Uses partial matching - if keyword appears in district name, maps to county
        DISTRICT_TO_COUNTY = {
            'Aberdeen': 'Monroe', 'Alcorn': 'Alcorn', 'Amory': 'Monroe', 'Baldwyn': 'Lee',
            'Bay St Louis': 'Hancock', 'Biloxi': 'Harrison', 'Booneville': 'Prentiss',
            'Brookhaven': 'Lincoln', 'Canton': 'Madison', 'Clarksdale Municipal': 'Coahoma',
            'Clarksdale Collegiate': 'Coahoma', 'Cleveland': 'Bolivar', 'Clinton': 'Hinds',
            'Coffeeville': 'Yalobusha', 'Columbia': 'Marion', 'Columbus': 'Lowndes', 'Corinth': 'Alcorn',
            'East Jasper': 'Jasper', 'East Tallahatchie': 'Tallahatchie',
            'Enterprise': 'Clarke', 'Forest': 'Scott', 'Greenville': 'Washington',
            'Greenwood': 'Leflore', 'Grenada': 'Grenada', 'Gulfport': 'Harrison',
            'Hattiesburg': 'Forrest', 'Hazlehurst': 'Copiah', 'Hollandale': 'Washington',
            'Holly Springs': 'Marshall', 'Holmes Consolidated': 'Holmes', 'Jackson Public': 'Hinds',
            'Kosciusko': 'Attala', 'Laurel': 'Jones', 'Leland': 'Washington', 'Long Beach': 'Harrison',
            'Louisville': 'Winston', 'Mccomb': 'Pike', 'Meridian': 'Lauderdale',
            'Moss Point': 'Jackson', 'Natchez': 'Adams', 'Nettleton': 'Lee',
            'New Albany': 'Union', 'Newton Municipal': 'Newton',
            'Ocean Springs': 'Jackson', 'Okolona': 'Chickasaw', 'Oxford': 'Lafayette',
            'Pascagoula': 'Jackson', 'Pass Christian': 'Harrison', 'Pearl Public': 'Rankin',
            'Petal': 'Forrest', 'Philadelphia': 'Neshoba', 'Picayune': 'Pearl River',
            'Pontotoc City': 'Pontotoc', 'Poplarville': 'Pearl River', 'Quitman School': 'Clarke',
            'Richton': 'Perry', 'Senatobia': 'Tate', 'South Delta': 'Sharkey',
            'Starkville': 'Oktibbeha', 'Tupelo': 'Lee',
            'Union Public': 'Newton', 'Vicksburg': 'Warren', 'Water Valley': 'Yalobusha',
            'West Point': 'Clay', 'Western Line': 'DeSoto', 'Winona': 'Montgomery',
            'Yazoo City': 'Yazoo', 'Ambition Preparatory': 'Hinds',
            'Joel E. Smilow': 'Harrison', 'Leflore Legacy': 'Leflore', 'Midtown Public': 'Hinds',
            'Reimagine Prep': 'Hinds', 'Smilow Prep': 'Harrison',
            'MS School for the Blind': 'Hinds', 'Mdhs Division': 'Hinds'
        }

        # Special handling for district names that contain county-like words
        # but aren't actually in those counties
        DISTRICT_OVERRIDES = {
            'North Panola': 'Panola',
            'South Panola': 'Panola',
            'North Pike': 'Pike',
            'South Pike': 'Pike',
            'North Tippah': 'Tippah',
            'South Tippah': 'Tippah',
            'North Bolivar': 'Bolivar',
            'West Bolivar': 'Bolivar',
            'West Jasper': 'Jasper',
            'West Tallahatchie': 'Tallahatchie'
        }

        # Get 'All' subgroup for overall performance
        all_subgroup = Subgroups.query.filter_by(Subgroup_Name='All').first()

        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404

        # Get most recent year
        most_recent_year = db.session.query(
            func.max(PerformanceData.School_Year)
        ).scalar()

        # Get district data with literacy metrics
        districts_data = db.session.query(
            Districts.District_Name,
            func.avg(PerformanceData.English_Proficiency).label('avg_english_proficiency'),
            func.avg(PerformanceData.English_Growth).label('avg_english_growth'),
            func.avg(PerformanceData.Chronic_Absenteeism_Percent).label('avg_chronic_absenteeism'),
            func.count(Schools.School_ID.distinct()).label('school_count')
        ).join(
            PerformanceData, Districts.District_ID == PerformanceData.District_ID
        ).outerjoin(
            Schools, Districts.District_ID == Schools.District_ID
        ).filter(
            PerformanceData.Subgroup_ID == all_subgroup.Subgroup_ID,
            PerformanceData.School_Year == most_recent_year
        ).group_by(
            Districts.District_ID, Districts.District_Name
        ).all()

        # Extract county name from district name and aggregate data by county
        county_data = {}
        for district_name, eng_prof, eng_growth, absenteeism, school_count in districts_data:
            county_name = None

            # First check override mapping (exact match for special cases)
            for override_key, override_county in DISTRICT_OVERRIDES.items():
                if override_key in district_name:
                    county_name = override_county
                    break

            # If not in overrides, try county-based naming
            if not county_name and 'County' in district_name:
                parts = district_name.split('County')[0].strip()
                county_parts = parts.split()
                if len(county_parts) > 1 and county_parts[0] in ['North', 'South', 'East', 'West']:
                    county_name = county_parts[-1]
                else:
                    county_name = parts

            # If still not found, try partial matching in DISTRICT_TO_COUNTY
            if not county_name:
                for key, value in DISTRICT_TO_COUNTY.items():
                    if key in district_name:
                        county_name = value
                        break

            if county_name:
                if county_name not in county_data:
                    county_data[county_name] = {
                        'districts': [],
                        'total_proficiency': 0,
                        'total_growth': 0,
                        'total_absenteeism': 0,
                        'count_proficiency': 0,
                        'count_growth': 0,
                        'count_absenteeism': 0,
                        'total_schools': 0
                    }

                county_data[county_name]['districts'].append(district_name)
                county_data[county_name]['total_schools'] += school_count if school_count else 0

                if eng_prof:
                    county_data[county_name]['total_proficiency'] += float(eng_prof)
                    county_data[county_name]['count_proficiency'] += 1
                if eng_growth:
                    county_data[county_name]['total_growth'] += float(eng_growth)
                    county_data[county_name]['count_growth'] += 1
                if absenteeism:
                    county_data[county_name]['total_absenteeism'] += float(absenteeism)
                    county_data[county_name]['count_absenteeism'] += 1

        # Calculate averages and format result
        result = {}
        for county_name, data in county_data.items():
            result[county_name] = {
                'county_name': county_name,
                'districts': data['districts'],
                'district_count': len(data['districts']),
                'english_proficiency': round(data['total_proficiency'] / data['count_proficiency'], 1) if data['count_proficiency'] > 0 else None,
                'english_growth': round(data['total_growth'] / data['count_growth'], 1) if data['count_growth'] > 0 else None,
                'chronic_absenteeism': round(data['total_absenteeism'] / data['count_absenteeism'], 1) if data['count_absenteeism'] > 0 else None,
                'school_count': data['total_schools'],
                'school_year': most_recent_year
            }

        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'school_year': most_recent_year
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/map/county/<county_name>', methods=['GET'])
def get_county_districts_schools(county_name):
    """Get detailed district and school information for a specific county"""
    try:
        # Mapping of city/district name keywords to counties (same as in /map/districts)
        DISTRICT_TO_COUNTY = {
            'Aberdeen': 'Monroe', 'Alcorn': 'Alcorn', 'Amory': 'Monroe', 'Baldwyn': 'Lee',
            'Bay St Louis': 'Hancock', 'Biloxi': 'Harrison', 'Booneville': 'Prentiss',
            'Brookhaven': 'Lincoln', 'Canton': 'Madison', 'Clarksdale Municipal': 'Coahoma',
            'Clarksdale Collegiate': 'Coahoma', 'Cleveland': 'Bolivar', 'Clinton': 'Hinds',
            'Coffeeville': 'Yalobusha', 'Columbia': 'Marion', 'Columbus': 'Lowndes', 'Corinth': 'Alcorn',
            'East Jasper': 'Jasper', 'East Tallahatchie': 'Tallahatchie',
            'Enterprise': 'Clarke', 'Forest': 'Scott', 'Greenville': 'Washington',
            'Greenwood': 'Leflore', 'Grenada': 'Grenada', 'Gulfport': 'Harrison',
            'Hattiesburg': 'Forrest', 'Hazlehurst': 'Copiah', 'Hollandale': 'Washington',
            'Holly Springs': 'Marshall', 'Holmes Consolidated': 'Holmes', 'Jackson Public': 'Hinds',
            'Kosciusko': 'Attala', 'Laurel': 'Jones', 'Leland': 'Washington', 'Long Beach': 'Harrison',
            'Louisville': 'Winston', 'Mccomb': 'Pike', 'Meridian': 'Lauderdale',
            'Moss Point': 'Jackson', 'Natchez': 'Adams', 'Nettleton': 'Lee',
            'New Albany': 'Union', 'Newton Municipal': 'Newton',
            'Ocean Springs': 'Jackson', 'Okolona': 'Chickasaw', 'Oxford': 'Lafayette',
            'Pascagoula': 'Jackson', 'Pass Christian': 'Harrison', 'Pearl Public': 'Rankin',
            'Petal': 'Forrest', 'Philadelphia': 'Neshoba', 'Picayune': 'Pearl River',
            'Pontotoc City': 'Pontotoc', 'Poplarville': 'Pearl River', 'Quitman School': 'Clarke',
            'Richton': 'Perry', 'Senatobia': 'Tate', 'South Delta': 'Sharkey',
            'Starkville': 'Oktibbeha', 'Tupelo': 'Lee',
            'Union Public': 'Newton', 'Vicksburg': 'Warren', 'Water Valley': 'Yalobusha',
            'West Point': 'Clay', 'Western Line': 'DeSoto', 'Winona': 'Montgomery',
            'Yazoo City': 'Yazoo', 'Ambition Preparatory': 'Hinds',
            'Joel E. Smilow': 'Harrison', 'Leflore Legacy': 'Leflore', 'Midtown Public': 'Hinds',
            'Reimagine Prep': 'Hinds', 'Smilow Prep': 'Harrison',
            'MS School for the Blind': 'Hinds', 'Mdhs Division': 'Hinds'
        }

        DISTRICT_OVERRIDES = {
            'North Panola': 'Panola', 'South Panola': 'Panola',
            'North Pike': 'Pike', 'South Pike': 'Pike',
            'North Tippah': 'Tippah', 'South Tippah': 'Tippah',
            'North Bolivar': 'Bolivar', 'West Bolivar': 'Bolivar',
            'West Jasper': 'Jasper', 'West Tallahatchie': 'Tallahatchie'
        }

        # Get all districts
        all_districts = Districts.query.all()

        # Find districts in this county
        county_districts = []
        for district in all_districts:
            mapped_county = None

            # Check override mapping
            for override_key, override_county in DISTRICT_OVERRIDES.items():
                if override_key in district.District_Name:
                    mapped_county = override_county
                    break

            # Try county-based naming
            if not mapped_county and 'County' in district.District_Name:
                parts = district.District_Name.split('County')[0].strip()
                county_parts = parts.split()
                if len(county_parts) > 1 and county_parts[0] in ['North', 'South', 'East', 'West']:
                    mapped_county = county_parts[-1]
                else:
                    mapped_county = parts

            # Try partial matching
            if not mapped_county:
                for key, value in DISTRICT_TO_COUNTY.items():
                    if key in district.District_Name:
                        mapped_county = value
                        break

            # If this district is in the requested county
            if mapped_county and mapped_county.lower() == county_name.lower():
                # Get schools for this district
                schools = Schools.query.filter_by(District_ID=district.District_ID).all()

                # Get performance data for this district
                all_subgroup = Subgroups.query.filter_by(Subgroup_Name='All').first()
                most_recent_year = db.session.query(func.max(PerformanceData.School_Year)).scalar()

                perf_data = PerformanceData.query.filter_by(
                    District_ID=district.District_ID,
                    Subgroup_ID=all_subgroup.Subgroup_ID,
                    School_Year=most_recent_year
                ).first()

                district_info = {
                    'district_id': district.District_ID,
                    'district_name': district.District_Name,
                    'district_number': district.District_Number,
                    'school_count': len(schools),
                    'schools': [
                        {
                            'school_id': school.School_ID,
                            'school_name': school.School_Name,
                            'school_number': school.School_Number,
                            'county_name': school.County_Name
                        }
                        for school in schools
                    ],
                    'english_proficiency': float(perf_data.English_Proficiency) if perf_data and perf_data.English_Proficiency else None,
                    'english_growth': float(perf_data.English_Growth) if perf_data and perf_data.English_Growth else None,
                    'chronic_absenteeism': float(perf_data.Chronic_Absenteeism_Percent) if perf_data and perf_data.Chronic_Absenteeism_Percent else None
                }

                county_districts.append(district_info)

        return jsonify({
            'success': True,
            'county': county_name,
            'districts': county_districts,
            'district_count': len(county_districts)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/books', methods=['GET'])
def get_books():
    """Get book recommendations with filtering options"""
    try:
        # Query parameters
        grade_level = request.args.get('grade_level', type=str)
        literature_type = request.args.get('literature_type', type=str)
        lexile_min = request.args.get('lexile_min', type=str)
        lexile_max = request.args.get('lexile_max', type=str)
        author = request.args.get('author', type=str)
        search = request.args.get('search', type=str)
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)

        # Build query
        query = Books.query

        # Apply filters
        if grade_level:
            query = query.filter(Books.Grade_Level == grade_level)

        if literature_type:
            query = query.filter(Books.Literature_Type == literature_type)

        if author:
            query = query.filter(Books.Author.ilike(f'%{author}%'))

        if search:
            query = query.filter(or_(
                Books.Title.ilike(f'%{search}%'),
                Books.Author.ilike(f'%{search}%')
            ))

        # Lexile filtering (handle numeric and special values like "BR")
        if lexile_min or lexile_max:
            # For numeric Lexile values, filter appropriately
            # Note: "BR" (Beginning Reader) is typically below 0
            if lexile_min:
                try:
                    min_val = int(lexile_min)
                    query = query.filter(
                        or_(
                            Books.Lexile.cast(db.Integer) >= min_val,
                            Books.Lexile == 'BR'
                        )
                    )
                except ValueError:
                    pass

            if lexile_max:
                try:
                    max_val = int(lexile_max)
                    query = query.filter(
                        or_(
                            Books.Lexile.cast(db.Integer) <= max_val,
                            Books.Lexile == 'BR'
                        )
                    )
                except ValueError:
                    pass

        # Get total count before pagination
        total_count = query.count()

        # Apply pagination
        books = query.order_by(Books.Grade_Level, Books.Title).limit(limit).offset(offset).all()

        result = []
        for book in books:
            result.append({
                'book_id': book.Book_ID,
                'title': book.Title,
                'author': book.Author,
                'grade_level': book.Grade_Level,
                'lexile': book.Lexile,
                'literature_type': book.Literature_Type,
                'cover_url': book.Cover_URL
            })

        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'total': total_count,
            'filters_applied': {
                'grade_level': grade_level,
                'literature_type': literature_type,
                'lexile_min': lexile_min,
                'lexile_max': lexile_max,
                'author': author,
                'search': search,
                'limit': limit,
                'offset': offset
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book_detail(book_id):
    """Get detailed information for a specific book"""
    try:
        book = Books.query.get_or_404(book_id)

        result = {
            'book_id': book.Book_ID,
            'title': book.Title,
            'author': book.Author,
            'grade_level': book.Grade_Level,
            'lexile': book.Lexile,
            'literature_type': book.Literature_Type,
            'cover_url': book.Cover_URL,
            'created_at': book.Created_At.isoformat() if book.Created_At else None
        }

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/books/grade-levels', methods=['GET'])
def get_grade_levels():
    """Get all available grade levels for books"""
    try:
        grade_levels = db.session.query(
            Books.Grade_Level,
            func.count(Books.Book_ID).label('book_count')
        ).group_by(Books.Grade_Level).order_by(
            func.field(Books.Grade_Level,
                      'Kindergarten', '1st Grade', '2nd Grade', '3rd Grade',
                      '4th Grade', '5th Grade', '6th Grade', '7th Grade',
                      '8th Grade', '9th Grade', '10th Grade', '11th Grade', '12th Grade')
        ).all()

        result = []
        for grade_level, count in grade_levels:
            result.append({
                'grade_level': grade_level,
                'book_count': count
            })

        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/books/authors', methods=['GET'])
def get_authors():
    """Get all authors with book counts"""
    try:
        limit = request.args.get('limit', default=50, type=int)

        authors = db.session.query(
            Books.Author,
            func.count(Books.Book_ID).label('book_count')
        ).group_by(Books.Author).order_by(
            func.count(Books.Book_ID).desc(),
            Books.Author
        ).limit(limit).all()

        result = []
        for author, count in authors:
            result.append({
                'author': author,
                'book_count': count
            })

        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    try:
        # Simple database connectivity check
        district_count = Districts.query.count()
        book_count = Books.query.count()

        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'district_count': district_count,
            'book_count': book_count
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500