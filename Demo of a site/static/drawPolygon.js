// List of polygon coordinates (example)
const polygonCoordinates = [
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

// Function to normalize and draw the polygon based on canvas size
function drawNormalizedPolygon(canvas, coordinates) {
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Find the maximum and minimum x and y coordinates of the polygon
    let maxX = coordinates[0].x;
    let maxY = coordinates[0].y;
    let minX = coordinates[0].x;
    let minY = coordinates[0].y;

    for (let i = 1; i < coordinates.length; i++) {
        maxX = Math.max(maxX, coordinates[i].x);
        maxY = Math.max(maxY, coordinates[i].y);
        minX = Math.min(minX, coordinates[i].x);
        minY = Math.min(minY, coordinates[i].y);
    }

    // Calculate the width and height of the bounding box around the polygon
    const width = maxX - minX;
    const height = maxY - minY;

    // Calculate the scaling factors for x and y coordinates
    const scaleX = canvas.width / width;
    const scaleY = canvas.height / height;

    // Choose the smaller scaling factor to ensure the polygon fits within the canvas
    const scaleFactor = Math.min(scaleX, scaleY);

    // Calculate the offset to center the polygon in the canvas
    const offsetX = (canvas.width - width * scaleFactor) / 2;
    const offsetY = (canvas.height - height * scaleFactor) / 2;

    ctx.beginPath();
    ctx.moveTo((coordinates[0].x - minX) * scaleFactor + offsetX, (coordinates[0].y - minY) * scaleFactor + offsetY);

    for (let i = 1; i < coordinates.length; i++) {
        ctx.lineTo((coordinates[i].x - minX) * scaleFactor + offsetX, (coordinates[i].y - minY) * scaleFactor + offsetY);
    }

    ctx.closePath();
    ctx.stroke();
}


// Get the canvas element
const canvas = document.getElementById('polygonCanvas');

// Call drawNormalizedPolygon function with the canvas and list of coordinates
drawNormalizedPolygon(canvas, polygonCoordinates);


