-- Initialize MS_DBMS Database
-- This script runs automatically when the MySQL container starts

CREATE DATABASE IF NOT EXISTS MS_DBMS;

-- Create user with full privileges on MS_DBMS database
CREATE USER IF NOT EXISTS 'literacy_user'@'%' IDENTIFIED BY 'literacy_pass123';
GRANT ALL PRIVILEGES ON MS_DBMS.* TO 'literacy_user'@'%';

-- Grant connection privileges
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON MS_DBMS.* TO 'literacy_user'@'%';

-- Refresh privileges
FLUSH PRIVILEGES;

USE MS_DBMS;