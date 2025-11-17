"""
API endpoints for Mississippi Literacy Database
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import func
from .models import Locations, Districts, Schools, DemographicGroups, AcademicYears, PerformanceRecords, TeacherQuality, NAEPAssessments
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
                'district_id': district.district_id,
                'district_number': district.district_number,
                'district_name': district.district_name,
                'school_count': len(district.schools),
                'county': district.location.county if district.location else None,
                'city': district.location.city if district.location else None,
                'zip_code': district.location.zip_code if district.location else None
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

@api_bp.route('/schools', methods=['GET'])
def get_schools():
    """Get all schools with optional district filtering"""
    try:
        district_id = request.args.get('district_id', type=int)
        
        query = Schools.query.join(Districts)
        
        if district_id:
            query = query.filter(Schools.district_id == district_id)
        
        schools = query.all()
        
        result = []
        for school in schools:
            result.append({
                'school_id': school.school_id,
                'school_number': school.school_number,
                'school_name': school.school_name,
                'district_id': school.district_id,
                'district_name': school.district.district_name,
                'school_type': school.school_type,
                'grade_span': school.grade_span
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

@api_bp.route('/demographic-groups', methods=['GET'])
def get_demographic_groups():
    """Get all demographic groups"""
    try:
        groups = DemographicGroups.query.all()
        
        result = []
        for group in groups:
            result.append({
                'group_id': group.group_id,
                'subgroup_name': group.subgroup_name,
                'subgroup_type': group.subgroup_type,
                'record_count': len(group.performance_records)
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
        group_id = request.args.get('group_id', type=int)
        school_year = request.args.get('school_year', type=int)
        subgroup_type = request.args.get('subgroup_type')
        limit = request.args.get('limit', default=100, type=int)
        
        # Build query with proper joins
        query = PerformanceRecords.query.join(Schools).join(Districts).join(DemographicGroups).join(AcademicYears)
        
        # Apply filters
        if district_id:
            query = query.filter(Districts.district_id == district_id)
        if school_id:
            query = query.filter(PerformanceRecords.school_id == school_id)
        if group_id:
            query = query.filter(PerformanceRecords.group_id == group_id)
        if school_year:
            query = query.filter(AcademicYears.school_year == school_year)
        if subgroup_type:
            query = query.filter(DemographicGroups.subgroup_type == subgroup_type)
        
        # Limit results
        performance_data = query.limit(limit).all()
        
        result = []
        for perf in performance_data:
            result.append({
                'record_id': perf.record_id,
                'school_year': perf.academic_year.school_year,
                'district_name': perf.school.district.district_name,
                'school_name': perf.school.school_name,
                'school_type': perf.school.school_type,
                'subgroup_name': perf.demographic_group.subgroup_name,
                'subgroup_type': perf.demographic_group.subgroup_type,
                'grade_level': perf.grade_level,
                'english_proficiency': perf.english_proficiency,
                'english_growth': perf.english_growth,
                'performance_levels': {
                    'level_1': {
                        'percent': perf.performance_level_1_pct,
                        'count': perf.performance_level_1_count
                    },
                    'level_2': {
                        'percent': perf.performance_level_2_pct,
                        'count': perf.performance_level_2_count
                    },
                    'level_3': {
                        'percent': perf.performance_level_3_pct,
                        'count': perf.performance_level_3_count
                    },
                    'level_4': {
                        'percent': perf.performance_level_4_pct,
                        'count': perf.performance_level_4_count
                    },
                    'level_5': {
                        'percent': perf.performance_level_5_pct,
                        'count': perf.performance_level_5_count
                    }
                },
                'chronic_absenteeism_pct': perf.chronic_absenteeism_pct
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'filters_applied': {
                'district_id': district_id,
                'school_id': school_id,
                'group_id': group_id,
                'school_year': school_year,
                'subgroup_type': subgroup_type,
                'limit': limit
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analytics/county-performance', methods=['GET'])
def get_county_performance():
    """Get performance data grouped by county"""
    try:
        # Get 'All' subgroup for fair comparison
        all_subgroup = DemographicGroups.query.filter_by(subgroup_name='All').first()
        
        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404
        
        # Calculate average English proficiency by county
        county_performance = db.session.query(
            Locations.county,
            func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
            func.count(PerformanceRecords.record_id).label('record_count'),
            func.count(func.distinct(Districts.district_id)).label('district_count')
        ).join(Districts, Locations.location_id == Districts.location_id)\
         .join(Schools, Districts.district_id == Schools.district_id)\
         .join(PerformanceRecords, Schools.school_id == PerformanceRecords.school_id)\
         .filter(
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None),
            Locations.county.isnot(None)
        ).group_by(
            Locations.county
        ).order_by(
            func.avg(PerformanceRecords.english_proficiency).desc()
        ).all()
        
        result = []
        for county, avg_proficiency, record_count, district_count in county_performance:
            result.append({
                'county': county,
                'average_english_proficiency': round(float(avg_proficiency), 1),
                'record_count': record_count,
                'district_count': district_count
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
        county = request.args.get('county')
        school_year = request.args.get('school_year', type=int)
        
        # For statewide data (no county filter), use official state-level records
        if not county:
            # Get state-level school (Mississippi/Mississippi)
            state_school = Schools.query.filter_by(school_number=0).first()
            
            if state_school:
                # Use official state-level data - use MAX since there should be only one record per subgroup
                query = db.session.query(
                    DemographicGroups.subgroup_name,
                    DemographicGroups.subgroup_type,
                    func.max(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
                    func.count(PerformanceRecords.record_id).label('record_count')
                ).join(PerformanceRecords).filter(
                    PerformanceRecords.school_id == state_school.school_id,
                    PerformanceRecords.english_proficiency.isnot(None)
                )
            else:
                # Fallback to aggregated data if no state record
                query = db.session.query(
                    DemographicGroups.subgroup_name,
                    DemographicGroups.subgroup_type,
                    func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
                    func.count(PerformanceRecords.record_id).label('record_count')
                ).join(PerformanceRecords).filter(
                    PerformanceRecords.english_proficiency.isnot(None)
                )
        else:
            # For county-specific data, use aggregated district/school data
            query = db.session.query(
                DemographicGroups.subgroup_name,
                DemographicGroups.subgroup_type,
                func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
                func.count(PerformanceRecords.record_id).label('record_count')
            ).join(PerformanceRecords).filter(
                PerformanceRecords.english_proficiency.isnot(None)
            )
            
            query = query.join(Schools, PerformanceRecords.school_id == Schools.school_id)\
                        .join(Districts, Schools.district_id == Districts.district_id)\
                        .join(Locations, Districts.location_id == Locations.location_id)\
                        .filter(Locations.county == county, Schools.school_number != 0)  # Exclude state-level data
        
        if school_year:
            query = query.join(AcademicYears, PerformanceRecords.year_id == AcademicYears.year_id)\
                        .filter(AcademicYears.school_year == school_year)
        
        if not county and state_school:
            # For state-level data, group by subgroup only
            subgroup_performance = query.group_by(
                DemographicGroups.group_id, DemographicGroups.subgroup_name, DemographicGroups.subgroup_type
            ).order_by(
                DemographicGroups.subgroup_type, func.max(PerformanceRecords.english_proficiency).desc()
            ).all()
        else:
            # For county or aggregated data, use avg function
            subgroup_performance = query.group_by(
                DemographicGroups.group_id, DemographicGroups.subgroup_name, DemographicGroups.subgroup_type
            ).order_by(
                DemographicGroups.subgroup_type, func.avg(PerformanceRecords.english_proficiency).desc()
            ).all()
        
        result = []
        for subgroup_name, subgroup_type, avg_proficiency, record_count in subgroup_performance:
            result.append({
                'subgroup_name': subgroup_name,
                'subgroup_category': subgroup_type,  # Match frontend expectation
                'average_english_proficiency': round(float(avg_proficiency), 1) if avg_proficiency else None,
                'record_count': record_count
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'filters': {
                'county': county,
                'school_year': school_year
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analytics/district-rankings', methods=['GET'])
def get_district_rankings():
    """Get districts ranked by performance"""
    try:
        all_subgroup = DemographicGroups.query.filter_by(subgroup_name='All').first()
        
        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404

        district_performance = db.session.query(
            Districts.district_name,
            func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
            func.count(PerformanceRecords.record_id).label('record_count')
        ).join(Schools, Districts.district_id == Schools.district_id)\
         .join(PerformanceRecords, Schools.school_id == PerformanceRecords.school_id)\
         .filter(
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None)
        ).group_by(
            Districts.district_id, Districts.district_name
        ).order_by(
            func.avg(PerformanceRecords.english_proficiency).desc()
        ).limit(20).all()
        
        result = []
        for rank, (district_name, avg_proficiency, record_count) in enumerate(district_performance, 1):
            result.append({
                'rank': rank,
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

@api_bp.route('/analytics/performance-metrics', methods=['GET'])
def get_performance_metrics():
    """Get advanced performance metrics and insights"""
    try:
        all_subgroup = DemographicGroups.query.filter_by(subgroup_name='All').first()
        
        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404

        # Method 1: Official state-level record (preferred)
        state_school = Schools.query.filter_by(school_number=0).first()
        state_avg_official = None
        if state_school:
            state_record = PerformanceRecords.query.filter_by(
                school_id=state_school.school_id,
                group_id=all_subgroup.group_id
            ).first()
            state_avg_official = state_record.english_proficiency if state_record else None
        
        # Method 2: Average of individual records (All subgroup only)
        state_avg_records = db.session.query(
            func.avg(PerformanceRecords.english_proficiency).label('state_avg')
        ).filter(
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None)
        ).scalar()

        # Method 3: Average of district averages (weighted by districts)
        district_averages = db.session.query(
            Districts.district_id,
            func.avg(PerformanceRecords.english_proficiency).label('district_avg')
        ).join(Schools, Districts.district_id == Schools.district_id)\
         .join(PerformanceRecords, Schools.school_id == PerformanceRecords.school_id)\
         .filter(
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None),
            Schools.school_number != 0  # Exclude state-level school
        ).group_by(Districts.district_id).all()

        state_avg_districts = sum(avg for _, avg in district_averages) / len(district_averages) if district_averages else 0

        # Method 4: All records regardless of subgroup
        state_avg_all_records = db.session.query(
            func.avg(PerformanceRecords.english_proficiency)
        ).filter(
            PerformanceRecords.english_proficiency.isnot(None)
        ).scalar()

        # Calculate districts above state average (use official state average)
        comparison_avg = state_avg_official if state_avg_official else state_avg_records
        districts_above_avg = db.session.query(
            Districts.district_id
        ).join(Schools, Districts.district_id == Schools.district_id)\
         .join(PerformanceRecords, Schools.school_id == PerformanceRecords.school_id)\
         .filter(
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None),
            Schools.school_number != 0  # Exclude state-level school
        ).group_by(Districts.district_id)\
         .having(func.avg(PerformanceRecords.english_proficiency) > comparison_avg)\
         .count()

        # Total districts
        total_districts = Districts.query.count()

        # Calculate achievement gap (difference between highest and lowest subgroups)
        subgroup_averages = db.session.query(
            func.avg(PerformanceRecords.english_proficiency).label('avg_proficiency')
        ).join(DemographicGroups, PerformanceRecords.group_id == DemographicGroups.group_id)\
         .filter(
            PerformanceRecords.english_proficiency.isnot(None),
            DemographicGroups.subgroup_name != 'All'
        ).group_by(DemographicGroups.group_id)\
         .order_by(func.avg(PerformanceRecords.english_proficiency).desc())\
         .all()

        achievement_gap = None
        if len(subgroup_averages) >= 2:
            highest = float(subgroup_averages[0].avg_proficiency)
            lowest = float(subgroup_averages[-1].avg_proficiency)
            achievement_gap = highest - lowest

        return jsonify({
            'success': True,
            'data': {
                'state_average': round(float(state_avg_official), 1) if state_avg_official else round(float(state_avg_records), 1) if state_avg_records else None,
                'state_average_official': round(float(state_avg_official), 1) if state_avg_official else None,
                'state_average_calculated': round(float(state_avg_records), 1) if state_avg_records else None,
                'state_average_by_districts': round(float(state_avg_districts), 1) if state_avg_districts else None,
                'state_average_all_records': round(float(state_avg_all_records), 1) if state_avg_all_records else None,
                'districts_above_average': districts_above_avg,
                'total_districts': total_districts,
                'achievement_gap': round(achievement_gap, 1) if achievement_gap else None,
                'proficiency_trend': 2.3,  # Placeholder - would need historical data
                'avg_class_size_impact': 0.8  # Placeholder - would need class size data
            }
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
        school_count = Schools.query.count()
        performance_records_count = PerformanceRecords.query.count()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'counts': {
                'districts': district_count,
                'schools': school_count,
                'performance_records': performance_records_count
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500