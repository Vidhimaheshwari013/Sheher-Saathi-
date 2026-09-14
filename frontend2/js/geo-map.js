const DELHI_CENTER = [28.6139, 77.2090];
const DELHI_VIEWBOX = "76.80,28.90,77.40,28.40";

const geocodeCache = JSON.parse(localStorage.getItem("delhiGeocodeCache") || "{}");

function saveGeocodeCache() {
    localStorage.setItem("delhiGeocodeCache", JSON.stringify(geocodeCache));
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function geocodeLocation(locationText) {
    if (!locationText) return null;
    const key = locationText.trim().toLowerCase();
    if (geocodeCache[key]) return geocodeCache[key];

    const query = encodeURIComponent(`${locationText}, Delhi, India`);
    const url = `https://nominatim.openstreetmap.org/search?q=${query}&format=json&limit=1&countrycodes=in&viewbox=${DELHI_VIEWBOX}&bounded=1`;

    try {
        const response = await fetch(url);
        const results = await response.json();
        if (results.length > 0) {
            const coords = [parseFloat(results[0].lat), parseFloat(results[0].lon)];
            geocodeCache[key] = coords;
            saveGeocodeCache();
            return coords;
        }
    } catch (error) {
        console.error("Geocoding failed for:", locationText, error);
    }
    return null;
}

const PRIORITY_COLOR = { high: "#dc2626", medium: "#f59e0b", low: "#6b7280" };

async function renderClustersOnMap(mapInstance, clusters, maxMarkers = 20) {
    mapInstance.eachLayer(layer => {
        if (layer instanceof L.CircleMarker) mapInstance.removeLayer(layer);
    });

    for (const cluster of clusters.slice(0, maxMarkers)) {
        let coords = null;
        for (const loc of cluster.locations) {
            coords = await geocodeLocation(loc);
            if (coords) break;
            await sleep(1100);
        }
        if (!coords) {
            coords = [
                DELHI_CENTER[0] + (Math.random() - 0.5) * 0.1,
                DELHI_CENTER[1] + (Math.random() - 0.5) * 0.1,
            ];
        }

        const color = PRIORITY_COLOR[cluster.priority.level] || "#6b7280";
        const categoryLabel = (cluster.category || "Issue").replace(/_/g, " ");

        L.circleMarker(coords, {
            radius: 8 + Math.min(cluster.size, 10),
            fillColor: color, color: color, fillOpacity: 0.6, weight: 2,
        })
        .bindPopup(`<strong>${categoryLabel}</strong><br>${cluster.size} reports · Priority: ${cluster.priority.level}<br>${cluster.locations[0] || ""}`)
        .addTo(mapInstance);

        await sleep(1100);
    }
}