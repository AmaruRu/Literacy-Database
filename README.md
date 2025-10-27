# 📖 Read Mississippi: Literacy Database

A comprehensive Flask-based web application that analyzes literacy rates across Mississippi by school district, providing interactive dashboards and data visualizations to support educational decision-making and community awareness.

## 🎯 Purpose

**Read Mississippi** transforms raw literacy statistics from the Mississippi Department of Education into accessible, interactive visualizations. The platform serves educators, policy makers, researchers, and citizens with data-driven insights to address educational challenges and track progress toward literacy improvements.

## ✨ Current Features

- **📊 Interactive Dashboard**: Real-time literacy analytics with charts and rankings
- **🏆 District Rankings**: Performance comparisons across 147 Mississippi school districts
- **👥 Demographic Analysis**: Performance breakdowns by race, gender, and special populations
- **📈 Performance Levels**: 5-level proficiency distribution visualizations
- **🔍 Filtering & Search**: District-specific data filtering capabilities
- **📱 Responsive Design**: Mobile-friendly interface for accessibility

## 🗄️ Database Schema

The application uses a normalized MySQL database with comprehensive literacy data:

### Core Tables
- **Districts** (147 records): School district information and metadata
- **Schools** (853 records): Individual schools linked to districts
- **Subgroups** (29 categories): Demographic and special population classifications
- **Performance_Data** (19,377 records): Detailed literacy metrics with 5-level proficiency scales
- **Teacher_Quality**: Teacher experience and certification metrics by poverty level
- **NAEP_Assessments**: National assessment data for 4th and 8th grade reading/math

### Key Metrics Tracked
- English proficiency percentages and growth rates
- Performance level distributions (Levels 1-5)
- Chronic absenteeism rates
- Teacher quality indicators
- Student demographic breakdowns

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.2, SQLAlchemy ORM, Flask-Login
- **Database**: MySQL with PyMySQL connector and cryptography support
- **Frontend**: HTML5, CSS3, JavaScript ES6, Chart.js for visualizations
- **API**: RESTful JSON API with comprehensive endpoints
- **Authentication**: Flask-Login ready for user management
- **Environment**: Python-dotenv for configuration management

## 📋 Prerequisites

- Python 3.13+
- MySQL Server
- Virtual environment (recommended)

## 🚀 Installation & Setup

### Quick Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Literacy-Database
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=your_mysql_username
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DB=literacy_db
   ```

5. **Run automated setup**
   ```bash
   python3 setup.py
   ```
   
   This single command will:
   - ✅ Test MySQL connection
   - ✅ Create the `literacy_db` database
   - ✅ Create all tables with proper schema
   - ✅ Import 19,377+ literacy records
   - ✅ Validate the complete installation

6. **Start the application**
   ```bash
   python3 website.py
   ```

   The app will start on `http://127.0.0.1:5001` and automatically open in your browser.

### Manual Setup (Alternative)

If you prefer manual setup or need to troubleshoot:

1. **Create MySQL database**
   ```bash
   mysql -u your_username -p -e "CREATE DATABASE literacy_db;"
   ```

2. **Run database schema**
   ```bash
   mysql -u your_username -p literacy_db < create_tables_new.sql
   ```

3. **Import data**
   ```bash
   python3 dev/import_data.py
   ```

## 📁 Project Structure

```
Literacy-Database/
├── 📁 project/              # Main Flask application
│   ├── __init__.py          # Flask app factory and configuration
│   ├── api.py               # RESTful API endpoints
│   ├── models.py            # SQLAlchemy database models
│   ├── 📁 static/           # Static assets
│   │   ├── 📁 css/
│   │   │   └── styles.css   # Application styling
│   │   └── dashboard.js     # Dashboard functionality
│   └── 📁 templates/        # Jinja2 HTML templates
│       ├── layout.html      # Base template
│       ├── dashboard.html   # Interactive dashboard
│       ├── map.html         # Literacy map (placeholder)
│       ├── mission.html     # Mission page
│       └── books.html       # Resources page
├── 📁 dev/                  # Development tools
│   ├── import_data.py       # Data import script
│   ├── test_api.py          # API testing suite
│   └── test_models.py       # Model testing suite
├── website.py               # Application entry point
├── create_tables_new.sql    # Current database schema
├── literacy_data.sql        # Original data source (6MB)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore rules
└── README.md               # This documentation
```

## 🔧 Development Status

### ✅ Completed Features
- **🗄️ Database**: Normalized schema with 19,377+ literacy records from 147 districts
- **🔌 API**: Comprehensive RESTful endpoints for data access and analytics
- **📊 Dashboard**: Interactive visualizations with Chart.js integration
- **🏗️ Backend**: Complete Flask application with SQLAlchemy models
- **🎨 Frontend**: Responsive design with dynamic data loading
- **📈 Analytics**: District rankings, subgroup comparisons, performance distributions
- **🔍 Filtering**: District-specific data filtering and search capabilities
- **⚙️ Infrastructure**: Environment configuration, error handling, logging

