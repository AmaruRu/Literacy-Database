from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100))
    reset_token = db.Column(db.String(100))
    reset_token_expires = db.Column(db.DateTime)

class Locations(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String(100))
    city = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    
    districts = db.relationship('Districts', backref='location', lazy=True)
    
    def to_dict(self):
        return {
            'location_id': self.location_id,
            'county': self.county,
            'city': self.city,
            'zip_code': self.zip_code
        }
    
class Districts(db.Model):
    __tablename__ = 'districts'
    district_id = db.Column(db.Integer, primary_key=True)
    district_number = db.Column(db.Integer, nullable=False)
    district_name = db.Column(db.String(255), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=True)
    
    schools = db.relationship('Schools', backref='district', lazy=True, cascade='all, delete-orphan')
    teacher_quality = db.relationship('TeacherQuality', backref='district', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'district_id': self.district_id,
            'district_number': self.district_number,
            'district_name': self.district_name,
            'location_id': self.location_id,
            'county': self.location.county if self.location else None,
            'city': self.location.city if self.location else None,
            'zip_code': self.location.zip_code if self.location else None
        }

class Schools(db.Model):
    __tablename__ = 'schools'
    school_id = db.Column(db.Integer, primary_key=True)
    school_number = db.Column(db.Integer, nullable=False)
    school_name = db.Column(db.String(255), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.district_id'), nullable=False)
    school_type = db.Column(db.String(50))  # State/District/School/Public/Private
    grade_span = db.Column(db.String(50))   # e.g., K-5, 6-8, 9-12
    
    performance_records = db.relationship('PerformanceRecords', backref='school', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'school_id': self.school_id,
            'school_number': self.school_number,
            'school_name': self.school_name,
            'district_id': self.district_id,
            'school_type': self.school_type,
            'grade_span': self.grade_span,
            'district_name': self.district.district_name if self.district else None
        }

class DemographicGroups(db.Model):
    __tablename__ = 'demographic_groups'
    group_id = db.Column(db.Integer, primary_key=True)
    subgroup_name = db.Column(db.String(255), nullable=False, unique=True)
    subgroup_type = db.Column(db.String(50), nullable=False)  # Race | Gender | Ethnicity | EconStatus | SPED | EL | All
    
    performance_records = db.relationship('PerformanceRecords', backref='demographic_group', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'group_id': self.group_id,
            'subgroup_name': self.subgroup_name,
            'subgroup_type': self.subgroup_type
        }

class AcademicYears(db.Model):
    __tablename__ = 'academic_years'
    year_id = db.Column(db.Integer, primary_key=True)
    school_year = db.Column(db.Integer, nullable=False, unique=True)
    
    performance_records = db.relationship('PerformanceRecords', backref='academic_year', lazy=True, cascade='all, delete-orphan')
    teacher_quality = db.relationship('TeacherQuality', backref='academic_year', lazy=True, cascade='all, delete-orphan')
    naep_assessments = db.relationship('NAEPAssessments', backref='academic_year', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'year_id': self.year_id,
            'school_year': self.school_year
        }

class PerformanceRecords(db.Model):
    __tablename__ = 'performance_records'
    record_id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.school_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('demographic_groups.group_id'), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('academic_years.year_id'), nullable=False)
    grade_level = db.Column(db.String(50))
    
    # English/Reading Performance Metrics
    english_proficiency = db.Column(db.Float)
    english_growth = db.Column(db.Float)
    english_growth_lowest_25 = db.Column(db.Float)
    
    # Performance Level Percentages and Counts
    performance_level_1_pct = db.Column(db.Float)
    performance_level_1_count = db.Column(db.Integer)
    performance_level_2_pct = db.Column(db.Float)
    performance_level_2_count = db.Column(db.Integer)
    performance_level_3_pct = db.Column(db.Float)
    performance_level_3_count = db.Column(db.Integer)
    performance_level_4_pct = db.Column(db.Float)
    performance_level_4_count = db.Column(db.Integer)
    performance_level_5_pct = db.Column(db.Float)
    performance_level_5_count = db.Column(db.Integer)
    
    # Additional Metrics
    chronic_absenteeism_pct = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'record_id': self.record_id,
            'school_id': self.school_id,
            'group_id': self.group_id,
            'year_id': self.year_id,
            'grade_level': self.grade_level,
            'english_proficiency': self.english_proficiency,
            'english_growth': self.english_growth,
            'english_growth_lowest_25': self.english_growth_lowest_25,
            'performance_level_1_pct': self.performance_level_1_pct,
            'performance_level_1_count': self.performance_level_1_count,
            'performance_level_2_pct': self.performance_level_2_pct,
            'performance_level_2_count': self.performance_level_2_count,
            'performance_level_3_pct': self.performance_level_3_pct,
            'performance_level_3_count': self.performance_level_3_count,
            'performance_level_4_pct': self.performance_level_4_pct,
            'performance_level_4_count': self.performance_level_4_count,
            'performance_level_5_pct': self.performance_level_5_pct,
            'performance_level_5_count': self.performance_level_5_count,
            'chronic_absenteeism_pct': self.chronic_absenteeism_pct,
            'school_year': self.academic_year.school_year if self.academic_year else None,
            'school_name': self.school.school_name if self.school else None,
            'subgroup_name': self.demographic_group.subgroup_name if self.demographic_group else None,
            'subgroup_type': self.demographic_group.subgroup_type if self.demographic_group else None
        }

