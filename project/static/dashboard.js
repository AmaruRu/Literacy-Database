/**
 * Mississippi Literacy Dashboard JavaScript
 * Fetches and displays literacy data from the Flask API
 */

// Global variables for charts
let subgroupChart = null;
let performanceLevelsChart = null;

// API endpoints
const API_BASE = '/api';

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

async function initializeDashboard() {
    try {
        showLoading(true);
        
        // Load all dashboard data
        await Promise.all([
            loadKeyStatistics(),
            loadDistrictRankings(),
            loadSubgroupPerformance(),
            loadPerformanceLevels(),
            loadPerformanceMetrics(),
            loadDataSummary(),
            populateDistrictFilter()
        ]);
        
        showLoading(false);
        showDashboardSections();
        
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        showError('Failed to load dashboard data: ' + error.message);
        showLoading(false);
    }
}

async function loadKeyStatistics() {
    try {
        // Fetch basic statistics
        const [healthResponse, districtsResponse, schoolsResponse, subgroupResponse] = await Promise.all([
            fetch(`${API_BASE}/health`),
            fetch(`${API_BASE}/districts`),
            fetch(`${API_BASE}/schools`),
            fetch(`${API_BASE}/analytics/subgroup-performance`)
        ]);

        const healthData = await healthResponse.json();
        const districtsData = await districtsResponse.json();
        const schoolsData = await schoolsResponse.json();
        const subgroupData = await subgroupResponse.json();

        // Calculate state average proficiency (from 'All' subgroup)
        const allSubgroup = subgroupData.data.find(sg => sg.subgroup_name === 'All');
        const stateProficiency = allSubgroup ? allSubgroup.average_english_proficiency : 0;

        // Update statistics display
        document.getElementById('total-districts').textContent = districtsData.count || 0;
        document.getElementById('total-schools').textContent = schoolsData.count || 0;
        document.getElementById('state-proficiency').textContent = `${stateProficiency}%`;
        
        // Calculate total records
        const totalRecords = subgroupData.data.reduce((sum, sg) => sum + sg.record_count, 0);
        document.getElementById('total-students').textContent = totalRecords.toLocaleString();

    } catch (error) {
        console.error('Error loading key statistics:', error);
        throw error;
    }
}

