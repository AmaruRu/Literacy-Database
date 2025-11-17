"""
API endpoints for Mississippi Literacy Database
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_
from .models import Locations, Districts, Schools, DemographicGroups, AcademicYears, PerformanceRecords, TeacherQuality, NAEPAssessments, Books
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
    """Get districts ranked by performance with filtering options"""
    try:
        all_subgroup = DemographicGroups.query.filter_by(subgroup_name='All').first()
        
        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404

        # Get filter parameters
        county = request.args.get('county')
        performance_range = request.args.get('performance_range')
        limit = request.args.get('limit', default=20, type=int)

        # Build query with filters
        query = db.session.query(
            Districts.district_id,
            Districts.district_name,
            Locations.county,
            func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
            func.count(PerformanceRecords.record_id).label('record_count')
        ).join(Schools, Districts.district_id == Schools.district_id)\
         .join(PerformanceRecords, Schools.school_id == PerformanceRecords.school_id)\
         .join(Locations, Districts.location_id == Locations.location_id)\
         .filter(
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None),
            Schools.school_number != 0  # Exclude state-level school
        )

        # Apply county filter
        if county:
            query = query.filter(Locations.county == county)

        # Group and order
        district_performance = query.group_by(
            Districts.district_id, Districts.district_name, Locations.county
        ).order_by(
            func.avg(PerformanceRecords.english_proficiency).desc()
        )

        # Apply performance range filter after grouping
        if performance_range:
            if performance_range == 'high':
                district_performance = district_performance.having(
                    func.avg(PerformanceRecords.english_proficiency) >= 47.6
                )
            elif performance_range == 'medium':
                district_performance = district_performance.having(
                    func.avg(PerformanceRecords.english_proficiency).between(35, 47.5)
                )
            elif performance_range == 'low':
                district_performance = district_performance.having(
                    func.avg(PerformanceRecords.english_proficiency) < 35
                )

        district_performance = district_performance.limit(limit).all()
        
        result = []
        for rank, (district_id, district_name, county, avg_proficiency, record_count) in enumerate(district_performance, 1):
            result.append({
                'rank': rank,
                'district_id': district_id,
                'district_name': district_name,
                'county': county,
                'average_english_proficiency': round(float(avg_proficiency), 1),
                'record_count': record_count
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'filters': {
                'county': county,
                'performance_range': performance_range,
                'limit': limit
            }
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

@api_bp.route('/analytics/school-performance', methods=['GET'])
def get_school_performance():
    """Get school performance data within a district"""
    try:
        district_id = request.args.get('district_id', type=int)
        grade_span = request.args.get('grade_span')
        
        if not district_id:
            return jsonify({
                'success': False,
                'error': 'district_id parameter is required'
            }), 400

        all_subgroup = DemographicGroups.query.filter_by(subgroup_name='All').first()
        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404

        # Get district information
        district = Districts.query.get(district_id)
        if not district:
            return jsonify({
                'success': False,
                'error': 'District not found'
            }), 404

        # Build school performance query
        query = db.session.query(
            Schools.school_id,
            Schools.school_name,
            Schools.grade_span,
            Schools.school_type,
            func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
            func.count(PerformanceRecords.record_id).label('record_count')
        ).join(PerformanceRecords, Schools.school_id == PerformanceRecords.school_id)\
         .filter(
            Schools.district_id == district_id,
            Schools.school_number != 0,  # Exclude district-level aggregates
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None)
        )

        # Apply grade span filter if provided
        if grade_span:
            query = query.filter(Schools.grade_span == grade_span)

        school_performance = query.group_by(
            Schools.school_id, Schools.school_name, Schools.grade_span, Schools.school_type
        ).order_by(
            func.avg(PerformanceRecords.english_proficiency).desc()
        ).all()

        # Calculate district average
        district_avg_query = db.session.query(
            func.avg(PerformanceRecords.english_proficiency)
        ).join(Schools, PerformanceRecords.school_id == Schools.school_id)\
         .filter(
            Schools.district_id == district_id,
            Schools.school_number != 0,
            PerformanceRecords.group_id == all_subgroup.group_id,
            PerformanceRecords.english_proficiency.isnot(None)
        ).scalar()

        district_average = round(float(district_avg_query), 1) if district_avg_query else 0

        # Prepare results
        result = []
        schools_above_avg = 0
        
        for rank, (school_id, school_name, grade_span, school_type, avg_proficiency, record_count) in enumerate(school_performance, 1):
            proficiency = round(float(avg_proficiency), 1)
            vs_district = proficiency - district_average
            
            if proficiency > district_average:
                schools_above_avg += 1
                vs_district_indicator = 'above'
            elif proficiency == district_average:
                vs_district_indicator = 'equal'
            else:
                vs_district_indicator = 'below'

            result.append({
                'rank': rank,
                'school_id': school_id,
                'school_name': school_name,
                'grade_span': grade_span or 'Not specified',
                'school_type': school_type,
                'average_english_proficiency': proficiency,
                'record_count': record_count,
                'vs_district_avg': round(vs_district, 1),
                'vs_district_indicator': vs_district_indicator
            })

        # Get available grade spans for filtering
        grade_spans = db.session.query(Schools.grade_span)\
            .filter(Schools.district_id == district_id, Schools.school_number != 0, Schools.grade_span.isnot(None))\
            .distinct().all()
        
        available_grade_spans = [span[0] for span in grade_spans if span[0]]

        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'district_info': {
                'district_id': district.district_id,
                'district_name': district.district_name,
                'district_average': district_average,
                'total_schools': len(result),
                'schools_above_district_avg': schools_above_avg,
                'available_grade_spans': available_grade_spans
            },
            'filters': {
                'district_id': district_id,
                'grade_span': grade_span
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analytics/counties', methods=['GET'])
def get_counties():
    """Get list of available counties for filtering"""
    try:
        counties = db.session.query(Locations.county)\
            .filter(Locations.county.isnot(None))\
            .distinct()\
            .order_by(Locations.county)\
            .all()
        
        county_list = [county[0] for county in counties]
        
        return jsonify({
            'success': True,
            'data': county_list,
            'count': len(county_list)
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
            query = query.filter(Books.grade_level == grade_level)

        if literature_type:
            query = query.filter(Books.literature_type == literature_type)

        if author:
            query = query.filter(Books.author.ilike(f'%{author}%'))

        if search:
            query = query.filter(or_(
                Books.title.ilike(f'%{search}%'),
                Books.author.ilike(f'%{search}%')
            ))

        # Lexile filtering (handle numeric and special values like "BR")
        if lexile_min or lexile_max:
            if lexile_min:
                try:
                    min_val = int(lexile_min)
                    query = query.filter(
                        or_(
                            Books.lexile.cast(db.Integer) >= min_val,
                            Books.lexile == 'BR'
                        )
                    )
                except ValueError:
                    pass

            if lexile_max:
                try:
                    max_val = int(lexile_max)
                    query = query.filter(
                        or_(
                            Books.lexile.cast(db.Integer) <= max_val,
                            Books.lexile == 'BR'
                        )
                    )
                except ValueError:
                    pass

        # Get total count before pagination
        total_count = query.count()

        # Apply pagination
        books = query.order_by(Books.grade_level, Books.title).limit(limit).offset(offset).all()

        result = []
        for book in books:
            result.append({
                'book_id': book.book_id,
                'title': book.title,
                'author': book.author,
                'grade_level': book.grade_level,
                'lexile': book.lexile,
                'literature_type': book.literature_type,
                'cover_url': book.cover_url
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
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'grade_level': book.grade_level,
            'lexile': book.lexile,
            'literature_type': book.literature_type,
            'cover_url': book.cover_url,
            'created_at': book.created_at.isoformat() if book.created_at else None
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
            Books.grade_level,
            func.count(Books.book_id).label('book_count')
        ).group_by(Books.grade_level).order_by(
            func.field(Books.grade_level,
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
            Books.author,
            func.count(Books.book_id).label('book_count')
        ).group_by(Books.author).order_by(
            func.count(Books.book_id).desc(),
            Books.author
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

@api_bp.route('/map/districts', methods=['GET'])
def get_map_districts():
    """Get district literacy data for map visualization (grouped by county)"""
    try:
        # Mapping of district names to counties using your existing data
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
            'Yazoo City': 'Yazoo'
        }

        # Special handling for district names with directional prefixes
        DISTRICT_OVERRIDES = {
            'North Panola': 'Panola', 'South Panola': 'Panola',
            'North Pike': 'Pike', 'South Pike': 'Pike',
            'North Tippah': 'Tippah', 'South Tippah': 'Tippah',
            'North Bolivar': 'Bolivar', 'West Bolivar': 'Bolivar',
            'West Jasper': 'Jasper', 'West Tallahatchie': 'Tallahatchie'
        }

        # Get 'All' subgroup for overall performance
        all_subgroup = DemographicGroups.query.filter_by(subgroup_name='All').first()

        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404

        # Get most recent year
        most_recent_year = db.session.query(
            func.max(AcademicYears.school_year)
        ).join(PerformanceRecords).scalar()

        # Get district data with literacy metrics
        districts_data = db.session.query(
            Districts.district_name,
            func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
            func.avg(PerformanceRecords.english_growth).label('avg_english_growth'),
            func.avg(PerformanceRecords.chronic_absenteeism_pct).label('avg_chronic_absenteeism'),
            func.count(Schools.school_id.distinct()).label('school_count')
        ).join(
            Schools, Districts.district_id == Schools.district_id
        ).join(
            PerformanceRecords, Schools.school_id == PerformanceRecords.school_id
        ).join(
            AcademicYears, PerformanceRecords.year_id == AcademicYears.year_id
        ).filter(
            PerformanceRecords.group_id == all_subgroup.group_id,
            AcademicYears.school_year == most_recent_year
        ).group_by(
            Districts.district_id, Districts.district_name
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

            # Use location data if still no match
            if not county_name:
                district_obj = Districts.query.filter_by(district_name=district_name).first()
                if district_obj and district_obj.location:
                    county_name = district_obj.location.county

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
        # Same mapping as in /map/districts
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
            'Yazoo City': 'Yazoo'
        }
        
        DISTRICT_OVERRIDES = {
            'North Panola': 'Panola', 'South Panola': 'Panola',
            'North Pike': 'Pike', 'South Pike': 'Pike',
            'North Tippah': 'Tippah', 'South Tippah': 'Tippah',
            'North Bolivar': 'Bolivar', 'West Bolivar': 'Bolivar',
            'West Jasper': 'Jasper', 'West Tallahatchie': 'Tallahatchie'
        }

        # Get 'All' subgroup
        all_subgroup = DemographicGroups.query.filter_by(subgroup_name='All').first()
        
        if not all_subgroup:
            return jsonify({
                'success': False,
                'error': "'All' subgroup not found"
            }), 404

        # Find districts for this county
        county_districts = []
        districts_data = db.session.query(
            Districts.district_name,
            Districts.district_id,
            func.avg(PerformanceRecords.english_proficiency).label('avg_english_proficiency'),
            func.avg(PerformanceRecords.english_growth).label('avg_english_growth'),
            func.avg(PerformanceRecords.chronic_absenteeism_pct).label('avg_chronic_absenteeism'),
            func.count(Schools.school_id.distinct()).label('school_count')
        ).join(
            Schools, Districts.district_id == Schools.district_id
        ).join(
            PerformanceRecords, Schools.school_id == PerformanceRecords.school_id
        ).filter(
            PerformanceRecords.group_id == all_subgroup.group_id
        ).group_by(
            Districts.district_id, Districts.district_name
        ).all()

        for district_name, district_id, eng_prof, eng_growth, absenteeism, school_count in districts_data:
            # Determine if this district belongs to the requested county
            district_county = None
            
            # Check override mapping first
            for override_key, override_county in DISTRICT_OVERRIDES.items():
                if override_key in district_name:
                    district_county = override_county
                    break

            # Try county-based naming
            if not district_county and 'County' in district_name:
                parts = district_name.split('County')[0].strip()
                county_parts = parts.split()
                if len(county_parts) > 1 and county_parts[0] in ['North', 'South', 'East', 'West']:
                    district_county = county_parts[-1]
                else:
                    district_county = parts

            # Try partial matching in DISTRICT_TO_COUNTY
            if not district_county:
                for key, value in DISTRICT_TO_COUNTY.items():
                    if key in district_name:
                        district_county = value
                        break

            # Use location data as fallback
            if not district_county:
                district_obj = Districts.query.get(district_id)
                if district_obj and district_obj.location:
                    district_county = district_obj.location.county

            if district_county and district_county.lower() == county_name.lower():
                # Get schools for this district
                schools = Schools.query.filter_by(district_id=district_id).all()
                
                district_info = {
                    'district_id': district_id,
                    'district_name': district_name,
                    'school_count': school_count if school_count else 0,
                    'schools': [
                        {
                            'school_id': school.school_id,
                            'school_name': school.school_name,
                            'school_type': school.school_type,
                            'grade_span': school.grade_span,
                            'county_name': district_county
                        }
                        for school in schools if school.school_number != 0  # Exclude state-level
                    ],
                    'english_proficiency': round(float(eng_prof), 1) if eng_prof else None,
                    'english_growth': round(float(eng_growth), 1) if eng_growth else None,
                    'chronic_absenteeism': round(float(absenteeism), 1) if absenteeism else None
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

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    try:
        # Simple database connectivity check
        district_count = Districts.query.count()
        school_count = Schools.query.count()
        performance_records_count = PerformanceRecords.query.count()
        book_count = Books.query.count()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'counts': {
                'districts': district_count,
                'schools': school_count,
                'performance_records': performance_records_count,
                'books': book_count
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500