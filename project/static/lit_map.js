// Initialize the map (centered on Mississippi)
const map = L.map("map", {
  center: [32.7364, -89.6678],
  zoom: 6,
  minZoom: 6.5,
  maxZoom: 10,
  maxBounds: [[29.5, -92.5], [36.0, -86.5]], // Restrict to Mississippi area with extra padding
  maxBoundsViscosity: 1.0, // Makes the bounds completely solid
  zoomControl: false // Disable default zoom buttons
});

// Use CartoDB Positron for a clean, light map style
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 10
}).addTo(map);


// Function to get color based on English proficiency
function getColor(proficiency) {
  if (!proficiency) return '#cccccc';  // Gray for no data
  return proficiency >= 80 ? '#2ecc71' :  // Green - High proficiency
         proficiency >= 60 ? '#f1c40f' :  // Yellow - Medium proficiency
         proficiency >= 40 ? '#e67e22' :  // Orange - Low proficiency
                            '#e74c3c';     // Red - Very low proficiency
}

// Store the current GeoJSON layer and view mode
let currentLayer = null;
let currentView = 'county'; // 'county' or 'district'
let literacyData = {};
let geoJsonDataCache = {
  county: null,
  district: null
};
let selectedLayer = null; // Track currently selected layer
let infoPanel = null; // Reference to info panel control

// Function to create popup content for county view
function createCountyPopup(countyName, county) {
  let popupContent = '<div style="min-width: 250px;">';
  popupContent += '<h3 style="margin: 0 0 10px 0; color: #4b2e83;">' + countyName + ' County</h3>';

  if (county) {
    popupContent += '<table style="width: 100%; border-collapse: collapse;">';

    if (county.english_proficiency !== null) {
      popupContent += '<tr><td><strong>English Proficiency:</strong></td><td style="text-align: right;">' +
                     county.english_proficiency + '%</td></tr>';
    }

    if (county.english_growth !== null) {
      popupContent += '<tr><td><strong>English Growth:</strong></td><td style="text-align: right;">' +
                     county.english_growth + '%</td></tr>';
    }

    if (county.chronic_absenteeism !== null) {
      popupContent += '<tr><td><strong>Chronic Absenteeism:</strong></td><td style="text-align: right;">' +
                     county.chronic_absenteeism + '%</td></tr>';
    }

    popupContent += '<tr><td><strong>Schools:</strong></td><td style="text-align: right;">' +
                   county.school_count + '</td></tr>';

    popupContent += '<tr><td><strong>School Districts:</strong></td><td style="text-align: right;">' +
                   county.district_count + '</td></tr>';

    if (county.districts && county.districts.length > 0) {
      popupContent += '<tr><td colspan="2" style="padding-top: 8px;"><strong>Districts:</strong><br>' +
                     county.districts.map(d => '• ' + d).join('<br>') + '</td></tr>';
    }

    if (county.school_year) {
      popupContent += '<tr><td colspan="2" style="padding-top: 8px; font-size: 0.9em; color: #666;">School Year: ' +
                     county.school_year + '</td></tr>';
    }

    popupContent += '</table>';
  } else {
    if (countyName === 'Issaquena') {
      popupContent += '<em style="color: #999;">Issaquena County has no school districts in the database.</em>';
    } else {
      popupContent += '<em style="color: #999;">No literacy data available</em>';
    }
  }

  popupContent += '</div>';
  return popupContent;
}

// Function to get county FIPS from description
function getCountyFIPS(description) {
  const lines = description.split('\n');
  for (let line of lines) {
    if (line.startsWith('COUNTYFP:')) {
      return line.split(':')[1].trim();
    }
  }
  return null;
}

