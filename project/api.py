"""
API endpoints for Mississippi Literacy Database
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import func
from .models import Districts, Schools, Subgroups, PerformanceData, TeacherQuality, NAEPAssessments
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
        
        # Get most recent year for accurate comparison
        recent_year = db.session.query(func.max(PerformanceData.School_Year)).scalar()
        
        # Calculate average English proficiency by district
        rankings = db.session.query(
            Districts.District_Name,
            Districts.District_ID,
            func.avg(PerformanceData.English_Proficiency).label('avg_english_proficiency'),
            func.count(PerformanceData.Performance_ID).label('record_count')
        ).join(PerformanceData).filter(
            PerformanceData.Subgroup_ID == all_subgroup.Subgroup_ID,
            PerformanceData.English_Proficiency.isnot(None),
            PerformanceData.School_Year == recent_year,
            PerformanceData.Assessment_Type == 'District'
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

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    try:
        # Simple database connectivity check
        district_count = Districts.query.count()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'district_count': district_count
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500