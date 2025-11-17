/**
 * Mississippi Literacy Dashboard JavaScript
 * Fetches and displays literacy data from the Flask API
 */

// Global variables for charts and state
let subgroupChart = null;
let performanceLevelsChart = null;
let schoolPerformanceChart = null;
let currentFilters = {
    county: '',
    city: '',
    zipCode: '',
    district: '',
    schoolType: '',
    gradeLevel: '',
    raceEthnicity: '',
    subgroupType: '',
    performanceRange: '',
    gradeSpan: ''
};
let currentView = 'districts'; // 'districts' or 'schools'

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
            populateFilters()
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
        
        // Use actual performance records count from health endpoint
        const totalRecords = healthData.counts.performance_records || 0;
        document.getElementById('total-students').textContent = totalRecords.toLocaleString();

    } catch (error) {
        console.error('Error loading key statistics:', error);
        throw error;
    }
}

async function loadDistrictRankings() {
    try {
        // Build URL with current filters
        let url = `${API_BASE}/analytics/district-rankings`;
        const params = new URLSearchParams();
        
        if (currentFilters.county) params.append('county', currentFilters.county);
        if (currentFilters.performanceRange) params.append('performance_range', currentFilters.performanceRange);
        
        if (params.toString()) {
            url += `?${params.toString()}`;
        }

        const response = await fetch(url);
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
                <td>
                    ${district.district_name}
                    ${district.county ? `<div class="county-badge">${district.county} County</div>` : ''}
                </td>
                <td><strong>${district.average_english_proficiency}%</strong></td>
                <td>${district.record_count}</td>
                <td>
                    <button class="action-btn" onclick="viewDistrictSchools(${district.district_id}, '${district.district_name}')">
                        View Schools
                    </button>
                </td>
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

async function populateFilters() {
    try {
        // Load all filter options in parallel
        const [
            countiesResponse,
            citiesResponse,
            zipCodesResponse,
            districtsResponse,
            schoolTypesResponse,
            gradeLevelsResponse,
            demographicGroupsResponse
        ] = await Promise.all([
            fetch(`${API_BASE}/filters/counties`),
            fetch(`${API_BASE}/filters/cities`),
            fetch(`${API_BASE}/filters/zip-codes`),
            fetch(`${API_BASE}/districts`),
            fetch(`${API_BASE}/filters/school-types`),
            fetch(`${API_BASE}/filters/grade-levels`),
            fetch(`${API_BASE}/filters/demographic-groups`)
        ]);

        // Parse responses
        const counties = await countiesResponse.json();
        const cities = await citiesResponse.json();
        const zipCodes = await zipCodesResponse.json();
        const districts = await districtsResponse.json();
        const schoolTypes = await schoolTypesResponse.json();
        const gradeLevels = await gradeLevelsResponse.json();
        const demographicGroups = await demographicGroupsResponse.json();

        // Populate county filter
        const countySelect = document.getElementById('county-filter');
        counties.data.forEach(county => {
            const option = document.createElement('option');
            option.value = county;
            option.textContent = county;
            countySelect.appendChild(option);
        });

        // Populate city filter
        const citySelect = document.getElementById('city-filter');
        cities.data.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });

        // Populate zip code filter
        const zipSelect = document.getElementById('zip-filter');
        zipCodes.data.forEach(zip => {
            const option = document.createElement('option');
            option.value = zip;
            option.textContent = zip;
            zipSelect.appendChild(option);
        });

        // Populate district filter
        const districtSelect = document.getElementById('district-filter');
        districts.data.forEach(district => {
            const option = document.createElement('option');
            option.value = district.district_id;
            option.textContent = district.district_name;
            districtSelect.appendChild(option);
        });

        // Populate school type filter
        const schoolTypeSelect = document.getElementById('school-type-filter');
        schoolTypes.data.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            schoolTypeSelect.appendChild(option);
        });

        // Populate grade level filter
        const gradeLevelSelect = document.getElementById('grade-level-filter');
        gradeLevels.data.forEach(grade => {
            const option = document.createElement('option');
            option.value = grade;
            option.textContent = grade;
            gradeLevelSelect.appendChild(option);
        });

        // Populate race/ethnicity filter
        const raceEthnicitySelect = document.getElementById('race-ethnicity-filter');
        demographicGroups.data.forEach(group => {
            const option = document.createElement('option');
            option.value = group.group_id;
            option.textContent = `${group.subgroup_name} (${group.subgroup_type})`;
            raceEthnicitySelect.appendChild(option);
        });

        // Add filter event listeners
        setupFilterListeners();
        
        console.log('All filters populated successfully');
    } catch (error) {
        console.error('Error populating filters:', error);
        throw error;
    }
}

