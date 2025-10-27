# 📖 Read Mississippi: Literacy Database

A Flask-based web application that analyzes literacy rates across Mississippi by county/school district, grade level, and demographic factors. This platform aims to raise awareness about literacy rates and empower communities to take action through data visualization and insights.

## 🎯 Purpose

**Read Mississippi** transforms raw literacy statistics into an accessible, web-based tool for understanding and addressing Mississippi's educational challenges. The platform serves educators, policy makers, researchers, and citizens interested in educational outcomes.

## ✨ Features

- **Interactive Literacy Map**: Visualize literacy rates across Mississippi counties and school districts
- **Data Dashboard**: View reading proficiency, math proficiency, and graduation rates
- **Demographics Analysis**: Track performance across different demographic groups
- **Book Resources**: Access educational materials and reading resources
- **Mission & Information Hub**: Learn about literacy initiatives

## 🗄️ Database Schema

The application uses a MySQL database with three main tables:

### District Table
- Stores school district information
- Fields: District_ID, Name, Type, City, County, Zip_Code, Grades_Served, Enrollment
- Indexed by City, County, and Type

### Demographics Table  
- Demographic data for each district by year
- Fields: Percent_Black, Percent_White, Percent_Hispanic, Percent_LowIncome, Percent_EnglishLearners
- Foreign key relationship to District table

### Performance Table
- Academic performance metrics by district and year  
- Fields: Reading_Proficiency, Math_Proficiency, Graduation_Rate
- Foreign key relationship to District table

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.2, SQLAlchemy, Flask-Login
- **Database**: MySQL with PyMySQL connector
- **Frontend**: HTML templates, CSS, JavaScript
- **Authentication**: Ready for user management with Flask-Login
- **Environment**: Python-dotenv for configuration

## 📋 Prerequisites

- Python 3.13+
- MySQL Server
- Virtual environment (recommended)

## 🚀 Installation & Setup

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

4. **Set up MySQL database**
   - Create a MySQL database named `literacy_db`
   - Run the schema:
   ```bash
   mysql -u your_username -p literacy_db < create_tables.sql
   ```

5. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=your_mysql_username
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DB=literacy_db
   ```

6. **Run the application**
   ```bash
   python3 website.py
   ```

   The app will start on `http://127.0.0.1:5000` and automatically open in your browser.

## 📁 Project Structure

```
Literacy-Database/
├── project/
│   ├── __init__.py          # Flask app factory and configuration
│   ├── models.py            # SQLAlchemy database models
│   ├── static/
│   │   └── css/
│   │       └── styles.css   # Application styling
│   └── templates/           # HTML templates
│       ├── layout.html      # Base template
│       ├── dashboard.html   # Data dashboard
│       ├── map.html         # Literacy map
│       ├── mission.html     # Mission page
│       ├── books.html       # Resources page
│       └── script.js        # Frontend JavaScript
├── website.py               # Main application entry point
├── create_tables.sql        # Database schema
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Development Status

### ✅ Completed
- Flask application framework setup
- MySQL database connection with URL encoding
- Basic routing for all main pages
- User authentication model (Flask-Login ready)
- Database schema design and creation
- Environment configuration
- Static file serving

### 🚧 In Progress / Next Steps
- Create SQLAlchemy models for District, Demographics, and Performance tables
- Implement API endpoints for CRUD operations
- Add data visualization components (charts, graphs)
- Populate database with actual Mississippi literacy data
- Implement interactive map functionality
- Add data import/export features

## 🐛 Troubleshooting

### Common Issues

**MySQL Connection Errors**
- Ensure MySQL server is running
- Verify credentials in `.env` file
- Check that `literacy_db` database exists

**Import Errors**
- Make sure virtual environment is activated
- Install all dependencies: `pip install -r requirements.txt`

**Password with Special Characters**
- The app handles URL encoding automatically with `quote_plus()`
- No need to manually encode passwords in `.env`

## 🤝 Contributing

This project aims to improve literacy awareness in Mississippi. Contributions welcome for:
- Data visualization enhancements
- Additional demographic analysis features
- Performance optimizations
- Documentation improvements

## 📄 License

Educational project for literacy analysis and community awareness.

---

*Built with 📚 by Team Read - Every Page Turned is a Step Toward Change*
