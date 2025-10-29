# 📊 Data Accuracy Guide
## Mississippi Literacy Database - Validation & Maintenance Procedures

### 🎯 Overview
This guide provides comprehensive procedures to ensure accuracy between `create_tables_new.sql`, `literacy_data.sql`, and the MySQL database (`literacy_db`).

---

## 🛠️ Validation Tools

### **1. Database Validation Script**
**File:** `dev/validate_database.py`

**Purpose:** Comprehensive validation of schema consistency, data integrity, and data quality

**Usage:**
```bash
python3 dev/validate_database.py
```

**Checks performed:**
- ✅ Schema consistency (required columns present)
- ✅ Referential integrity (no orphaned records)
- ✅ Data constraints (percentage ranges 0-100)
- ✅ NULL value analysis
- ✅ Source file vs database record counts

**Output:** Detailed JSON report saved to `dev/validation_report_YYYYMMDD_HHMMSS.json`

---

### **2. Data Cleanup Script**
**File:** `dev/cleanup_data.py`

**Purpose:** Handles NULL values, sub-1% data standardization, and performance optimization

**Usage:**
```bash
python3 dev/cleanup_data.py
```

**Operations performed:**
- 🔧 Converts NULL percentages to 0.0 (conservative sub-1% estimate)
- 📋 Adds `Data_Quality_Flags` column to track data quality issues
- ✅ Validates percentage constraints
- ⚡ Creates performance indexes

**Output:** Cleanup report saved to `dev/cleanup_report_YYYYMMDD_HHMMSS.json`

---

### **3. Health Monitoring Script**
**File:** `dev/monitor_health.py`

**Purpose:** Lightweight daily health checks and alerting

**Usage:**
```bash
python3 dev/monitor_health.py
```

**Monitoring:**
- 🔗 Database connectivity
- 📊 Record count variance detection
- 🏷️ Data quality flag tracking
- 📅 Recent activity monitoring

**Scheduling:** Add to cron for daily monitoring:
```bash
# Daily at 8 AM
0 8 * * * cd /path/to/Literacy-Database && python3 dev/monitor_health.py
```

---

## 🔍 Current Status

### **✅ Issues Resolved**
1. **Schema inconsistencies:** Removed extra columns from Districts table
2. **NULL value handling:** Standardized 7,831 NULL values to 0.0 (sub-1% estimate)
3. **Data quality tracking:** Added metadata flags for 9,716 problematic records
4. **Percentage validation:** All values now within 0-100 range

### **⚠️ Remaining Warnings**
1. **Teacher_Quality table:** Empty (0 records) - needs data import
2. **NAEP_Assessments table:** Empty (0 records) - needs data import  
3. **Record count variance:** 18,162 source → 19,377 database (normalized data expansion)

---

## 📋 Recommended Workflow

### **Daily Operations**
1. **Health Check:** Run `python3 dev/monitor_health.py`
2. **Review alerts:** Check for record count variances or connectivity issues

### **Weekly Operations**
1. **Full Validation:** Run `python3 dev/validate_database.py`
2. **Review reports:** Check validation reports for new issues

### **After Data Updates**
1. **Pre-import validation:** Verify source file integrity
2. **Import data:** Use existing import scripts
3. **Post-import validation:** Run full validation suite
4. **Cleanup if needed:** Run cleanup script for data quality issues

---

## 🎯 Accuracy Assurance Methods

### **1. Schema Consistency**
```sql
-- Compare actual vs expected structure
SHOW CREATE TABLE table_name;

-- Verify constraints exist
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE 
FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = 'literacy_db';
```

### **2. Data Integrity Checks**
```sql
-- Check for orphaned records
SELECT COUNT(*) FROM Schools s 
LEFT JOIN Districts d ON s.District_ID = d.District_ID 
WHERE d.District_ID IS NULL;

-- Validate percentage ranges
SELECT COUNT(*) FROM Performance_Data 
WHERE English_Proficiency > 100 OR English_Proficiency < 0;
```

### **3. Source Data Verification**
```bash
# Count source records
grep -c "INSERT INTO" literacy_data.sql

# Compare with database
mysql -u user -p -e "SELECT COUNT(*) FROM Performance_Data;" literacy_db
```

---

## 🚨 Troubleshooting

### **High NULL Percentages**
- **Cause:** Sub-1% values from source data
- **Solution:** Run cleanup script to standardize values
- **Prevention:** Update import script to handle "<1%" strings

### **Record Count Mismatches**
- **Expected:** Source records may be normalized into multiple database records
- **Investigation:** Check if variance is within acceptable range (±10%)
- **Action:** If variance >10%, investigate data import process

### **Schema Drift**
- **Detection:** Validation script flags missing/extra columns
- **Resolution:** Update schema or validation expectations
- **Prevention:** Version control schema changes

---

## 📊 Performance Monitoring

### **Key Metrics to Track**
- Database connectivity uptime
- Record count stability
- Data quality flag trends  
- Query performance times

### **Alert Thresholds**
- Record count variance: >10%
- Database downtime: Any
- Data quality degradation: >20% increase in flagged records

---

## 🔄 Maintenance Schedule

| Frequency | Task | Script | Purpose |
|-----------|------|--------|---------|
| Daily | Health Check | `monitor_health.py` | Early issue detection |
| Weekly | Full Validation | `validate_database.py` | Comprehensive accuracy check |
| Monthly | Performance Review | Manual | Query optimization analysis |
| Quarterly | Schema Review | Manual | Evaluate structural changes |

---

## 📞 Support & Contact

For questions about data accuracy procedures:
1. Review validation reports in `dev/validation_report_*.json`
2. Check health logs in `dev/health_log.jsonl`
3. Run diagnostic scripts for detailed analysis

**Key Files:**
- Validation: `dev/validate_database.py`
- Cleanup: `dev/cleanup_data.py`  
- Monitoring: `dev/monitor_health.py`
- Reports: `dev/*_report_*.json`

---

*Last Updated: October 29, 2025*
*Database Status: ✅ Healthy (3 minor warnings)*