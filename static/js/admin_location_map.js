window.addEventListener("load", function () {
    const mapDiv = document.getElementById("location-map");
    if (!mapDiv) {
        return;
    }

    if (typeof L === "undefined") {
        console.log("Leaflet not loaded in admin.");
        return;
    }

    const latInput = document.getElementById("id_latitude");
    const lngInput = document.getElementById("id_longitude");
    const locateBtn = document.getElementById("btn-use-my-location");

    if (!latInput || !lngInput) {
        return;
    }

    let lat = parseFloat(latInput.value);
    let lng = parseFloat(lngInput.value);

    if (isNaN(lat) || isNaN(lng)) {
        // default center (Kathmandu area – adjust if you like)
        lat = 27.700769;
        lng = 85.300140;
    }

    const map = L.map(mapDiv).setView([lat, lng], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
    }).addTo(map);

    const marker = L.marker([lat, lng], { draggable: true }).addTo(map);

    function updateInputs(pos) {
        latInput.value = pos.lat.toFixed(6);
        lngInput.value = pos.lng.toFixed(6);
    }

    marker.on("dragend", function (e) {
        updateInputs(e.target.getLatLng());
    });

    map.on("click", function (e) {
        marker.setLatLng(e.latlng);
        updateInputs(e.latlng);
    });

    function tryUpdateMarker() {
        const newLat = parseFloat(latInput.value);
        const newLng = parseFloat(lngInput.value);
        if (!isNaN(newLat) && !isNaN(newLng)) {
            const pos = { lat: newLat, lng: newLng };
            marker.setLatLng(pos);
            map.setView(pos, map.getZoom());
        }
    }

    latInput.addEventListener("change", tryUpdateMarker);
    lngInput.addEventListener("change", tryUpdateMarker);

    // Button: use browser location
    if (locateBtn && navigator.geolocation) {
        locateBtn.addEventListener("click", function () {
            locateBtn.disabled = true;
            locateBtn.textContent = "Detecting location...";

            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    marker.setLatLng(pos);
                    map.setView(pos, 15);
                    updateInputs(pos);
                    locateBtn.textContent = "Use my current location";
                    locateBtn.disabled = false;
                },
                function (error) {
                    console.error("Geolocation error:", error);
                    alert("Unable to detect your location. Please allow location access in the browser.");
                    locateBtn.textContent = "Use my current location";
                    locateBtn.disabled = false;
                }
            );
        });
    }

    console.log("Admin location map initialized.");
});