// Mississippi county names by FIPS code
const MS_COUNTIES = {
  '001': 'Adams', '003': 'Alcorn', '005': 'Amite', '007': 'Attala', '009': 'Benton',
  '011': 'Bolivar', '013': 'Calhoun', '015': 'Carroll', '017': 'Chickasaw', '019': 'Choctaw',
  '021': 'Claiborne', '023': 'Clarke', '025': 'Clay', '027': 'Coahoma', '029': 'Copiah',
  '031': 'Covington', '033': 'DeSoto', '035': 'Forrest', '037': 'Franklin', '039': 'George',
  '041': 'Greene', '043': 'Grenada', '045': 'Hancock', '047': 'Harrison', '049': 'Hinds',
  '051': 'Holmes', '053': 'Humphreys', '055': 'Issaquena', '057': 'Itawamba', '059': 'Jackson',
  '061': 'Jasper', '063': 'Jefferson', '065': 'Jefferson Davis', '067': 'Jones', '069': 'Kemper',
  '071': 'Lafayette', '073': 'Lamar', '075': 'Lauderdale', '077': 'Lawrence', '079': 'Leake',
  '081': 'Lee', '083': 'Leflore', '085': 'Lincoln', '087': 'Lowndes', '089': 'Madison',
  '091': 'Marion', '093': 'Marshall', '095': 'Monroe', '097': 'Montgomery', '099': 'Neshoba',
  '101': 'Newton', '103': 'Noxubee', '105': 'Oktibbeha', '107': 'Panola', '109': 'Pearl River',
  '111': 'Perry', '113': 'Pike', '115': 'Pontotoc', '117': 'Prentiss', '119': 'Quitman',
  '121': 'Rankin', '123': 'Scott', '125': 'Sharkey', '127': 'Simpson', '129': 'Smith',
  '131': 'Stone', '133': 'Sunflower', '135': 'Tallahatchie', '137': 'Tate', '139': 'Tippah',
  '141': 'Tishomingo', '143': 'Tunica', '145': 'Union', '147': 'Walthall', '149': 'Warren',
  '151': 'Washington', '153': 'Wayne', '155': 'Webster', '157': 'Wilkinson', '159': 'Winston',
  '161': 'Yalobusha', '163': 'Yazoo'
};

// Cache for county district data to avoid duplicate fetches
const countyDistrictCache = {};

// Function to create popup content for district view (async loading)
async function createDistrictPopup(districtTitle, countyName) {
  let popupContent = '<div style="min-width: 300px;">';
  popupContent += '<h3 style="margin: 0 0 5px 0; color: #4b2e83;">Subdivision ' + districtTitle + '</h3>';
  popupContent += '<p style="margin: 0 0 10px 0; font-size: 0.95em; color: #666;">' + countyName + ' County</p>';

  // Fetch detailed district and school data for this county (with caching)
  try {
    let data;

    // Check cache first
    if (countyDistrictCache[countyName]) {
      data = countyDistrictCache[countyName];
    } else {
      const response = await fetch('/api/map/county/' + countyName);
      data = await response.json();
      countyDistrictCache[countyName] = data;
    }

    if (data.success && data.districts && data.districts.length > 0) {
      popupContent += '<div style="max-height: 400px; overflow-y: auto;">';
      popupContent += '<strong>School Districts in this subdivision:</strong><br><br>';

      const subdivisionNum = parseInt(districtTitle);

      // Show all districts (they can be shared across subdivisions)
      // But distribute schools uniquely across subdivisions
      for (let district of data.districts) {
        popupContent += '<div style="margin-bottom: 15px; padding: 10px; background: #f8f8f8; border-radius: 5px;">';
        popupContent += '<strong style="color: #4b2e83; font-size: 1.05em;">' + district.district_name + '</strong><br>';

        if (district.english_proficiency !== null) {
          popupContent += '<span style="font-size: 0.9em;">English Proficiency: ' + district.english_proficiency + '%</span><br>';
        }

        if (district.schools && district.schools.length > 0) {
          // Filter schools based on their actual county location from the database
          // Schools with county_name matching the subdivision's county should appear here
          const schoolsToShow = district.schools.filter(school => {
            // If school has county data, check if it matches this subdivision's county
            if (school.county_name) {
              // Database has "County Name County" format, GeoJSON has "County Name" format
              // So we need to check if school's county contains the subdivision's county name
              const schoolCounty = school.county_name.toLowerCase();
              const subdivCounty = countyName.toLowerCase();

              // Check if database county starts with GeoJSON county (e.g., "Adams County" starts with "Adams")
              return schoolCounty.startsWith(subdivCounty) || schoolCounty === subdivCounty + ' county';
            }
            // If no county data, fall back to hash-based assignment for consistency
            let hash = 0;
            for (let i = 0; i < school.school_name.length; i++) {
              hash = ((hash << 5) - hash) + school.school_name.charCodeAt(i);
              hash = hash & hash; // Convert to 32bit integer
            }
            const assignedSubdivision = (Math.abs(hash) % 5) + 1;
            return assignedSubdivision === subdivisionNum;
          });

          if (schoolsToShow.length > 0) {
            popupContent += '<details style="margin-top: 8px;">';
            popupContent += '<summary style="cursor: pointer; color: #4b2e83; font-weight: 600;">';
            popupContent += 'Schools in this area (' + schoolsToShow.length + ' of ' + district.school_count + ' total)';
            popupContent += '</summary>';
            popupContent += '<ul style="margin: 5px 0; padding-left: 20px; font-size: 0.9em;">';
            for (let school of schoolsToShow) {
              popupContent += '<li>' + school.school_name + '</li>';
            }
            popupContent += '</ul>';

            // Add note about other schools
            if (district.schools.length > schoolsToShow.length) {
              popupContent += '<div style="font-size: 0.85em; color: #666; margin-top: 5px; font-style: italic;">';
              popupContent += '(' + (district.schools.length - schoolsToShow.length) + ' more school(s) in other areas)';
              popupContent += '</div>';
            }

            popupContent += '</details>';
          } else {
            popupContent += '<span style="font-size: 0.9em; color: #666;">No schools in this area</span><br>';
            popupContent += '<span style="font-size: 0.85em; color: #888;">(See other subdivisions for ' + district.school_count + ' total schools)</span>';
          }
        } else {
          popupContent += '<span style="font-size: 0.9em; color: #666;">No schools data</span>';
        }

        popupContent += '</div>';
      }

      popupContent += '</div>';
    } else {
      popupContent += '<em style="color: #999;">No district data available</em>';
    }
  } catch (error) {
    console.error('Error loading district data:', error);
    popupContent += '<em style="color: #999;">Error loading district data</em>';
  }

  popupContent += '</div>';
  return popupContent;
}

