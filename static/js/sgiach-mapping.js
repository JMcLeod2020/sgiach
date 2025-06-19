// Sgiach Interactive Mapping System
// Professional Property Analysis with Municipal Validation

class SgiachMapping {
    constructor(containerId) {
        this.containerId = containerId;
        this.map = null;
        this.propertyMarker = null;
        this.utilityMarkers = [];
        this.amenityMarkers = [];
        this.currentProperty = null;
    }

    async initializeMap(coordinates, municipality) {
        // Initialize Leaflet map
        this.map = L.map(this.containerId).setView([coordinates.lat, coordinates.lng], 14);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);

        // Add property center marker
        this.propertyMarker = L.marker([coordinates.lat, coordinates.lng], {
            icon: this.createPropertyIcon()
        }).addTo(this.map);

        // Load property analysis
        await this.loadPropertyAnalysis(coordinates, municipality);
    }

    async loadPropertyAnalysis(coordinates, municipality) {
        try {
            const response = await fetch('/property/comprehensive-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    address: "Analysis Property",
                    coordinates: coordinates,
                    municipality: municipality,
                    property_type: "development",
                    size_hectares: 2.0,
                    zoning: "RF3",
                    analysis_type: "comprehensive"
                })
            });

            const analysisData = await response.json();
            this.currentProperty = analysisData;

            // Add map features
            this.addUtilityMarkers(analysisData.property_data.utility_connections);
            this.addAmenityMarkers(analysisData.property_data.amenity_features);
            
            // Update analysis panel
            this.updateAnalysisPanel(analysisData);

        } catch (error) {
            console.error('Property analysis failed:', error);
        }
    }

    createPropertyIcon() {
        return L.divIcon({
            html: '<div style="background: #e74c3c; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"><i class="fas fa-building"></i></div>',
            className: 'property-marker',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
    }

    addUtilityMarkers(utilities) {
        const utilityIcons = {
            water: '💧',
            sewer: '🚰', 
            electrical: '⚡',
            gas: '🔥',
            internet: '📶'
        };

        utilities.forEach(utility => {
            const marker = L.marker([utility.coordinates.lat, utility.coordinates.lng], {
                icon: L.divIcon({
                    html: `<div style="background: ${this.getStatusColor(utility.status)}; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; border: 2px solid white;">${utilityIcons[utility.utility_type] || '🔧'}</div>`,
                    className: 'utility-marker',
                    iconSize: [25, 25],
                    iconAnchor: [12, 12]
                })
            }).addTo(this.map);

            marker.bindPopup(`
                <div>
                    <h4>${utility.utility_type.toUpperCase()} Service</h4>
                    <p><strong>Distance:</strong> ${utility.distance}</p>
                    <p><strong>Cost:</strong> ${utility.connection_cost}</p>
                    <p><strong>Timeline:</strong> ${utility.timeline}</p>
                    <p><strong>Status:</strong> ${utility.status.replace('-', ' ')}</p>
                    <p>${utility.details}</p>
                </div>
            `);

            this.utilityMarkers.push(marker);
        });
    }

    addAmenityMarkers(amenities) {
        const amenityIcons = {
            transit: '🚊',
            park: '🌳',
            school: '🏫',
            healthcare: '🏥',
            retail: '🛒',
            employment: '🏢'
        };

        amenities.forEach(amenity => {
            const marker = L.marker([amenity.coordinates.lat, amenity.coordinates.lng], {
                icon: L.divIcon({
                    html: `<div style="background: ${this.getStatusColor(amenity.status)}; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; border: 2px solid white;">${amenityIcons[amenity.amenity_type] || '📍'}</div>`,
                    className: 'amenity-marker',
                    iconSize: [25, 25],
                    iconAnchor: [12, 12]
                })
            }).addTo(this.map);

            marker.bindPopup(`
                <div>
                    <h4>${amenity.name}</h4>
                    <p><strong>Distance:</strong> ${amenity.distance}</p>
                    <p><strong>Impact:</strong> ${amenity.impact}</p>
                    <p><strong>Validation:</strong> ${amenity.validation}</p>
                </div>
            `);

            this.amenityMarkers.push(marker);
        });
    }

    getStatusColor(status) {
        const colors = {
            'available': '#27ae60',
            'excellent': '#27ae60',
            'good': '#27ae60',
            'extension-required': '#f39c12',
            'adequate': '#f39c12',
            'limited': '#f39c12',
            'major-infrastructure': '#e74c3c',
            'private-system': '#e74c3c',
            'pending': '#95a5a6'
        };
        return colors[status] || '#95a5a6';
    }

    updateAnalysisPanel(analysisData) {
        const panelHtml = `
            <div class="analysis-panel">
                <h3>Property Analysis Summary</h3>
                <div class="summary-grid">
                    <div class="summary-item">
                        <h4>Infrastructure Cost</h4>
                        <p>$${analysisData.property_data.infrastructure.total_cost_min.toLocaleString()} - $${analysisData.property_data.infrastructure.total_cost_max.toLocaleString()}</p>
                    </div>
                    <div class="summary-item">
                        <h4>Development Timeline</h4>
                        <p>${analysisData.property_data.infrastructure.development_timeline}</p>
                    </div>
                    <div class="summary-item">
                        <h4>Amenity Score</h4>
                        <p>${analysisData.property_data.amenity_score.toFixed(1)}/10</p>
                    </div>
                    <div class="summary-item">
                        <h4>Professional Validation</h4>
                        <p>${analysisData.property_data.professional_validation_required ? 'Required' : 'Optional'}</p>
                    </div>
                </div>
                ${analysisData.property_data.professional_validation_required ? `
                <div class="validation-section">
                    <h4>🔧 Professional Engineering Review Required</h4>
                    <button onclick="requestProfessionalValidation()" class="validation-btn">
                        Request P.Eng Validation
                    </button>
                </div>
                ` : ''}
            </div>
        `;

        document.getElementById('analysis-panel').innerHTML = panelHtml;
    }

    exportAnalysisReport() {
        if (!this.currentProperty) return;

        const reportData = {
            property: this.currentProperty.property_data.address,
            analysis_date: new Date().toISOString(),
            infrastructure_summary: this.currentProperty.property_data.infrastructure,
            professional_summary: this.currentProperty.professional_summary
        };

        // Create downloadable report
        const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sgiach-analysis-${Date.now()}.json`;
        a.click();
    }
}

// Global function for professional validation request
async function requestProfessionalValidation() {
    try {
        const response = await fetch('/professional/validation-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                validation_type: 'comprehensive',
                property_data: window.sgiachMap.currentProperty.property_data
            })
        });

        const result = await response.json();
        alert(`Professional validation requested! Request ID: ${result.validation_request.request_id}`);
    } catch (error) {
        console.error('Validation request failed:', error);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.sgiachMap = new SgiachMapping('map');
});
