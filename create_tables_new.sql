-- Mississippi Literacy Database Schema
-- Created: 2025-10-27
-- Database: literacy_db (MySQL)
-- Based on actual literacy_data.sql structure with proper normalization

-- Use the database (created by setup script)
USE literacy_db;

-- Drop existing tables if they exist (for clean reinstall)
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Performance_Data;
DROP TABLE IF EXISTS Teacher_Quality;
DROP TABLE IF EXISTS NAEP_Assessments;
DROP TABLE IF EXISTS Schools;
DROP TABLE IF EXISTS Subgroups;
DROP TABLE IF EXISTS Districts;
SET FOREIGN_KEY_CHECKS = 1;

-- Districts Table: Stores district information
CREATE TABLE Districts (
  District_ID INT AUTO_INCREMENT PRIMARY KEY,
  District_Number INT UNIQUE NOT NULL,
  District_Name VARCHAR(255) NOT NULL,
  Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_district_number (District_Number),
  INDEX idx_district_name (District_Name)
);

-- Schools Table: Stores individual school information
CREATE TABLE Schools (
  School_ID INT AUTO_INCREMENT PRIMARY KEY,
  School_Number INT NOT NULL,
  School_Name VARCHAR(255) NOT NULL,
  District_ID INT NOT NULL,
  Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (District_ID) REFERENCES Districts(District_ID) ON DELETE CASCADE,
  INDEX idx_school_number (School_Number),
  INDEX idx_school_name (School_Name),
  INDEX idx_district (District_ID),
  UNIQUE KEY unique_school_district (School_Number, District_ID)
);

-- Subgroups Table: Demographic and student subgroups
CREATE TABLE Subgroups (
  Subgroup_ID INT AUTO_INCREMENT PRIMARY KEY,
  Subgroup_Name VARCHAR(100) NOT NULL UNIQUE,
  Subgroup_Category ENUM('All', 'Gender', 'Race_Ethnicity', 'Special_Population') NOT NULL,
  Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_category (Subgroup_Category)
);

-- Performance Data Table: Core literacy and academic performance metrics
CREATE TABLE Performance_Data (
  Performance_ID INT AUTO_INCREMENT PRIMARY KEY,
  School_Year INT NOT NULL,
  District_ID INT,
  School_ID INT,
  Subgroup_ID INT NOT NULL,
  Grade_Level VARCHAR(20),
  Assessment_Type ENUM('State', 'District', 'School') NOT NULL,
  
  -- English/Reading Performance
  English_Proficiency DECIMAL(5,2) CHECK (English_Proficiency BETWEEN 0 AND 100),
  English_Growth DECIMAL(5,2),
  English_Growth_Lowest_25_Percent DECIMAL(5,2),
  
  -- Performance Level Percentages (1-5 scale)
  Performance_Level_1_Percent DECIMAL(5,2) CHECK (Performance_Level_1_Percent BETWEEN 0 AND 100),
  Performance_Level_1_Students INT,
  Performance_Level_2_Percent DECIMAL(5,2) CHECK (Performance_Level_2_Percent BETWEEN 0 AND 100),
  Performance_Level_2_Students INT,
  Performance_Level_3_Percent DECIMAL(5,2) CHECK (Performance_Level_3_Percent BETWEEN 0 AND 100),
  Performance_Level_3_Students INT,
  Performance_Level_4_Percent DECIMAL(5,2) CHECK (Performance_Level_4_Percent BETWEEN 0 AND 100),
  Performance_Level_4_Students INT,
  Performance_Level_5_Percent DECIMAL(5,2) CHECK (Performance_Level_5_Percent BETWEEN 0 AND 100),
  Performance_Level_5_Students INT,
  
  -- Attendance
  Chronic_Absenteeism_Percent DECIMAL(5,2) CHECK (Chronic_Absenteeism_Percent BETWEEN 0 AND 100),
  
  Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (District_ID) REFERENCES Districts(District_ID) ON DELETE CASCADE,
  FOREIGN KEY (School_ID) REFERENCES Schools(School_ID) ON DELETE CASCADE,
  FOREIGN KEY (Subgroup_ID) REFERENCES Subgroups(Subgroup_ID) ON DELETE CASCADE,
  
  INDEX idx_year (School_Year),
  INDEX idx_district (District_ID),
  INDEX idx_school (School_ID),
  INDEX idx_subgroup (Subgroup_ID),
  INDEX idx_grade (Grade_Level),
  INDEX idx_proficiency (English_Proficiency),
  
  UNIQUE KEY unique_performance_record (School_Year, District_ID, School_ID, Subgroup_ID, Grade_Level)
);

