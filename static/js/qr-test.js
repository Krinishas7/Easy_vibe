document.addEventListener("DOMContentLoaded", async () => {
    const readerDiv = document.getElementById("reader");
    const startBtn = document.getElementById("startBtn");
    const debugDiv = document.getElementById("debugLog");

    function log(msg) {
        const time = new Date().toLocaleTimeString();
        debugDiv.innerHTML += `<br>[${time}] ${msg}`;
        debugDiv.scrollTop = debugDiv.scrollHeight;
        console.log(msg);
    }

    if (!startBtn) return;

    let html5QrCode = new Html5Qrcode("reader");

    startBtn.onclick = async () => {
        try {
            log("Trying to get cameras...");
            const devices = await Html5Qrcode.getCameras();
            if (!devices || devices.length === 0) throw new Error("No camera found");
            const cameraId = devices[0].id;
            log(`Using camera: ${devices[0].label}`);

            await html5QrCode.start(
                cameraId,
                { fps: 10, qrbox: 250 },
                qrMessage => {
                    log("QR Scanned: " + qrMessage);
                    alert("QR Code: " + qrMessage);
                },
                err => log("Scan error: " + err)
            );
        } catch (err) {
            log("Error: " + err.message);
        }
    };
});
