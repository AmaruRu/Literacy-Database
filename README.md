# 📖 Mississippi Literacy Database

> **Transform literacy data into actionable insights for Mississippi's educational future**

A comprehensive web application that analyzes literacy performance across Mississippi's school districts, providing interactive dashboards, geographic visualizations, book recommendations, and analytics to support educators, policymakers, and communities in improving educational outcomes.

## 🎯 Overview

The **Mississippi Literacy Database** provides an intuitive, data-driven platform for understanding educational performance across the state. With interactive charts, district rankings, literacy maps, and book recommendations, users can identify trends, track progress, and make informed decisions to support literacy improvement efforts.

### ✨ Key Features

- **📊 Interactive Dashboard** - Real-time analytics with dynamic charts and filtering
- **🗺️ Literacy Map** - Geographic visualization of county and district performance
- **📚 Book Recommendations** - Grade-level appropriate books with lexile filtering
- **🏆 District Rankings** - Performance comparisons across Mississippi school districts
- **🏫 School-Level Analysis** - Individual school performance within districts
- **👥 Demographic Analysis** - Performance breakdowns by race, gender, economic status
- **🔍 Advanced Filtering** - Multi-dimensional filters by county, city, school type, grade level
- **📱 Responsive Design** - Mobile-friendly interface accessible on any device
- **🔌 REST API** - Comprehensive data access for developers and researchers

## 🚀 Quick Start Guide

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed

### Setup (One Command!)
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Literacy-Database

# 2. Start services and import all data
docker-compose --profile setup up db-setup

# 3. Launch the application  
docker-compose up

# 4. Access your application
open http://localhost:5001
```

**That's it!** Your application is running with:
- ✅ Complete MySQL database with literacy performance data
- ✅ Book recommendations database with 1000+ titles
- ✅ Interactive dashboard with charts and analytics
- ✅ Geographic map with county/district visualization

### Application Features

**Homepage** (`/`) - Overview and navigation  
**Dashboard** (`/dashboard.html`) - Interactive analytics with filtering  
**Literacy Map** (`/map.html`) - Geographic performance visualization  
**Books** (`/books.html`) - Book recommendations by grade and lexile  
**Mission** (`/mission.html`) - About the platform  

## 🔌 API Reference

### Base URL
`http://localhost:5001/api`

### Core Endpoints
```http
GET /api/health                    # System status
GET /api/districts                 # All school districts  
GET /api/schools                   # Schools with optional district filter
GET /api/performance               # Performance data with filtering
GET /api/books                     # Book recommendations with filtering

# Analytics
GET /api/analytics/district-rankings        # Top performing districts
GET /api/analytics/subgroup-performance     # Demographic breakdowns  
GET /api/analytics/county-performance       # County-level aggregation

# Filtering Support
GET /api/filters/counties          # Available counties
GET /api/filters/cities            # Cities by county
GET /api/filters/school-types      # School type options
GET /api/filters/grade-levels      # Grade level options
```

### Example Usage
```bash
# Get top performing districts
curl http://localhost:5001/api/analytics/district-rankings

# Get books for 3rd grade
curl "http://localhost:5001/api/books?grade_level=3rd%20Grade"

# Get county performance data
curl http://localhost:5001/api/analytics/county-performance
```

## 🗄️ Database Schema

### Core Tables
- **📍 Locations**: Geographic data (county, city, zip code)
- **🏫 Districts**: 150+ Mississippi school districts
- **🎓 Schools**: 1000+ individual schools
- **👥 DemographicGroups**: Student subgroup classifications
- **📊 PerformanceRecords**: 18,630+ literacy performance records
- **📚 Books**: 1000+ book recommendations with grade/lexile data
- **👩‍🏫 TeacherQuality**: Teacher experience and certification metrics

## 🛠️ Technology Stack

