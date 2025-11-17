# 📖 Mississippi Literacy Database

> **Transform literacy data into actionable insights for Mississippi's educational future**

A comprehensive web application that analyzes literacy performance across Mississippi's school districts, providing interactive dashboards, data visualizations, and analytics to support educators, policymakers, and communities in improving educational outcomes.

## 🎯 Overview

The **Mississippi Literacy Database** provides an intuitive, data-driven platform for understanding educational performance across the state. With interactive charts, district rankings, and demographic analysis, users can identify trends, track progress, and make informed decisions to support literacy improvement efforts.

### ✨ Key Features

- **📊 Interactive Dashboard** - Real-time analytics with dynamic charts and visualizations
- **🏆 District Rankings** - Performance comparisons across 150 Mississippi school districts  
- **👥 Demographic Analysis** - Performance breakdowns by race, gender, economic status, and special populations
- **📈 Performance Metrics** - Advanced analytics including achievement gaps and trend analysis
- **🔍 Smart Filtering** - District-specific data exploration and comparison tools
- **📱 Responsive Design** - Mobile-friendly interface accessible on any device
- **🔌 REST API** - Comprehensive data access for developers and researchers

## 🚀 Quick Start Guide

### Option 1: Docker (Recommended)

**Prerequisites**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Literacy-Database

# 2. Start the application with Docker
docker compose up -d

# 3. Import the literacy data
docker compose --profile setup run db-setup

# 4. Access your application
open http://localhost:5001
```

**That's it!** Your application is running with a complete MySQL database containing 18,630 literacy records.

### Option 2: Local Development Setup

**Prerequisites**: Python 3.9+, MySQL 8.0+

```bash
# 1. Clone and setup environment
git clone <your-repo-url>
cd Literacy-Database
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure database connection
cp .env.example .env
# Edit .env with your MySQL credentials

# 4. Import data and run
python import_data.py
python website.py

# 5. Open dashboard
open http://localhost:5000
```

## 📊 Using the Dashboard

### 🏠 Homepage Features
- **Quick Statistics** - State-level literacy overview
- **Navigation** - Easy access to all application features

### 📈 Interactive Dashboard
Access comprehensive analytics at `/dashboard.html`:

#### **Key Statistics Panel**
- **School Districts**: Total count of districts in the database
- **Schools**: Number of individual schools tracked
- **State Average Proficiency**: Overall English proficiency percentage
- **Total Records**: Student performance data points

#### **District Rankings Table**
- **Top Performers**: Districts ranked by average English proficiency
- **Performance Metrics**: Proficiency percentages and student counts
- **Sortable Data**: Click headers to reorder by different criteria

#### **Subgroup Performance Charts**
- **Interactive Filtering**: Select specific districts or view statewide data
- **Demographic Breakdown**: Performance by:
  - **All Students**: Overall district performance
  - **Gender**: Male vs Female performance comparison
  - **Race/Ethnicity**: Performance across racial groups
  - **Economic Status**: Economically disadvantaged vs non-disadvantaged
  - **English Learners**: EL student performance tracking
  - **Special Education**: SPED student outcomes
  - **Special Populations**: Other specialized student groups

#### **Performance Level Distribution**
- **5-Level Proficiency Scale**: 
  - Level 1 (Below Basic) - Red
  - Level 2 (Approaching Basic) - Orange  
  - Level 3 (Basic) - Yellow
  - Level 4 (Proficient) - Green
  - Level 5 (Advanced) - Blue
- **Interactive Pie Chart**: Hover for detailed percentages

#### **Advanced Performance Metrics**
- **Achievement Gap**: Difference between highest and lowest performing subgroups
- **Districts Above Average**: Count and percentage of high-performing districts
- **Proficiency Trends**: Year-over-year improvement tracking
- **Impact Indicators**: Factors affecting student outcomes

### 📱 Mobile Experience
- **Responsive Design**: Full functionality on phones and tablets
- **Touch-Friendly**: Optimized for mobile interaction
- **Fast Loading**: Efficient data loading and caching

## 🔌 API Reference

### Authentication
Currently open access. Future versions will include role-based authentication.

### Base URL
- **Local Development**: `http://localhost:5000/api`
- **Docker Setup**: `http://localhost:5001/api`

### Core Endpoints

#### **Health Check**
```http
GET /api/health
```
**Response**: System status and database connectivity
```json
{
  "success": true,
  "status": "healthy",
  "database": "connected",
  "counts": {
    "districts": 150,
    "schools": 1003
  }
}
```

#### **Districts**
```http
GET /api/districts
```
**Response**: List of all school districts with basic information

#### **Schools**  
```http
GET /api/schools?district_id={id}
```
**Parameters**:
- `district_id` (optional): Filter schools by district

#### **Performance Data**
```http
GET /api/performance?district_id={id}&group_id={group}&limit={num}
```
**Parameters**:
- `district_id` (optional): Filter by district
- `group_id` (optional): Filter by demographic group
- `limit` (optional): Limit number of results

