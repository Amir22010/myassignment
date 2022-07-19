import tensorflow as tf
from layers import L1Dist
import numpy as np
import os
import shutil

# Build app and layout 
class Model():

    def __init__(self):

        # Load tensorflow/keras model
        print("[INFO] loading siamese model...")
        self.model = tf.keras.models.load_model(os.path.join('siamese_model', 'siamesemodel.h5'), custom_objects={'L1Dist':L1Dist})

    # Load image from file and convert to 100x100px
    def preprocess(self, file_path):
        # Read in image from file path
        byte_img = tf.io.read_file(file_path)
        # Load in the image 
        img = tf.io.decode_jpeg(byte_img)
        # Preprocessing steps - resizing the image to be 100x100x3
        img = tf.image.resize(img, (100,100))
        # Scale image to be between 0 and 1 
        img = img / 255.0
        
        # Return image
        return img

    # Verification function to verify person
    def verify(self):
        # Specify thresholds
        detection_threshold = 0.4
        #verification_threshold = 0.7
        # Get final accuracy results in dictionary
        final_result = {}
        # read all registered users directory
        for dir in os.listdir(os.path.join('application_data', 'verification_images')):
            results = []
            # read all registered users images from specific user directory
            for image in os.listdir(os.path.join('application_data', 'verification_images', dir)):
                # pre process input image
                input_img = self.preprocess(os.path.join('application_data', 'input_image', 'input_image.jpg'))
                # pre process verification images
                validation_img = self.preprocess(os.path.join('application_data', 'verification_images', dir, image))
                # Make Predictions 
                result = self.model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
                # append all similarity results
                results.append(result)
            # Detection Threshold: Metric above which a prediciton is considered positive 
            detection = np.sum(np.array(results) > detection_threshold)
            print(detection)
            print(len(os.listdir(os.path.join('application_data', 'verification_images',dir))))
            # Verification Threshold: Proportion of positive predictions / total positive samples 
            verification = detection / len(os.listdir(os.path.join('application_data', 'verification_images',dir)))
            print("=====================================")
            final_result[dir]=verification
            print(final_result)
            #verified = verification > verification_threshold
            # delete all directories after authentication
            shutil.rmtree(os.path.join('application_data', 'verification_images', dir))
        return final_result