// Function to reset selected layer style
function resetSelectedLayer() {
  if (selectedLayer) {
    const countyName = selectedLayer.feature.properties.name;
    const county = literacyData[countyName];
    const proficiency = county ? county.english_proficiency : null;

    selectedLayer.setStyle({
      color: '#4b2e83',
      weight: 2,
      opacity: 0.8,
      fillColor: getColor(proficiency),
      fillOpacity: 0.6
    });
    selectedLayer = null;
  }
}

// Function to update info panel
function updateInfoPanel(content) {
  if (infoPanel) {
    const container = infoPanel.getContainer();
    if (container) {
      container.innerHTML = content;
      container.style.display = 'block';
    }
  }
}

// Function to hide info panel
function hideInfoPanel() {
  if (infoPanel) {
    const container = infoPanel.getContainer();
    if (container) {
      container.style.display = 'none';
    }
  }
}

// Function to render county view
function renderCountyView() {
  if (!geoJsonDataCache.county) {
    console.error('County GeoJSON data not loaded');
    return;
  }

  // Remove existing layer
  if (currentLayer) {
    map.removeLayer(currentLayer);
  }

  // Reset selected layer
  selectedLayer = null;
  hideInfoPanel();

  currentLayer = L.geoJSON(geoJsonDataCache.county, {
    style: function(feature) {
      const countyName = feature.properties.name;
      const county = literacyData[countyName];
      const proficiency = county ? county.english_proficiency : null;

      return {
        color: '#4b2e83',
        weight: 2,
        opacity: 0.8,
        fillColor: getColor(proficiency),
        fillOpacity: 0.6
      };
    },
    onEachFeature: function(feature, layer) {
      const countyName = feature.properties.name;
      const county = literacyData[countyName];

      // Add click handler
      layer.on('click', function(e) {
        // Reset previous selection
        if (selectedLayer && selectedLayer !== this) {
          const prevCountyName = selectedLayer.feature.properties.name;
          const prevCounty = literacyData[prevCountyName];
          const prevProficiency = prevCounty ? prevCounty.english_proficiency : null;
          selectedLayer.setStyle({
            fillColor: getColor(prevProficiency),
            fillOpacity: 0.6
          });
        }

        // Highlight selected area in light blue color
        this.setStyle({
          fillColor: '#ccc8f8ff',
          fillOpacity: 0.7
        });

        selectedLayer = this;

        // Show popup content in info panel
        const popupContent = createCountyPopup(countyName, county);
        updateInfoPanel(popupContent);

        L.DomEvent.stopPropagation(e);
      });

      // Add hover effect
      layer.on('mouseover', function() {
        if (this !== selectedLayer) {
          this.setStyle({
            weight: 3,
            fillOpacity: 0.8
          });
        }
      });

      layer.on('mouseout', function() {
        if (this !== selectedLayer) {
          this.setStyle({
            weight: 2,
            fillOpacity: 0.6
          });
        }
      });
    }
  }).addTo(map);

  console.log('County view rendered');
}