**Backend**: Flask 3.1.2, SQLAlchemy ORM, MySQL 8.0  
**Frontend**: HTML5/CSS3, JavaScript ES6, Chart.js, Leaflet.js  
**Infrastructure**: Docker, Docker Compose  
**Data**: Mississippi Department of Education (2024)

## 📁 Project Structure

```
Literacy-Database/
├── 🐳 docker-compose.yml        # Multi-service orchestration
├── 🐳 Dockerfile               # Application container  
├── 📝 requirements.txt         # Python dependencies
├── 🐍 website.py              # Application entry point

├── 📁 data/                   # Data files
│   ├── Mississippi_Literacy_Dataset.csv
│   └── book_reco/Book_Recs.xls

├── 📁 scripts/               # Setup and maintenance scripts  
│   ├── sql/                  # SQL scripts
│   │   ├── init-db.sql       # Database initialization
│   │   ├── update_covers.sql # Book cover updates
│   │   └── update_all_covers.sql
│   ├── import_data.py        # Literacy data import
│   ├── import_books.py       # Book data import  
│   ├── update_covers.py      # Update book covers
│   └── generate_cover_sql.py # Generate cover update SQL

├── 📁 project/              # Main Flask application
│   ├── __init__.py          # App factory & configuration
│   ├── models.py           # SQLAlchemy database models  
│   ├── api.py             # REST API endpoints
│   ├── 📁 templates/       # HTML templates
│   │   ├── layout.html     # Base template
│   │   ├── dashboard.html  # Interactive dashboard
│   │   ├── books.html      # Book recommendations  
│   │   ├── map.html        # Geographic visualization
│   │   └── mission.html    # Mission/about page
│   └── 📁 static/         # Frontend assets
│       ├── 📁 css/
│       │   ├── styles.css  # Main application styles
│       │   └── books.css   # Book page styles
│       ├── dashboard.js    # Dashboard interactivity
│       ├── books.js        # Book search/filtering
│       ├── lit_map.js      # Map functionality
│       └── *.geojson       # Mississippi geographic data

└── 📁 updated_front/       # Alternative modern frontend -- currently not in use
```

## 🔧 Configuration

### Docker (Recommended)
No configuration needed! Docker handles all services automatically.

### Local Development  
Create `.env` file:
```env
MYSQL_HOST=localhost
MYSQL_USER=your_username  
MYSQL_PASSWORD=your_password
MYSQL_DB=MS_DBMS
FLASK_ENV=development
```

## 🔍 Troubleshooting

### Common Issues

**Port Conflicts**:
```bash
docker-compose down
docker-compose up -d
```

**Database Issues**:
```bash
# Reset everything
docker-compose down -v
docker-compose --profile setup up db-setup
docker-compose up
```

**Manual Data Import**:
```bash
docker-compose exec web python scripts/import_data.py
docker-compose exec web python scripts/import_books.py
```

## 👥 Use Cases

**For Educators**: Compare district performance, identify achievement gaps, track progress  
**For Policymakers**: State overview, equity analysis, data-driven funding decisions  
**For Researchers**: Clean data access via API, demographic analysis, longitudinal studies  
**For Communities**: School selection, advocacy, educational awareness  

## 🚀 Future Enhancements

- **📱 Mobile App**: Native mobile application
- **👥 User Authentication**: Role-based access control  
- **📊 Advanced Analytics**: Predictive modeling and ML insights
- **📄 Report Generation**: Automated PDF reports  
- **🔔 Alert System**: Performance change notifications

## 🤝 Contributing

We welcome contributions! Focus areas:
- 🎨 UI/UX improvements and accessibility
- 📊 Additional data visualizations  
- ⚡ Performance optimization
- 🧪 Testing and documentation

## 📄 License

MIT License - See LICENSE file for details.

## 🎯 Mission

**Empowering Mississippi communities with accessible, actionable literacy data to drive educational improvement and ensure every student has the opportunity to succeed.**

---

**🏆 Built with passion for Mississippi's educational future**

*Every data point represents a student's potential*

**Version**: 3.0.0 | **Updated**: November 2025