class TeacherQuality(db.Model):
    __tablename__ = 'teacher_quality'
    quality_id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.district_id'), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('academic_years.year_id'), nullable=False)
    
    # Teacher Quality Metrics by Poverty Level
    experienced_teachers_high_poverty = db.Column(db.Float)
    experienced_teachers_low_poverty = db.Column(db.Float)
    emergency_provisional_teachers_high_poverty = db.Column(db.Float)
    emergency_provisional_teachers_low_poverty = db.Column(db.Float)
    in_field_teachers_high_poverty = db.Column(db.Float)
    in_field_teachers_low_poverty = db.Column(db.Float)
    effective_teachers_high_poverty = db.Column(db.Float)
    effective_teachers_low_poverty = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'quality_id': self.quality_id,
            'district_id': self.district_id,
            'year_id': self.year_id,
            'experienced_teachers_high_poverty': self.experienced_teachers_high_poverty,
            'experienced_teachers_low_poverty': self.experienced_teachers_low_poverty,
            'emergency_provisional_teachers_high_poverty': self.emergency_provisional_teachers_high_poverty,
            'emergency_provisional_teachers_low_poverty': self.emergency_provisional_teachers_low_poverty,
            'in_field_teachers_high_poverty': self.in_field_teachers_high_poverty,
            'in_field_teachers_low_poverty': self.in_field_teachers_low_poverty,
            'effective_teachers_high_poverty': self.effective_teachers_high_poverty,
            'effective_teachers_low_poverty': self.effective_teachers_low_poverty,
            'school_year': self.academic_year.school_year if self.academic_year else None,
            'district_name': self.district.district_name if self.district else None
        }

class NAEPAssessments(db.Model):
    __tablename__ = 'naep_assessments'
    assessment_id = db.Column(db.Integer, primary_key=True)
    year_id = db.Column(db.Integer, db.ForeignKey('academic_years.year_id'), nullable=False)
    scope = db.Column(db.String(20), nullable=False)  # State/District/School
    district_id = db.Column(db.Integer, db.ForeignKey('districts.district_id'), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.school_id'), nullable=True)
    
    # NAEP 4th Grade Reading Levels
    grade_4_reading_below_basic = db.Column(db.Float)
    grade_4_reading_basic = db.Column(db.Float)
    grade_4_reading_proficient = db.Column(db.Float)
    grade_4_reading_advanced = db.Column(db.Float)
    
    # NAEP 8th Grade Reading Levels
    grade_8_reading_below_basic = db.Column(db.Float)
    grade_8_reading_basic = db.Column(db.Float)
    grade_8_reading_proficient = db.Column(db.Float)
    grade_8_reading_advanced = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'assessment_id': self.assessment_id,
            'year_id': self.year_id,
            'scope': self.scope,
            'district_id': self.district_id,
            'school_id': self.school_id,
            'grade_4_reading_below_basic': self.grade_4_reading_below_basic,
            'grade_4_reading_basic': self.grade_4_reading_basic,
            'grade_4_reading_proficient': self.grade_4_reading_proficient,
            'grade_4_reading_advanced': self.grade_4_reading_advanced,
            'grade_8_reading_below_basic': self.grade_8_reading_below_basic,
            'grade_8_reading_basic': self.grade_8_reading_basic,
            'grade_8_reading_proficient': self.grade_8_reading_proficient,
            'grade_8_reading_advanced': self.grade_8_reading_advanced,
            'school_year': self.academic_year.school_year if self.academic_year else None
        }

class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    grade_level = db.Column(db.String(50), nullable=False)
    lexile = db.Column(db.String(20), nullable=True)
    literature_type = db.Column(db.Enum('Fiction', 'Nonfiction', name='literature_type'), nullable=False)
    cover_url = db.Column(db.String(1000), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'grade_level': self.grade_level,
            'lexile': self.lexile,
            'literature_type': self.literature_type,
            'cover_url': self.cover_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }