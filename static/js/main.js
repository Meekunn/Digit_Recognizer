document.addEventListener('DOMContentLoaded', function () {
	const canvas = document.getElementById('drawCanvas');
	const clearBtn = document.getElementById('clear-btn');
	const sendBtn = document.getElementById('send-btn');
	const ctx = canvas.getContext('2d');

	let isDrawing = false;

	canvas.addEventListener('mousedown', startDrawing);
	canvas.addEventListener('mousemove', draw);
	canvas.addEventListener('mouseup', stopDrawing);
	canvas.addEventListener('mouseout', stopDrawing);
	clearBtn.addEventListener('click', clearCanvas);
	sendBtn.addEventListener('click', sendImage);

	function startDrawing(e) {
		isDrawing = true;
		draw(e);
	}

	function draw(e) {
		if (!isDrawing) return;
		ctx.beginPath();
		ctx.fillStyle = 'blue';
		ctx.fillRect(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop, 5, 5);
		ctx.stroke();
		ctx.closePath();
	}

	function stopDrawing() {
		isDrawing = false;
	}

	function clearCanvas() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
	}

	function dataURLtoBlob(dataURL) {
		const parts = dataURL.split(';base64,');
		const contentType = parts[0].split(':')[1];
		const raw = window.atob(parts[1]);
		const array = new Uint8Array(new ArrayBuffer(raw.length));

		for (let i = 0; i < raw.length; i++) {
			array[i] = raw.charCodeAt(i);
		}

		return new Blob([array], { type: contentType });
	}

	function sendImage() {
		// Get the image data from the canvas
		const imageDataURL = canvas.toDataURL('image/png');

		// Convert the data URL to a Blob
		const blob = dataURLtoBlob(imageDataURL);

		// Create a FormData object
		const formData = new FormData();
		formData.append('image', blob, 'drawing.png');

		// Send the image data to the server
		fetch('/process_image', {
			method: 'POST',
			body: formData,
		})
			.then((response) => response.json())
			.then((data) => {
				console.log('Server response:', data);
			})
			.catch((error) => {
				console.error('Error sending image:', error);
			});
	}
});