// Function to render district view
function renderDistrictView() {
  if (!geoJsonDataCache.district) {
    console.error('District GeoJSON data not loaded');
    return;
  }

  // Remove existing layer
  if (currentLayer) {
    map.removeLayer(currentLayer);
  }

  // Reset selected layer
  selectedLayer = null;
  hideInfoPanel();

  // Create a map to track which counties we've already colored
  const countyColors = {};

  // Pre-process: determine color for each county using county_name property
  geoJsonDataCache.district.features.forEach(feature => {
    const countyName = feature.properties.county_name;
    if (countyName && !countyColors[countyName]) {
      const county = literacyData[countyName];
      const proficiency = county ? county.english_proficiency : null;
      countyColors[countyName] = getColor(proficiency);
    }
  });

  currentLayer = L.geoJSON(geoJsonDataCache.district, {
    style: function(feature) {
      const countyName = feature.properties.county_name;
      const fillColor = countyName && countyColors[countyName] ? countyColors[countyName] : '#cccccc';

      return {
        color: '#4b2e83',
        weight: 2,
        opacity: 0.8,
        fillColor: fillColor,
        fillOpacity: 0.6
      };
    },
    onEachFeature: function(feature, layer) {
      // Use county_name directly from properties (added during GeoJSON preprocessing)
      const countyName = feature.properties.county_name;
      const districtTitle = feature.properties.title;

      // Add click handler
      layer.on('click', async function(e) {
        // Reset previous selection
        if (selectedLayer && selectedLayer !== this) {
          const prevCountyName = selectedLayer.feature.properties.county_name;
          const prevColor = countyColors[prevCountyName] || '#cccccc';
          selectedLayer.setStyle({
            fillColor: prevColor,
            fillOpacity: 0.6
          });
        }

        // Highlight selected area in light blue color
        this.setStyle({
          fillColor: '#ccc8f8ff',
          fillOpacity: 0.7
        });

        selectedLayer = this;

        // Show loading in info panel
        updateInfoPanel('<div style="padding: 20px; text-align: center;">Loading district data...</div>');

        // Load and display content in info panel
        const content = await createDistrictPopup(districtTitle, countyName);
        updateInfoPanel(content);

        L.DomEvent.stopPropagation(e);
      });

      // Add hover effect
      layer.on('mouseover', function() {
        if (this !== selectedLayer) {
          this.setStyle({
            weight: 3,
            fillOpacity: 0.8
          });
        }
      });

      layer.on('mouseout', function() {
        if (this !== selectedLayer) {
          this.setStyle({
            weight: 2,
            fillOpacity: 0.6
          });
        }
      });
    }
  }).addTo(map);

  console.log('District view rendered');
}

// Function to toggle between views
function toggleView(newView) {
  if (newView === currentView) return;

  currentView = newView;

  if (currentView === 'county') {
    renderCountyView();
    document.getElementById('county-btn').classList.add('active');
    document.getElementById('district-btn').classList.remove('active');
  } else {
    renderDistrictView();
    document.getElementById('district-btn').classList.add('active');
    document.getElementById('county-btn').classList.remove('active');
  }
}

