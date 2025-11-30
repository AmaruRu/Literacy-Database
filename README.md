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

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Setup
```bash
# 1. Clone and navigate to the repository
git clone <your-repo-url>
cd Literacy-Database

# 2. Import data (runs once, takes ~2 minutes)
docker-compose --profile setup up db-setup

# 3. Start the application
docker-compose up -d

# 4. Open in your browser
http://localhost:5001
```

**✅ Setup Complete!** Your application includes:
- 18,630 literacy performance records across 150 MS districts
- 259 book recommendations with grade/lexile filtering  
- Interactive dashboard and geographic visualization

### Pages
- **Dashboard** (`/dashboard.html`) - Interactive charts with filtering
- **Literacy Map** (`/map.html`) - Geographic county visualization  
- **Books** (`/books.html`) - Grade-level book recommendations
- **API** (`/api/health`) - REST endpoints for data access  

## 🔌 API Endpoints

Base URL: `http://localhost:5001/api`

```bash
# Core Data
GET /api/districts                    # All MS school districts  
GET /api/performance                  # Literacy performance data
GET /api/books?grade_level=3rd+Grade  # Book recommendations

# Analytics  
GET /api/analytics/district-rankings  # Top performing districts
GET /api/analytics/county-performance # County averages
GET /api/health                       # System status
```

## 🛠️ Technology Stack

**Backend**: Flask + SQLAlchemy + MySQL 8.0  
**Frontend**: HTML5/CSS3 + JavaScript ES6 + Chart.js + Leaflet.js  
**Infrastructure**: Docker Compose  
**Data**: Mississippi Department of Education (2024)

## 📁 Key Files

- `docker-compose.yml` - Container orchestration
- `project/api.py` - REST API endpoints (20+ routes)
- `project/models.py` - Database schema (8 tables)
- `scripts/import_data.py` - Data pipeline from CSV
- `data/` - MS literacy dataset + book recommendations

## 🔧 Troubleshooting

**Port already in use**: `docker-compose down && docker-compose up -d`

**Data not loading**: `docker-compose down -v && docker-compose --profile setup up db-setup && docker-compose up -d`

**Application not responding**: Check containers are running with `docker-compose ps`

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