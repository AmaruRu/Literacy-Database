from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<User {self.username}>'


class Districts(db.Model):
    __tablename__ = 'Districts'
    
    District_ID = db.Column(db.Integer, primary_key=True)
    District_Number = db.Column(db.Integer, unique=True, nullable=False)
    District_Name = db.Column(db.String(255), nullable=False)
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)
    Updated_At = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schools = db.relationship('Schools', backref='district', lazy=True, cascade='all, delete-orphan')
    performance_data = db.relationship('PerformanceData', backref='district', lazy=True, cascade='all, delete-orphan')
    teacher_quality = db.relationship('TeacherQuality', backref='district', lazy=True, cascade='all, delete-orphan')
    naep_assessments = db.relationship('NAEPAssessments', backref='district', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<District {self.District_Name}>'


class Schools(db.Model):
    __tablename__ = 'Schools'
    
    School_ID = db.Column(db.Integer, primary_key=True)
    School_Number = db.Column(db.Integer, nullable=False)
    School_Name = db.Column(db.String(255), nullable=False)
    District_ID = db.Column(db.Integer, db.ForeignKey('Districts.District_ID'), nullable=False)
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)
    Updated_At = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    performance_data = db.relationship('PerformanceData', backref='school', lazy=True, cascade='all, delete-orphan')
    teacher_quality = db.relationship('TeacherQuality', backref='school', lazy=True, cascade='all, delete-orphan')
    naep_assessments = db.relationship('NAEPAssessments', backref='school', lazy=True, cascade='all, delete-orphan')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('School_Number', 'District_ID', name='unique_school_district'),)
    
    def __repr__(self):
        return f'<School {self.School_Name}>'


class Subgroups(db.Model):
    __tablename__ = 'Subgroups'
    
    Subgroup_ID = db.Column(db.Integer, primary_key=True)
    Subgroup_Name = db.Column(db.String(100), nullable=False, unique=True)
    Subgroup_Category = db.Column(db.Enum('All', 'Gender', 'Race_Ethnicity', 'Special_Population', name='subgroup_category'), nullable=False)
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    performance_data = db.relationship('PerformanceData', backref='subgroup', lazy=True, cascade='all, delete-orphan')
    naep_assessments = db.relationship('NAEPAssessments', backref='subgroup', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subgroup {self.Subgroup_Name}>'


class PerformanceData(db.Model):
    __tablename__ = 'Performance_Data'
    
    Performance_ID = db.Column(db.Integer, primary_key=True)
    School_Year = db.Column(db.Integer, nullable=False)
    District_ID = db.Column(db.Integer, db.ForeignKey('Districts.District_ID'), nullable=True)
    School_ID = db.Column(db.Integer, db.ForeignKey('Schools.School_ID'), nullable=True)
    Subgroup_ID = db.Column(db.Integer, db.ForeignKey('Subgroups.Subgroup_ID'), nullable=False)
    Grade_Level = db.Column(db.String(20), nullable=True)
    Assessment_Type = db.Column(db.Enum('State', 'District', 'School', name='assessment_type'), nullable=False)
    
    # English/Reading Performance
    English_Proficiency = db.Column(db.Numeric(5, 2), nullable=True)
    English_Growth = db.Column(db.Numeric(5, 2), nullable=True)
    English_Growth_Lowest_25_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    
    # Performance Level Percentages (1-5 scale)
    Performance_Level_1_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Performance_Level_1_Students = db.Column(db.Integer, nullable=True)
    Performance_Level_2_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Performance_Level_2_Students = db.Column(db.Integer, nullable=True)
    Performance_Level_3_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Performance_Level_3_Students = db.Column(db.Integer, nullable=True)
    Performance_Level_4_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Performance_Level_4_Students = db.Column(db.Integer, nullable=True)
    Performance_Level_5_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Performance_Level_5_Students = db.Column(db.Integer, nullable=True)
    
    # Attendance
    Chronic_Absenteeism_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)
    Updated_At = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('School_Year', 'District_ID', 'School_ID', 'Subgroup_ID', 'Grade_Level', name='unique_performance_record'),)
    
    def __repr__(self):
        return f'<PerformanceData {self.School_Year} - {self.subgroup.Subgroup_Name if self.subgroup else "Unknown"}>'


class TeacherQuality(db.Model):
    __tablename__ = 'Teacher_Quality'
    
    Teacher_Quality_ID = db.Column(db.Integer, primary_key=True)
    School_Year = db.Column(db.Integer, nullable=False)
    District_ID = db.Column(db.Integer, db.ForeignKey('Districts.District_ID'), nullable=True)
    School_ID = db.Column(db.Integer, db.ForeignKey('Schools.School_ID'), nullable=True)
    
    # Experienced Teachers
    Experienced_Teachers_High_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Experienced_Teachers_Low_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    
    # Emergency Provisional Teachers
    Emergency_Provisional_High_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Emergency_Provisional_Low_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    
    # In-Field Teachers
    In_Field_Teachers_High_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    In_Field_Teachers_Low_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    
    # Effective Teachers
    Effective_Teachers_High_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    Effective_Teachers_Low_Poverty_Percent = db.Column(db.Numeric(5, 2), nullable=True)
    
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)
    Updated_At = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('School_Year', 'District_ID', 'School_ID', name='unique_teacher_record'),)
    
    def __repr__(self):
        return f'<TeacherQuality {self.School_Year} - District {self.District_ID}>'


class NAEPAssessments(db.Model):
    __tablename__ = 'NAEP_Assessments'
    
    NAEP_ID = db.Column(db.Integer, primary_key=True)
    School_Year = db.Column(db.Integer, nullable=False)
    District_ID = db.Column(db.Integer, db.ForeignKey('Districts.District_ID'), nullable=True)
    School_ID = db.Column(db.Integer, db.ForeignKey('Schools.School_ID'), nullable=True)
    Subgroup_ID = db.Column(db.Integer, db.ForeignKey('Subgroups.Subgroup_ID'), nullable=False)
    
    # 4th Grade Math
    Grade_4_Math_Below_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_4_Math_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_4_Math_Proficient = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_4_Math_Advanced = db.Column(db.Numeric(5, 2), nullable=True)
    
    # 4th Grade Reading
    Grade_4_Reading_Below_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_4_Reading_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_4_Reading_Proficient = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_4_Reading_Advanced = db.Column(db.Numeric(5, 2), nullable=True)
    
    # 8th Grade Math
    Grade_8_Math_Below_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_8_Math_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_8_Math_Proficient = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_8_Math_Advanced = db.Column(db.Numeric(5, 2), nullable=True)
    
    # 8th Grade Reading
    Grade_8_Reading_Below_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_8_Reading_Basic = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_8_Reading_Proficient = db.Column(db.Numeric(5, 2), nullable=True)
    Grade_8_Reading_Advanced = db.Column(db.Numeric(5, 2), nullable=True)
    
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)
    Updated_At = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('School_Year', 'District_ID', 'School_ID', 'Subgroup_ID', name='unique_naep_record'),)
    
    def __repr__(self):
        return f'<NAEPAssessment {self.School_Year} - {self.subgroup.Subgroup_Name if self.subgroup else "Unknown"}>'