-- Teacher Quality Table: Teacher experience and certification metrics
CREATE TABLE Teacher_Quality (
  Teacher_Quality_ID INT AUTO_INCREMENT PRIMARY KEY,
  School_Year INT NOT NULL,
  District_ID INT,
  School_ID INT,
  
  -- Experienced Teachers
  Experienced_Teachers_High_Poverty_Percent DECIMAL(5,2) CHECK (Experienced_Teachers_High_Poverty_Percent BETWEEN 0 AND 100),
  Experienced_Teachers_Low_Poverty_Percent DECIMAL(5,2) CHECK (Experienced_Teachers_Low_Poverty_Percent BETWEEN 0 AND 100),
  
  -- Emergency Provisional Teachers
  Emergency_Provisional_High_Poverty_Percent DECIMAL(5,2) CHECK (Emergency_Provisional_High_Poverty_Percent BETWEEN 0 AND 100),
  Emergency_Provisional_Low_Poverty_Percent DECIMAL(5,2) CHECK (Emergency_Provisional_Low_Poverty_Percent BETWEEN 0 AND 100),
  
  -- In-Field Teachers
  In_Field_Teachers_High_Poverty_Percent DECIMAL(5,2) CHECK (In_Field_Teachers_High_Poverty_Percent BETWEEN 0 AND 100),
  In_Field_Teachers_Low_Poverty_Percent DECIMAL(5,2) CHECK (In_Field_Teachers_Low_Poverty_Percent BETWEEN 0 AND 100),
  
  -- Effective Teachers
  Effective_Teachers_High_Poverty_Percent DECIMAL(5,2) CHECK (Effective_Teachers_High_Poverty_Percent BETWEEN 0 AND 100),
  Effective_Teachers_Low_Poverty_Percent DECIMAL(5,2) CHECK (Effective_Teachers_Low_Poverty_Percent BETWEEN 0 AND 100),
  
  Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (District_ID) REFERENCES Districts(District_ID) ON DELETE CASCADE,
  FOREIGN KEY (School_ID) REFERENCES Schools(School_ID) ON DELETE CASCADE,
  
  INDEX idx_year (School_Year),
  INDEX idx_district (District_ID),
  INDEX idx_school (School_ID),
  
  UNIQUE KEY unique_teacher_record (School_Year, District_ID, School_ID)
);

-- NAEP Assessments Table: National Assessment of Educational Progress data
CREATE TABLE NAEP_Assessments (
  NAEP_ID INT AUTO_INCREMENT PRIMARY KEY,
  School_Year INT NOT NULL,
  District_ID INT,
  School_ID INT,
  Subgroup_ID INT NOT NULL,
  
  -- 4th Grade Math
  Grade_4_Math_Below_Basic DECIMAL(5,2) CHECK (Grade_4_Math_Below_Basic BETWEEN 0 AND 100),
  Grade_4_Math_Basic DECIMAL(5,2) CHECK (Grade_4_Math_Basic BETWEEN 0 AND 100),
  Grade_4_Math_Proficient DECIMAL(5,2) CHECK (Grade_4_Math_Proficient BETWEEN 0 AND 100),
  Grade_4_Math_Advanced DECIMAL(5,2) CHECK (Grade_4_Math_Advanced BETWEEN 0 AND 100),
  
  -- 4th Grade Reading
  Grade_4_Reading_Below_Basic DECIMAL(5,2) CHECK (Grade_4_Reading_Below_Basic BETWEEN 0 AND 100),
  Grade_4_Reading_Basic DECIMAL(5,2) CHECK (Grade_4_Reading_Basic BETWEEN 0 AND 100),
  Grade_4_Reading_Proficient DECIMAL(5,2) CHECK (Grade_4_Reading_Proficient BETWEEN 0 AND 100),
  Grade_4_Reading_Advanced DECIMAL(5,2) CHECK (Grade_4_Reading_Advanced BETWEEN 0 AND 100),
  
  -- 8th Grade Math
  Grade_8_Math_Below_Basic DECIMAL(5,2) CHECK (Grade_8_Math_Below_Basic BETWEEN 0 AND 100),
  Grade_8_Math_Basic DECIMAL(5,2) CHECK (Grade_8_Math_Basic BETWEEN 0 AND 100),
  Grade_8_Math_Proficient DECIMAL(5,2) CHECK (Grade_8_Math_Proficient BETWEEN 0 AND 100),
  Grade_8_Math_Advanced DECIMAL(5,2) CHECK (Grade_8_Math_Advanced BETWEEN 0 AND 100),
  
  -- 8th Grade Reading
  Grade_8_Reading_Below_Basic DECIMAL(5,2) CHECK (Grade_8_Reading_Below_Basic BETWEEN 0 AND 100),
  Grade_8_Reading_Basic DECIMAL(5,2) CHECK (Grade_8_Reading_Basic BETWEEN 0 AND 100),
  Grade_8_Reading_Proficient DECIMAL(5,2) CHECK (Grade_8_Reading_Proficient BETWEEN 0 AND 100),
  Grade_8_Reading_Advanced DECIMAL(5,2) CHECK (Grade_8_Reading_Advanced BETWEEN 0 AND 100),
  
  Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (District_ID) REFERENCES Districts(District_ID) ON DELETE CASCADE,
  FOREIGN KEY (School_ID) REFERENCES Schools(School_ID) ON DELETE CASCADE,
  FOREIGN KEY (Subgroup_ID) REFERENCES Subgroups(Subgroup_ID) ON DELETE CASCADE,
  
  INDEX idx_year (School_Year),
  INDEX idx_district (District_ID),
  INDEX idx_school (School_ID),
  INDEX idx_subgroup (Subgroup_ID),
  
  UNIQUE KEY unique_naep_record (School_Year, District_ID, School_ID, Subgroup_ID)
);

-- Insert default subgroups based on the data
INSERT INTO Subgroups (Subgroup_Name, Subgroup_Category) VALUES
('All', 'All'),
('Female', 'Gender'),
('Male', 'Gender'),
('Black or African American', 'Race_Ethnicity'),
('White', 'Race_Ethnicity'),
('Alaskan Native or Native American', 'Race_Ethnicity'),
('Asian', 'Race_Ethnicity'),
('Hispanic or Latino', 'Race_Ethnicity'),
('Native Hawaiian or Pacific Islander', 'Race_Ethnicity'),
('Two or More Races', 'Race_Ethnicity');

COMMIT;