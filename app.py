from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.transform import resize
from keras.models import load_model
from keras.models import model_from_json

app = Flask(__name__)

def models():
	# Model reconstruction from JSON file
	with open('model_architecture.json', 'r') as f:
			model = model_from_json(f.read())

	# Load weights into the new model
	model.load_weights('model_weights.h5')

	return model

new_model = models()

# Now you can use the new_model for predictions or further training

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

		resized_image = resize(thresholded_image, (28, 28))
		model_input = resized_image.reshape((1, 28*28)).astype('float32')

		model_input = model_input / 255.0

		prediction = new_model.predict(model_input)

		print(prediction)

		# Assuming prediction is a one-hot encoded output, you might want to get the predicted class
		predicted_class = np.argmax(prediction)

		print(predicted_class)

		
		# Display the original and thresholded images using matplotlib
		plt.subplot(1, 2, 1)
		plt.imshow(gray_image, cmap='gray')
		plt.title('Original Image')

		plt.subplot(1, 2, 2)
		plt.imshow(resized_image, cmap='gray')
		plt.title('Thresholded Image')

		plt.show()

		response = {"result": "Image received and processed successfully!", "prediction": [2,4,5]}
		return jsonify(response)
	else: 
		print("No image received!")
		response = {"result": "No image received!"}
		return jsonify(response)

if __name__ == "_main_":
	app.run(debug=True)