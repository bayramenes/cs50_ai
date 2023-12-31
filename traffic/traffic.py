import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """


    # the list of images and their corresponding labels that will be returned
    images = []
    labels = []

    # check if the data directory exists
    if os.path.isdir(data_dir) == False:
        sys.exit("Data directory does not exist")
    
    # if it does then we want to go through each of the sub-directories and load the images one by one
    for directory_index in range(NUM_CATEGORIES):
        sign_directory = os.path.join(data_dir, str(directory_index))
        # check if the sign directory exists
        if os.path.isdir(sign_directory):
            for image in os.listdir(sign_directory):
                # load the image
                image_path = os.path.join(sign_directory, image)
                image_array = cv2.imread(image_path)

                # resize the image
                image_array = cv2.resize(image_array, (IMG_WIDTH, IMG_HEIGHT))

                # add the image and label to the list
                images.append(image_array)
                labels.append(directory_index)
                
    return (images, labels)



def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """



    # create the neural network
    model  = tf.keras.Sequential([

        # first convolution layer
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # first pooling layer
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),

        # second convolution layer
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),

        # second pooling layer
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),

        
        # THIRD convolution layer
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        # THIRD pooling layer
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),

        # add input layer
        tf.keras.layers.Flatten(),


        # add a hidden layer
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.25),
        # add a second hidden layer
        tf.keras.layers.Dense(128, activation="relu"),


        # add the output layer
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")

    ])

    # compile the model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # return the model
    return model

    


if __name__ == "__main__":
    main()
