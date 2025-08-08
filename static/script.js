document.addEventListener("DOMContentLoaded", () => {
    const teamSelect = document.getElementById("teamSelect");
    const timeSlider = document.getElementById("timeSlider");
    const timeValue = document.getElementById("timeValue");
    const canvas = document.getElementById("pointsCanvas");
    const ctx = canvas.getContext("2d");

    const mapImageSize = 512;
    const MAP_MIN_X = 0;
    const MAP_MAX_X = 15000;
    const MAP_MIN_Y = 0;
    const MAP_MAX_Y = 15000;

    // Slider en secondes (0 → 30 min) avec pas de 15 sec
    timeSlider.min = 0;
    timeSlider.max = 30 * 60;
    timeSlider.step = 15;
    timeSlider.value = 0;

    function convertCoords(gameX, gameY) {
        const px = ((gameX - MAP_MIN_X) / (MAP_MAX_X - MAP_MIN_X)) * mapImageSize;
        const py = mapImageSize - ((gameY - MAP_MIN_Y) / (MAP_MAX_Y - MAP_MIN_Y)) * mapImageSize;
        return { px, py };
    }

    async function loadPoints() {
        const team = teamSelect.value;
        const timeSec = parseInt(timeSlider.value);
        const minutes = Math.floor(timeSec / 60);
        const seconds = timeSec % 60;
        timeValue.textContent = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

        const res = await fetch(`/positions/${team}/${timeSec}`);
        const points = await res.json();

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        points.forEach(p => {
            // Bleu ou rouge selon side
            ctx.fillStyle = (p.side === "blue") 
                ? "rgba(0, 0, 255, 0.7)" 
                : "rgba(255, 0, 0, 0.7)";

            const { px, py } = convertCoords(p.x, p.y);
            ctx.beginPath();
            ctx.arc(px, py, 8, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    teamSelect.addEventListener("change", loadPoints);
    timeSlider.addEventListener("input", loadPoints);

    loadPoints();
});