### Analytics Endpoints

#### **District Rankings**
```http
GET /api/analytics/district-rankings
```
**Response**: Top 20 districts ranked by English proficiency

#### **Subgroup Performance**
```http
GET /api/analytics/subgroup-performance?district_id={id}
```
**Parameters**:
- `district_id` (optional): Focus on specific district
**Response**: Performance comparison across all demographic groups

#### **Performance Metrics**
```http
GET /api/analytics/performance-metrics
```
**Response**: Advanced analytics including achievement gaps and trends

### Example Usage

```bash
# Get top performing districts
curl http://localhost:5001/api/analytics/district-rankings

# Get demographic performance for a specific district
curl http://localhost:5001/api/analytics/subgroup-performance?district_id=1

# Check system health
curl http://localhost:5001/api/health
```

## 🗄️ Database Schema

### Core Tables
- **📍 Locations** (109 records): Geographic data for districts
- **🏫 Districts** (150 records): School district information
- **🎓 Schools** (1,003 records): Individual schools with location links
- **👥 DemographicGroups** (71 records): Student subgroup classifications
- **📅 AcademicYears** (1 record): School year tracking
- **📊 PerformanceRecords** (18,630 records): Core literacy metrics
- **👩‍🏫 TeacherQuality** (150 records): Teacher experience and certification data
- **📋 NAEPAssessments**: National assessment comparison data

### Key Metrics Tracked
- **English Proficiency Percentages**: Primary literacy indicator
- **Performance Level Distributions**: 5-level proficiency breakdowns
- **Chronic Absenteeism Rates**: Attendance impact tracking
- **Teacher Quality Indicators**: Experience and certification metrics
- **Demographic Breakdowns**: Comprehensive subgroup analysis

## 🛠️ Technology Stack

### Backend
- **Flask 3.1.2**: Modern Python web framework
- **SQLAlchemy ORM**: Database abstraction and management
- **MySQL 8.0**: Production-grade database
- **PyMySQL**: Database connectivity
- **Python-dotenv**: Environment configuration

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript ES6**: Interactive functionality
- **Chart.js**: Dynamic data visualizations
- **Responsive Design**: Mobile-first approach

### Infrastructure
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-service orchestration
- **MySQL Container**: Isolated database environment
- **Health Checks**: Automated service monitoring

## 📁 Project Structure

```
Literacy-Database/
├── 🐳 docker-compose.yml        # Multi-container orchestration
├── 🐳 Dockerfile               # Application container
├── 🐳 init-db.sql             # Database initialization
├── 📊 Mississippi_Literacy_Dataset.csv  # Source data
├── 📝 requirements.txt         # Python dependencies
├── 🐍 website.py              # Application entry point
├── 📊 import_data.py          # Data import script
│
├── 📁 project/               # Main Flask application
│   ├── __init__.py           # App factory & configuration
│   ├── models.py            # SQLAlchemy database models
│   ├── api.py              # REST API endpoints
│   │
│   ├── 📁 templates/        # Jinja2 HTML templates
│   │   ├── layout.html      # Homepage template
│   │   └── dashboard.html   # Interactive dashboard
│   │
│   └── 📁 static/          # Frontend assets
│       ├── 📁 css/
│       │   └── styles.css   # Application styling
│       └── dashboard.js     # Dashboard functionality
│
└── 📁 dev/                 # Development tools (optional)
    ├── test_api.py         # API testing suite
    └── test_models.py      # Model testing
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for local development:

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=MS_DBMS

# Application Settings
FLASK_ENV=development
FLASK_APP=website.py
```

### Docker Configuration

The Docker setup includes:
- **MySQL 8.0 Container**: Isolated database with persistent storage
- **Flask Web Container**: Application server with auto-reload
- **Data Import Service**: One-time data population
- **Health Checks**: Automated service monitoring
- **Volume Persistence**: Data preserved across restarts

## 🔍 Troubleshooting

### Common Issues

#### **Docker Port Conflicts**
```bash
# If ports 5000 or 3306 are in use:
docker compose down
lsof -ti:5000 | xargs kill  # Kill conflicting process
docker compose up -d
```

#### **Database Connection Issues**
```bash
# Check MySQL container health:
docker compose ps
docker compose logs mysql

# Reset database:
docker compose down -v  # Removes volumes
docker compose up -d
docker compose --profile setup run db-setup
```

#### **Application Not Loading**
```bash
# Check web container logs:
docker compose logs web

# Restart services:
docker compose restart
```

#### **Data Import Failures**
```bash
# Manual data import:
docker compose exec web python import_data.py

# Check import logs:
docker compose logs db-setup
```

### Performance Optimization

#### **Database Queries**
- The application uses optimized SQLAlchemy queries with joins
- Indexes are automatically created for foreign keys
- Large datasets use pagination and limits

#### **Frontend Performance**
- Chart.js provides efficient rendering of large datasets
- API calls are cached where appropriate
- Mobile-responsive design minimizes data transfer