// Load data and initialize map
Promise.all([
  fetch('/api/map/districts').then(response => response.json()),
  fetch('/static/ms_counties_dissolved.geojson').then(response => response.json()),
  fetch('/static/ms_map.geojson').then(response => response.json())
])
  .then(([countyDataResponse, countyGeoJson, districtGeoJson]) => {
    literacyData = countyDataResponse.data || {};
    geoJsonDataCache.county = countyGeoJson;
    geoJsonDataCache.district = districtGeoJson;

    console.log('Loaded data for ' + Object.keys(literacyData).length + ' counties');

    // Add view toggle control
    const viewControl = L.control({ position: 'topleft' });

    viewControl.onAdd = function(map) {
      const div = L.DomUtil.create('div', 'view-control');

      div.innerHTML = `
        <div class="view-control-container">
          <button id="county-btn" class="view-btn active">County View</button>
          <button id="district-btn" class="view-btn">District View</button>
        </div>
      `;

      // Prevent map interactions when clicking on control
      L.DomEvent.disableClickPropagation(div);
      L.DomEvent.disableScrollPropagation(div);

      return div;
    };

    viewControl.addTo(map);

    // Add custom zoom slider control
    const zoomSlider = L.control({ position: 'topright' });

    zoomSlider.onAdd = function(map) {
      const div = L.DomUtil.create('div', 'zoom-slider-control');

      div.innerHTML = `
        <div class="zoom-slider-container">
          <span class="zoom-label">Zoom</span>
          <input type="range"
                 id="zoom-slider"
                 class="zoom-slider"
                 min="6.5"
                 max="10"
                 step="0.1"
                 value="${map.getZoom()}"
                 orient="horizontal">
          <div class="zoom-levels">
            <span>+</span>
            <span>-</span>
          </div>
        </div>
      `;

      // Prevent map interactions when using slider
      L.DomEvent.disableClickPropagation(div);
      L.DomEvent.disableScrollPropagation(div);

      return div;
    };

    zoomSlider.addTo(map);

    // Connect slider to map zoom
    const slider = document.getElementById('zoom-slider');
    if (slider) {
      slider.addEventListener('input', function() {
        map.setZoom(parseFloat(this.value));
      });

      // Update slider when map zoom changes
      map.on('zoomend', function() {
        slider.value = map.getZoom();
      });
    }

    // Add info panel control (below view buttons)
    infoPanel = L.control({ position: 'topleft' });

    infoPanel.onAdd = function(map) {
      const div = L.DomUtil.create('div', 'info-panel');
      div.style.display = 'none'; // Hidden by default
      div.style.backgroundColor = 'white';
      div.style.padding = '15px';
      div.style.marginTop = '10px';
      div.style.borderRadius = '5px';
      div.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
      div.style.maxWidth = '400px';
      div.style.maxHeight = '500px';
      div.style.overflowY = 'auto';

      // Prevent map interactions when clicking on panel
      L.DomEvent.disableClickPropagation(div);
      L.DomEvent.disableScrollPropagation(div);

      return div;
    };

    infoPanel.addTo(map);

    // Add event listeners to buttons
    document.getElementById('county-btn').addEventListener('click', function() {
      toggleView('county');
    });

    document.getElementById('district-btn').addEventListener('click', function() {
      toggleView('district');
    });

    // Click on map background to deselect
    map.on('click', function() {
      if (selectedLayer) {
        if (currentView === 'county') {
          const countyName = selectedLayer.feature.properties.name;
          const county = literacyData[countyName];
          const proficiency = county ? county.english_proficiency : null;
          selectedLayer.setStyle({
            fillColor: getColor(proficiency),
            fillOpacity: 0.6
          });
        } else {
          // District view - need to get the color from countyColors
          const countyName = selectedLayer.feature.properties.county_name;
          // Access countyColors from the current layer
          const layers = currentLayer.getLayers();
          let originalColor = '#cccccc';
          layers.forEach(l => {
            if (l.feature.properties.county_name === countyName) {
              const county = literacyData[countyName];
              const proficiency = county ? county.english_proficiency : null;
              originalColor = getColor(proficiency);
            }
          });
          selectedLayer.setStyle({
            fillColor: originalColor,
            fillOpacity: 0.6
          });
        }
        selectedLayer = null;
        hideInfoPanel();
      }
    });

    // Render initial view (county view)
    renderCountyView();

    // Fit map to show all of Mississippi with padding after a short delay
    setTimeout(() => {
      if (currentLayer) {
        const bounds = currentLayer.getBounds();
        map.fitBounds(bounds, {
          padding: [80, 80], // Increased padding to ensure nothing is cut off
          maxZoom: 7 // Don't zoom in too close
        });
      }
    }, 100);

    // Add legend (below zoom slider on right)
    const legend = L.control({ position: 'topright' });

    legend.onAdd = function(map) {
      const div = L.DomUtil.create('div', 'info legend');
      const grades = [0, 40, 60, 80];
      const labels = ['<strong>English Proficiency</strong><br><span style="font-size: 0.9em;">(County Average)</span>'];

      div.style.backgroundColor = 'white';
      div.style.padding = '10px';
      div.style.borderRadius = '5px';
      div.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';

      for (let i = 0; i < grades.length; i++) {
        labels.push(
          '<i style="background:' + getColor(grades[i] + 1) +
          '; width: 18px; height: 18px; display: inline-block; margin-right: 5px;"></i> ' +
          grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '%' : '+%')
        );
      }

      labels.push('<i style="background:#cccccc; width: 18px; height: 18px; display: inline-block; margin-right: 5px;"></i> No data');

      div.innerHTML = labels.join('<br>');
      return div;
    };

    legend.addTo(map);

    console.log('Map loaded successfully');
  })
  .catch(error => {
    console.error('Error loading map data:', error);
    alert('Failed to load literacy data. Please check the console for details.');
  });