### 🚧 Future Enhancements
- **🗺️ Interactive Map**: Mississippi district map with performance overlays
- **📱 Mobile App**: React Native or PWA for mobile access
- **👥 User Authentication**: Role-based access for educators and administrators  
- **📊 Advanced Analytics**: Trend analysis, predictive modeling, benchmarking
- **📄 Reporting**: PDF report generation for districts and schools
- **🔔 Alerts**: Performance threshold notifications and updates

### 📊 Current Data Coverage
- **147 School Districts** across Mississippi
- **853 Individual Schools** with detailed metrics
- **29 Demographic Subgroups** for comprehensive analysis
- **2024 School Year** data from Mississippi Department of Education
- **Performance Levels 1-5** with student count and percentage breakdowns

## 🔌 API Endpoints

The application provides a comprehensive REST API for accessing literacy data:

### Core Endpoints
- `GET /api/health` - System health check and database connectivity
- `GET /api/districts` - List all 147 school districts
- `GET /api/districts/{id}` - Detailed district information with schools
- `GET /api/schools` - All schools with optional district filtering
- `GET /api/subgroups` - Demographic categories and classifications
- `GET /api/performance` - Performance data with flexible filtering

### Analytics Endpoints  
- `GET /api/analytics/district-rankings` - Top performing districts by English proficiency
- `GET /api/analytics/subgroup-performance` - Performance comparison across demographics

### Usage Examples
```bash
# Get top performing districts
curl http://localhost:5001/api/analytics/district-rankings

# Get performance data for a specific district
curl http://localhost:5001/api/performance?district_id=1

# Get demographic performance statewide
curl http://localhost:5001/api/analytics/subgroup-performance
```

## 🐛 Troubleshooting

### Common Issues

**MySQL Connection Errors**
- Ensure MySQL server is running: `brew services start mysql` (macOS)
- Verify credentials in `.env` file match your MySQL setup
- Check that `literacy_db` database exists: `SHOW DATABASES;`
- Install cryptography: `pip install cryptography`

**Import/Dependency Errors**
- Activate virtual environment: `source .venv/bin/activate`
- Install all dependencies: `pip install -r requirements.txt`
- Python version compatibility: Requires Python 3.13+

**Password with Special Characters**
- The app handles URL encoding automatically with `quote_plus()`
- No need to manually encode passwords in `.env`
- Use quotes around passwords with special characters

**Port Conflicts**
- Default port changed to 5001 to avoid AirPlay conflicts on macOS
- Modify `website.py` if you need a different port

**Data Loading Issues**
- Ensure `literacy_data.sql` is in the root directory for import
- Check database permissions for the MySQL user
- Verify sufficient disk space for the 6MB dataset

## 🤝 Contributing

This project aims to improve literacy awareness in Mississippi. We welcome contributions for:

### Priority Areas
- **🗺️ Interactive Maps**: Mississippi district boundary visualizations
- **📊 Advanced Analytics**: Trend analysis, predictive modeling, statistical insights  
- **📱 Mobile Experience**: Progressive Web App (PWA) capabilities
- **🎨 UI/UX Improvements**: Accessibility, design enhancements, user experience
- **⚡ Performance**: Database query optimization, caching strategies
- **📋 Testing**: Unit tests, integration tests, API documentation

### Development Setup
1. Fork the repository and create a feature branch
2. Follow the installation instructions above
3. Use the development tools in the `/dev` folder for testing
4. Run tests: `python3 dev/test_api.py` and `python3 dev/test_models.py`
5. Submit a pull request with clear description of changes

### Code Standards
- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Include docstrings for new functions and classes
- Test API endpoints with the provided test suite

## 📊 Data Sources

- **Primary Data**: Mississippi Department of Education (2024 School Year)
- **Coverage**: All public school districts in Mississippi
- **Metrics**: English proficiency, performance levels, demographic breakdowns
- **Quality**: Cleaned and normalized data with comprehensive validation

## 📄 License

Educational project for literacy analysis and community awareness. Open source under MIT License.

## 🎯 Impact Goals

This platform supports Mississippi's literacy improvement efforts by:
- **Identifying Achievement Gaps**: Highlighting disparities across demographic groups
- **Informing Policy Decisions**: Providing data-driven insights for educators and policymakers  
- **Community Engagement**: Making literacy data accessible to parents and community members
- **Progress Tracking**: Enabling districts to monitor and celebrate improvements
- **Resource Allocation**: Supporting evidence-based funding and program decisions

---

*Built with 📚 for Mississippi's Future - Every Page Turned is a Step Toward Change*
