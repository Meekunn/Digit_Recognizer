from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

@app.route("/")
def index_page():
	# Render index Page
	return render_template("index.html")

# Endpoint to process image
@app.route('/process_image', methods=['POST'])
def process_image():

	if "image" in request.files:
		image_file = request.files["image"]
		# Upload image to server or save it
		image_file.save("test.jpg")

		# Load image with opencv
		rgb_image = cv2.imread('test.jpg')

		# Convert from RGB(3 Channels) to GrayScale(1 Channel)
		gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
		np_arr = np.array(gray_image)
		
		#Thresholding to display digit as black(0) or white(255)
		threshold_value = 10
		thresholded_image = np.where(np_arr < threshold_value, 0, 255)
		
		# Display the original and thresholded images using matplotlib
		plt.subplot(1, 2, 1)
		plt.imshow(gray_image, cmap='gray')
		plt.title('Original Image')

		plt.subplot(1, 2, 2)
		plt.imshow(thresholded_image, cmap='gray')
		plt.title('Thresholded Image')

		plt.show()

		response = {"result": "Image received and processed successfully!"}
		return jsonify(response)
	else: 
		print("No image received!")
		response = {"result": "No image received!"}
		return jsonify(response)

if __name__ == "_main_":
	app.run(debug=True)