function setupFilterListeners() {
    // County filter change - update cities and zip codes
    document.getElementById('county-filter').addEventListener('change', async function() {
        const selectedCounty = this.value;
        currentFilters.county = selectedCounty;
        
        // Update cities based on selected county
        await updateCitiesFilter(selectedCounty);
        await updateZipCodesFilter(selectedCounty, '');
        
        // Reload data with new filter
        await refreshData();
    });

    // City filter change - update zip codes
    document.getElementById('city-filter').addEventListener('change', async function() {
        const selectedCity = this.value;
        currentFilters.city = selectedCity;
        
        // Update zip codes based on selected city
        await updateZipCodesFilter(currentFilters.county, selectedCity);
        
        // Reload data with new filter
        await refreshData();
    });

    // All other filters
    ['zip-filter', 'district-filter', 'school-type-filter', 'grade-level-filter', 
     'race-ethnicity-filter', 'subgroup-type-filter', 'performance-filter'].forEach(filterId => {
        const element = document.getElementById(filterId);
        if (element) {
            element.addEventListener('change', async function() {
                // Update current filters
                if (filterId === 'zip-filter') currentFilters.zipCode = this.value;
                else if (filterId === 'district-filter') currentFilters.district = this.value;
                else if (filterId === 'school-type-filter') currentFilters.schoolType = this.value;
                else if (filterId === 'grade-level-filter') currentFilters.gradeLevel = this.value;
                else if (filterId === 'race-ethnicity-filter') currentFilters.raceEthnicity = this.value;
                else if (filterId === 'subgroup-type-filter') currentFilters.subgroupType = this.value;
                else if (filterId === 'performance-filter') currentFilters.performanceRange = this.value;

                // Handle subgroup type filter - update race/ethnicity options
                if (filterId === 'subgroup-type-filter') {
                    await updateRaceEthnicityFilter(this.value);
                }
                
                // Reload data with new filters
                await refreshData();
            });
        }
    });

    // Clear filters button
    document.getElementById('clear-filters').addEventListener('click', function() {
        clearAllFilters();
    });

    // School-level navigation
    const backButton = document.getElementById('back-to-districts');
    if (backButton) {
        backButton.addEventListener('click', function() {
            showDistrictsView();
        });
    }

    // Grade span filter (for school view)
    const gradeSpanSelect = document.getElementById('grade-span-filter');
    if (gradeSpanSelect) {
        gradeSpanSelect.addEventListener('change', function() {
            currentFilters.gradeSpan = this.value;
            if (currentView === 'schools') {
                loadSchoolPerformance(currentFilters.district, currentFilters.gradeSpan);
            }
        });
    }
}

async function updateCitiesFilter(selectedCounty) {
    try {
        const url = selectedCounty ? 
            `${API_BASE}/filters/cities?county=${encodeURIComponent(selectedCounty)}` : 
            `${API_BASE}/filters/cities`;
        
        const response = await fetch(url);
        const cities = await response.json();
        
        const citySelect = document.getElementById('city-filter');
        citySelect.innerHTML = '<option value="">All Cities</option>';
        
        cities.data.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error updating cities filter:', error);
    }
}

