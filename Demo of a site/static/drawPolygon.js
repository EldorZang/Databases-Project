// List of polygon coordinates (example)
const geometries = [
    { x: 35.719918, y: 32.709192 },
    { x: 35.545665, y: 32.393992 },
    { x: 35.18393, y: 32.532511 },
    { x: 34.974641, y: 31.866582 },
    { x: 35.225892, y: 31.754341 },
    { x: 34.970507, y: 31.616778 },
    { x: 34.927408, y: 31.353435 },
    { x: 35.397561, y: 31.489086 },
    { x: 35.420918, y: 31.100066 },
    { x: 34.922603, y: 29.501326 },
    { x: 34.265433, y: 31.219361 },
    { x: 34.556372, y: 31.548824 },
    { x: 34.488107, y: 31.605539 },
    { x: 34.752587, y: 32.072926 },
    { x: 34.955417, y: 32.827376 },
    { x: 35.098457, y: 33.080539 },
    { x: 35.126053, y: 33.0909 },
    { x: 35.460709, y: 33.08904 },
    { x: 35.552797, y: 33.264275 },
    { x: 35.821101, y: 33.277426 },
    { x: 35.836397, y: 32.868123 },
    { x: 35.700798, y: 32.716014 },
    { x: 35.719918, y: 32.709192 }
];

// Function to draw a single polygon
function drawPolygon(ctx, coordinates, offsetX, offsetY, scaleFactor) {
    ctx.beginPath();
    ctx.moveTo((coordinates[0].x - offsetX) * scaleFactor, (coordinates[0].y - offsetY) * scaleFactor);

    for (let i = 1; i < coordinates.length; i++) {
        ctx.lineTo((coordinates[i].x - offsetX) * scaleFactor, (coordinates[i].y - offsetY) * scaleFactor);
    }

    ctx.closePath();
    ctx.stroke();
}

// Function to normalize and draw polygons or multipolygons based on canvas size
function drawNormalizedGeometries(canvas, geometries) {
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Find the bounding box around all polygons
    let minX = Number.MAX_VALUE;
    let minY = Number.MAX_VALUE;
    let maxX = Number.MIN_VALUE;
    let maxY = Number.MIN_VALUE;

    geometries.forEach(geometry => {
        geometry.forEach(coordinates => {
            coordinates.forEach(coord => {
                minX = Math.min(minX, coord.x);
                minY = Math.min(minY, coord.y);
                maxX = Math.max(maxX, coord.x);
                maxY = Math.max(maxY, coord.y);
            });
        });
    });

    // Calculate the width and height of the bounding box
    const width = maxX - minX;
    const height = maxY - minY;

    // Calculate the scaling factors for x and y coordinates
    const scaleX = canvas.width / width;
    const scaleY = canvas.height / height;

    // Choose the smaller scaling factor to ensure the geometries fit within the canvas
    const scaleFactor = Math.min(scaleX, scaleY);

    // Calculate the offset to center the geometries in the canvas
    const offsetX = minX;
    const offsetY = minY;

    geometries.forEach(geometry => {
        if (geometry.length === 1) {
            // Single polygon
            drawPolygon(ctx, geometry[0], offsetX, offsetY, scaleFactor);
        } else {
            // Multi-polygon
            geometry.forEach(polygon => {
                drawPolygon(ctx, polygon, offsetX, offsetY, scaleFactor);
            });
        }
    });
}



// Get the canvas element
const canvas = document.getElementById('polygonCanvas');

// Call drawNormalizedGeometries function with the canvas and list of geometries
drawNormalizedGeometries(canvas, geometries);


