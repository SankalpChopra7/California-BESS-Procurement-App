let map, viewer, projects;
const toggleBtn = document.getElementById('toggle');
const mapDiv = document.getElementById('map');
const cesiumDiv = document.getElementById('cesiumContainer');
let showing3D = false;

async function fetchProjects() {
    const res = await fetch('/projects');
    return res.json();
}

async function fetchWeather(lat, lon) {
    const res = await fetch(`/weather?lat=${lat}&lon=${lon}`);
    return res.json();
}

function initLeaflet() {
    map = L.map('map').setView([37.5, -120], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    projects.forEach(p => {
        const m = L.marker([p.lat, p.lon]).addTo(map);
        m.on('click', async () => {
            const weather = await fetchWeather(p.lat, p.lon);
            m.bindPopup(`<b>${p.name}</b><br>${p.location}<br>Temp: ${weather.temperature}\xB0C`).openPopup();
        });
    });
}

function initCesium() {
    viewer = new Cesium.Viewer('cesiumContainer', {
        imageryProvider: new Cesium.UrlTemplateImageryProvider({
            url: 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
        }),
        baseLayerPicker: false
    });
    projects.forEach(p => {
        viewer.entities.add({
            position: Cesium.Cartesian3.fromDegrees(p.lon, p.lat),
            point: { pixelSize: 10, color: Cesium.Color.RED },
            description: `<b>${p.name}</b><br>${p.location}`
        });
    });
    viewer.zoomTo(viewer.entities);
}

async function toggle() {
    showing3D = !showing3D;
    if (showing3D) {
        mapDiv.style.display = 'none';
        cesiumDiv.style.display = 'block';
        toggleBtn.textContent = 'Switch to 2D';
        if (!viewer) initCesium();
    } else {
        cesiumDiv.style.display = 'none';
        mapDiv.style.display = 'block';
        toggleBtn.textContent = 'Switch to 3D';
    }
}

toggleBtn.addEventListener('click', toggle);

fetchProjects().then(data => {
    projects = data;
    initLeaflet();
});