## 👥 Use Cases

### **For Educators**
- **District Comparison**: Compare your district's performance against state averages
- **Demographic Analysis**: Identify achievement gaps within your student populations
- **Progress Tracking**: Monitor improvement trends over time
- **Resource Planning**: Use data to inform teaching strategies and resource allocation

### **For Policymakers**
- **State Overview**: Comprehensive view of educational performance across Mississippi
- **Equity Analysis**: Identify districts and populations needing additional support
- **Funding Decisions**: Data-driven insights for budget and program allocation
- **Accountability**: Track progress toward literacy improvement goals

### **For Researchers**
- **Data Export**: Access clean, normalized literacy data via API
- **Statistical Analysis**: Performance metrics and demographic breakdowns
- **Longitudinal Studies**: Track educational outcomes over time
- **Comparative Research**: Mississippi data in context with national standards

### **For Communities**
- **School Selection**: Compare district and school performance metrics
- **Advocacy**: Use data to support education initiatives and funding
- **Awareness**: Understand local educational challenges and successes
- **Engagement**: Participate in data-driven discussions about education

## 🚀 Future Enhancements

### **Planned Features**
- **🗺️ Interactive Maps**: Geographic visualization of district performance
- **📱 Mobile App**: Native mobile application for enhanced accessibility
- **👥 User Authentication**: Role-based access for different user types
- **📊 Advanced Analytics**: Predictive modeling and trend analysis
- **📄 Report Generation**: Automated PDF reports for districts and schools
- **🔔 Alert System**: Notifications for performance changes and updates

### **Data Expansions**
- **Historical Data**: Multi-year trend analysis
- **Additional Metrics**: Math proficiency, graduation rates, college readiness
- **School-Level Detail**: Individual school performance breakdowns
- **National Comparisons**: NAEP and other national benchmark integration

## 📊 Data Sources & Quality

### **Primary Source**
- **Mississippi Department of Education** (2024 School Year)
- **Coverage**: All public school districts in Mississippi
- **Update Frequency**: Annual updates as new data becomes available

### **Data Quality**
- **Validation**: Comprehensive data cleaning and normalization
- **Completeness**: 18,630 performance records across 150 districts
- **Accuracy**: Cross-referenced with official MDE publications
- **Consistency**: Standardized demographic categories and performance scales

### **Data Processing**
1. **Raw Data Import**: CSV files from MDE databases
2. **Cleaning & Validation**: Remove duplicates, validate ranges
3. **Normalization**: Convert to relational database schema
4. **Quality Assurance**: Automated tests for data integrity
5. **Index Optimization**: Performance tuning for query efficiency

## 🤝 Contributing

We welcome contributions to improve literacy education in Mississippi!

### **Priority Areas**
- **🎨 UI/UX Improvements**: Accessibility, design enhancements
- **📊 Data Visualizations**: Additional chart types and analytics
- **⚡ Performance**: Database optimization and caching
- **📱 Mobile Experience**: Progressive Web App features
- **🧪 Testing**: Unit tests and integration testing
- **📚 Documentation**: User guides and API documentation

### **Development Workflow**
1. **Fork** the repository and create a feature branch
2. **Setup** the development environment using Docker or local setup
3. **Test** your changes using the provided test suites
4. **Document** any new features or API changes
5. **Submit** a pull request with clear description of changes

### **Code Standards**
- Follow **PEP 8** for Python code style
- Use meaningful variable and function names
- Include **docstrings** for new functions and classes
- Write **unit tests** for new functionality
- Update **documentation** for API changes

## 📄 License

This project is open source under the **MIT License**. See LICENSE file for details.

## 🎯 Impact & Mission

### **Our Mission**
Empowering Mississippi communities with accessible, actionable literacy data to drive educational improvement and ensure every student has the opportunity to succeed.

### **Impact Goals**
- **🔍 Identify Achievement Gaps**: Highlight disparities for targeted intervention
- **📈 Track Progress**: Monitor improvement efforts and celebrate successes  
- **💡 Inform Decisions**: Provide data-driven insights for educators and policymakers
- **🤝 Engage Communities**: Make education data accessible to all stakeholders
- **💰 Optimize Resources**: Support evidence-based funding and program decisions

---

## 🆘 Support & Contact

### **Getting Help**
- **Documentation**: This README and inline code comments
- **Issues**: Report bugs and feature requests via GitHub issues
- **API Testing**: Use the provided test suites in `/dev` folder
- **Community**: Join discussions about Mississippi education data

### **Quick Links**
- **Live Demo**: [Your deployed URL here]
- **API Documentation**: `/api` endpoints documented above
- **GitHub Repository**: [Your repo URL here]
- **Mississippi Department of Education**: [Official MDE Data](https://www.mdek12.org)

---

*🏆 Built with passion for Mississippi's educational future - Every data point represents a student's potential* 

**Version**: 2.0.0 | **Last Updated**: November 2025