async function loadDistrictRankings() {
    try {
        const response = await fetch(`${API_BASE}/analytics/district-rankings`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        const rankingsTable = document.getElementById('district-rankings');
        rankingsTable.innerHTML = '';

        data.data.forEach(district => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="rank-number">${district.rank}</td>
                <td>${district.district_name}</td>
                <td><strong>${district.average_english_proficiency}%</strong></td>
                <td>${district.record_count}</td>
            `;
            rankingsTable.appendChild(row);
        });

    } catch (error) {
        console.error('Error loading district rankings:', error);
        throw error;
    }
}

async function loadSubgroupPerformance(districtId = null) {
    try {
        let url = `${API_BASE}/analytics/subgroup-performance`;
        if (districtId) {
            url += `?district_id=${districtId}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        // Prepare data for chart
        const categories = {
            'All': [],
            'Gender': [],
            'Race': [],
            'EconStatus': [],
            'EL': [],
            'SPED': [],
            'SpecialPop': []
        };

        data.data.forEach(subgroup => {
            const category = subgroup.subgroup_category;
            if (categories[category]) {
                categories[category].push({
                    name: subgroup.subgroup_name,
                    proficiency: subgroup.average_english_proficiency || 0
                });
            }
        });

        // Create chart
        createSubgroupChart(categories);

    } catch (error) {
        console.error('Error loading subgroup performance:', error);
        throw error;
    }
}

async function loadPerformanceLevels() {
    try {
        const response = await fetch(`${API_BASE}/performance?subgroup_id=1&limit=1000`); // All students
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        // Aggregate performance levels
        const levelTotals = {
            'Level 1': 0,
            'Level 2': 0,
            'Level 3': 0,
            'Level 4': 0,
            'Level 5': 0
        };

        let totalStudents = 0;

        data.data.forEach(record => {
            const levels = record.performance_levels;
            if (levels) {
                for (let i = 1; i <= 5; i++) {
                    const level = levels[`level_${i}`];
                    if (level && level.students) {
                        levelTotals[`Level ${i}`] += level.students;
                        totalStudents += level.students;
                    }
                }
            }
        });

        // Convert to percentages
        const levelPercentages = {};
        Object.keys(levelTotals).forEach(level => {
            levelPercentages[level] = totalStudents > 0 ? 
                ((levelTotals[level] / totalStudents) * 100).toFixed(1) : 0;
        });

        createPerformanceLevelsChart(levelPercentages);

    } catch (error) {
        console.error('Error loading performance levels:', error);
        throw error;
    }
}

async function loadPerformanceMetrics() {
    try {
        const response = await fetch(`${API_BASE}/analytics/performance-metrics`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        const metrics = data.data;
        
        // Update performance metrics display
        const metricsContainer = document.getElementById('performance-metrics');
        if (metricsContainer) {
            metricsContainer.innerHTML = `
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h4>State Achievement Gap</h4>
                        <div class="metric-value">${metrics.achievement_gap?.toFixed(1) || 'N/A'}%</div>
                        <small>Difference between highest and lowest performing subgroups</small>
                    </div>
                    <div class="metric-card">
                        <h4>Districts Above State Average</h4>
                        <div class="metric-value">${metrics.districts_above_average || 'N/A'}</div>
                        <small>Out of ${metrics.total_districts || 0} districts</small>
                    </div>
                    <div class="metric-card">
                        <h4>Proficiency Trend</h4>
                        <div class="metric-value ${metrics.proficiency_trend >= 0 ? 'positive' : 'negative'}">
                            ${metrics.proficiency_trend >= 0 ? '+' : ''}${metrics.proficiency_trend?.toFixed(1) || 'N/A'}%
                        </div>
                        <small>Year-over-year change</small>
                    </div>
                    <div class="metric-card">
                        <h4>Average Class Size Impact</h4>
                        <div class="metric-value">${metrics.avg_class_size_impact?.toFixed(1) || 'N/A'}</div>
                        <small>Students per teacher correlation with performance</small>
                    </div>
                </div>
            `;
        }

    } catch (error) {
        console.error('Error loading performance metrics:', error);
        // Don't throw error to prevent dashboard failure
    }
}

async function loadDataSummary() {
    try {
        const response = await fetch(`${API_BASE}/performance?limit=1`);
        const data = await response.json();

        const summary = document.getElementById('data-summary');
        
        const lastUpdate = new Date().toLocaleDateString();
        
        summary.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <strong>Data Source:</strong><br>
                    Mississippi Department of Education
                </div>
                <div>
                    <strong>School Year:</strong><br>
                    2024
                </div>
                <div>
                    <strong>Last Updated:</strong><br>
                    ${lastUpdate}
                </div>
                <div>
                    <strong>Coverage:</strong><br>
                    All Public School Districts
                </div>
            </div>
            <div style="margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                <strong>About the Data:</strong> This dashboard displays literacy performance data from Mississippi's public school districts, 
                including English proficiency rates, performance level distributions, and demographic breakdowns to support 
                data-driven educational improvements.
            </div>
        `;

    } catch (error) {
        console.error('Error loading data summary:', error);
        throw error;
    }
}

async function populateDistrictFilter() {
    try {
        const response = await fetch(`${API_BASE}/districts`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        const select = document.getElementById('district-filter');
        
        // Sort districts alphabetically
        const sortedDistricts = data.data.sort((a, b) => 
            a.district_name.localeCompare(b.district_name)
        );

        sortedDistricts.forEach(district => {
            const option = document.createElement('option');
            option.value = district.district_id;
            option.textContent = district.district_name;
            select.appendChild(option);
        });

        // Add event listener for filter changes
        select.addEventListener('change', function() {
            const districtId = this.value || null;
            loadSubgroupPerformance(districtId);
        });

    } catch (error) {
        console.error('Error populating district filter:', error);
        throw error;
    }
}

function createSubgroupChart(categories) {
    const ctx = document.getElementById('subgroup-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (subgroupChart) {
        subgroupChart.destroy();
    }

    // Prepare datasets
    const datasets = [];
    const colors = {
        'All': '#2c5aa0',
        'Gender': '#28a745',
        'Race': '#dc3545',
        'EconStatus': '#ffc107',
        'EL': '#17a2b8',
        'SPED': '#6f42c1',
        'SpecialPop': '#fd7e14'
    };

    const categoryLabels = {
        'All': 'All Students',
        'Gender': 'Gender',
        'Race': 'Race/Ethnicity', 
        'EconStatus': 'Economic Status',
        'EL': 'English Learners',
        'SPED': 'Special Education',
        'SpecialPop': 'Special Populations'
    };

    Object.keys(categories).forEach(category => {
        if (categories[category].length > 0) {
            datasets.push({
                label: categoryLabels[category] || category,
                data: categories[category].map(item => item.proficiency),
                backgroundColor: colors[category] + '80', // Add transparency
                borderColor: colors[category],
                borderWidth: 1
            });
        }
    });

    // Get all unique subgroup names for labels
    const allLabels = [];
    Object.values(categories).forEach(items => {
        items.forEach(item => {
            if (!allLabels.includes(item.name)) {
                allLabels.push(item.name);
            }
        });
    });

    subgroupChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: allLabels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'English Proficiency (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Student Subgroups'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Average English Proficiency by Student Subgroup'
                }
            }
        }
    });
}

function createPerformanceLevelsChart(levelData) {
    const ctx = document.getElementById('performance-levels-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (performanceLevelsChart) {
        performanceLevelsChart.destroy();
    }

    const labels = Object.keys(levelData);
    const data = Object.values(levelData);

    performanceLevelsChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#dc3545', // Level 1 - Red (Below Basic)
                    '#fd7e14', // Level 2 - Orange (Approaching)
                    '#ffc107', // Level 3 - Yellow (Basic)
                    '#28a745', // Level 4 - Green (Proficient)
                    '#007bff'  // Level 5 - Blue (Advanced)
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'right'
                },
                title: {
                    display: true,
                    text: 'Student Distribution Across Performance Levels'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed}%`;
                        }
                    }
                }
            }
        }
    });
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    loading.style.display = show ? 'block' : 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('error-message');
    
    errorMessage.textContent = message;
    errorDiv.style.display = 'block';
}

function showDashboardSections() {
    const sections = [
        'stats-section',
        'rankings-section', 
        'subgroup-section',
        'performance-levels-section',
        'metrics-section',
        'updates-section'
    ];
    
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'block';
        }
    });
}