async function updateZipCodesFilter(selectedCounty, selectedCity) {
    try {
        let url = `${API_BASE}/filters/zip-codes`;
        const params = new URLSearchParams();
        
        if (selectedCounty) params.append('county', selectedCounty);
        if (selectedCity) params.append('city', selectedCity);
        
        if (params.toString()) url += `?${params.toString()}`;
        
        const response = await fetch(url);
        const zipCodes = await response.json();
        
        const zipSelect = document.getElementById('zip-filter');
        zipSelect.innerHTML = '<option value="">All Zip Codes</option>';
        
        zipCodes.data.forEach(zip => {
            const option = document.createElement('option');
            option.value = zip;
            option.textContent = zip;
            zipSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error updating zip codes filter:', error);
    }
}

async function updateRaceEthnicityFilter(selectedSubgroupType) {
    try {
        const url = selectedSubgroupType ? 
            `${API_BASE}/filters/demographic-groups?subgroup_type=${encodeURIComponent(selectedSubgroupType)}` : 
            `${API_BASE}/filters/demographic-groups`;
        
        const response = await fetch(url);
        const groups = await response.json();
        
        const raceEthnicitySelect = document.getElementById('race-ethnicity-filter');
        raceEthnicitySelect.innerHTML = '<option value="">All Groups</option>';
        
        groups.data.forEach(group => {
            const option = document.createElement('option');
            option.value = group.group_id;
            option.textContent = `${group.subgroup_name}`;
            raceEthnicitySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error updating race/ethnicity filter:', error);
    }
}

function clearAllFilters() {
    // Reset all filter values
    Object.keys(currentFilters).forEach(key => {
        currentFilters[key] = '';
    });
    
    // Reset all select elements
    ['county-filter', 'city-filter', 'zip-filter', 'district-filter', 
     'school-type-filter', 'grade-level-filter', 'race-ethnicity-filter', 
     'subgroup-type-filter', 'performance-filter'].forEach(filterId => {
        const select = document.getElementById(filterId);
        if (select) select.selectedIndex = 0;
    });
    
    // Reload data without filters
    refreshData();
}

async function refreshData() {
    try {
        showLoading(true);
        
        // Refresh district rankings and subgroup performance
        await Promise.all([
            loadDistrictRankings(),
            loadSubgroupPerformance(currentFilters.district || null)
        ]);
        
        showLoading(false);
    } catch (error) {
        console.error('Error refreshing data:', error);
        showError('Failed to refresh data: ' + error.message);
        showLoading(false);
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

// School drill-down functionality
async function viewDistrictSchools(districtId, districtName) {
    try {
        currentView = 'schools';
        currentFilters.district = districtId;
        
        // Update district name in the school section
        document.getElementById('selected-district-name').textContent = districtName;
        
        // Load school performance data
        await loadSchoolPerformance(districtId);
        
        // Show school details section and hide district rankings
        document.getElementById('rankings-section').style.display = 'none';
        document.getElementById('school-details-section').style.display = 'block';
        
    } catch (error) {
        console.error('Error viewing district schools:', error);
        showError('Failed to load school data: ' + error.message);
    }
}

async function loadSchoolPerformance(districtId, gradeSpan = null) {
    try {
        let url = `${API_BASE}/analytics/school-performance?district_id=${districtId}`;
        if (gradeSpan) {
            url += `&grade_span=${encodeURIComponent(gradeSpan)}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        // Update district statistics
        updateSchoolStats(data.district_info);
        
        // Populate grade span filter
        populateGradeSpanFilter(data.district_info.available_grade_spans);
        
        // Populate school rankings table
        populateSchoolRankings(data.data);
        
        // Create school performance chart
        createSchoolPerformanceChart(data.data, data.district_info.district_average);

    } catch (error) {
        console.error('Error loading school performance:', error);
        throw error;
    }
}

function updateSchoolStats(districtInfo) {
    document.getElementById('district-schools-count').textContent = districtInfo.total_schools;
    document.getElementById('district-avg-proficiency').textContent = `${districtInfo.district_average}%`;
    document.getElementById('schools-above-district-avg').textContent = districtInfo.schools_above_district_avg;
}

function populateGradeSpanFilter(gradeSpans) {
    const select = document.getElementById('grade-span-filter');
    
    // Clear existing options except the first one
    while (select.children.length > 1) {
        select.removeChild(select.lastChild);
    }
    
    gradeSpans.forEach(span => {
        const option = document.createElement('option');
        option.value = span;
        option.textContent = span;
        select.appendChild(option);
    });
}

function populateSchoolRankings(schools) {
    const tbody = document.getElementById('school-rankings');
    tbody.innerHTML = '';

    schools.forEach(school => {
        const row = document.createElement('tr');
        
        // Performance indicator
        let indicator = '';
        if (school.vs_district_indicator === 'above') {
            indicator = '<span class="performance-indicator above">↑ Above</span>';
        } else if (school.vs_district_indicator === 'below') {
            indicator = '<span class="performance-indicator below">↓ Below</span>';
        } else {
            indicator = '<span class="performance-indicator equal">= Equal</span>';
        }

        row.innerHTML = `
            <td class="rank-number">${school.rank}</td>
            <td>${school.school_name}</td>
            <td>${school.grade_span}</td>
            <td><strong>${school.average_english_proficiency}%</strong></td>
            <td>${indicator} (${school.vs_district_avg >= 0 ? '+' : ''}${school.vs_district_avg}%)</td>
        `;
        tbody.appendChild(row);
    });
}

function createSchoolPerformanceChart(schools, districtAverage) {
    const ctx = document.getElementById('school-performance-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (schoolPerformanceChart) {
        schoolPerformanceChart.destroy();
    }

    const labels = schools.map(school => school.school_name.length > 20 ? 
        school.school_name.substring(0, 20) + '...' : school.school_name);
    const proficiencies = schools.map(school => school.average_english_proficiency);
    
    // Color-code bars based on performance vs district average
    const backgroundColors = schools.map(school => {
        if (school.average_english_proficiency > districtAverage) {
            return '#28a745'; // Green for above average
        } else if (school.average_english_proficiency === districtAverage) {
            return '#ffc107'; // Yellow for equal
        } else {
            return '#dc3545'; // Red for below average
        }
    });

    schoolPerformanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'English Proficiency (%)',
                data: proficiencies,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color + 'CC'),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'School Performance Comparison'
                }
            },
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
                        text: 'Schools'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            // Add district average line
            plugins: [{
                afterDraw: function(chart) {
                    const ctx = chart.ctx;
                    const yAxis = chart.scales.y;
                    const yPos = yAxis.getPixelForValue(districtAverage);
                    
                    ctx.save();
                    ctx.beginPath();
                    ctx.moveTo(chart.chartArea.left, yPos);
                    ctx.lineTo(chart.chartArea.right, yPos);
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = '#2c5aa0';
                    ctx.setLineDash([5, 5]);
                    ctx.stroke();
                    
                    // Add label
                    ctx.fillStyle = '#2c5aa0';
                    ctx.font = '12px Arial';
                    ctx.fillText(`District Avg: ${districtAverage}%`, chart.chartArea.left + 10, yPos - 5);
                    ctx.restore();
                }
            }]
        }
    });
}

function showDistrictsView() {
    currentView = 'districts';
    
    // Show district rankings and hide school details
    document.getElementById('rankings-section').style.display = 'block';
    document.getElementById('school-details-section').style.display = 'none';
    
    // Reset grade span filter
    document.getElementById('grade-span-filter').value = '';
    currentFilters.gradeSpan = '';
}