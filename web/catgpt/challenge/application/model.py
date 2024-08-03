import tensorflow as tf
from flask import current_app as app
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
import numpy as np
import os
import logging

def predict_image(image_path: str):

    try:

        model = tf.keras.models.load_model(os.path.join(app.config.get("MODEL_DIR"), 'base_model.h5'))
    
        img = load_img(image_path, target_size=(150, 150))

        img_array = img_to_array(img)
        
        img_array = np.expand_dims(img_array, axis=0)
        
        img_array /= 255.0
        
        prediction = model.predict(img_array,verbose=0)
        
        if prediction[0] > 0.5:
           P = "Dog"
        else:
            P = "Cat"

        return {"class":P,
                "cat":round(100-prediction[0][0]*100),
                "dog":round(prediction[0][0]*100)}
        
    except Exception as e:
        logging.error(e)
        return {"error":"An error occurred while classifying your image."}

def validate_model(model_path):

    try:

        model = tf.keras.models.load_model(model_path,safe_mode=False)

        validation_dir = os.path.join(app.config.get("MODEL_DIR"), 'cats_and_dogs_filtered/validation')

        IMG_SIZE = (150, 150)
        BATCH_SIZE = 32

        validation_datagen = ImageDataGenerator(rescale=1./255)

        validation_generator = validation_datagen.flow_from_directory(
            validation_dir,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='binary'
        )

        validation_loss, validation_accuracy = model.evaluate(validation_generator, steps=validation_generator.n // BATCH_SIZE,verbose=0)

        return {"accuracy":round(validation_accuracy*100)}
    
    except Exception as e:
        logging.error(e)
        return {"error":"An error occurred while validating your model."}

