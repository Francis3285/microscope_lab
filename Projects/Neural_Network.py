#Required Libraries
import ipywidgets as widgets
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
from skimage.util import montage
from PIL import Image

# Declare a variable to keep track of whether the histogram has been generated or not
histogram_generated = False

# Declare a variable to store the loaded dataset
dataset = None
images = None
labels = None

# Function to load dataset
def load_dataset(b):
    global dataset, images, labels

    path = ('/content/drive/MyDrive/Datasets /train_images.npy')
    data = np.load(path)

    # Preview a single image from the dataset
    image = data[0]  # Get the first image
    plt.imshow(image, cmap='gray')
    plt.title("Single Image")
    plt.axis('off')
    plt.show()

    # Create a montage of images from the dataset with labels
    num_images = data.shape[0]  # Number of images in the dataset
    images = data
    labels = np.arange(num_images)

    fig, axes = plt.subplots(5, 5, figsize=(8, 8))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(images[i], cmap='gray')
        ax.set_title(f"Label: {labels[i]}")
        ax.axis('off')
    plt.suptitle("Montage of Images with Labels")
    plt.tight_layout()
    plt.show()

    dataset = list(zip(images, labels))  # Create dataset as a list of tuples


# Function to generate histogram
def generate_histogram(b):
    global histogram_generated

    if not histogram_generated:
        if labels is not None:
            # Convert labels to a NumPy array
            labels_array = np.array(labels)

            # Generate histogram
            plt.figure(figsize=(10, 6))
            plt.hist(labels_array, bins=10, edgecolor='black')
            plt.xlabel('Label')
            plt.ylabel('Frequency')
            plt.title('Histogram of MNIST Dataset')
            plt.show()

            histogram_generated = True
        else:
            print("Please load the dataset first.")
    else:
        print("Histogram has already been generated. Click 'Generate Histogram' only once.")


# Function to view RGB channels
def view_rgb_channels(d):
    global dataset

    if dataset is not None:
        # Get a random image from the dataset
        image, _ = dataset[np.random.randint(len(dataset))]

        # Check if the image is grayscale or RGB
        if image.shape[0] == 1:
            # Grayscale image, duplicate the channel for RGB visualization
            image = np.repeat(image, 3, axis=0)
        else:
            # Scale RGB image pixel values to [0, 1]
            image = image / 255.0

        # Split the image into RGB channels
        red_channel = image[0]
        green_channel = image[1]
        blue_channel = image[2]

        # Plot the RGB channels separately
        fig, axes = plt.subplots(1, 4, figsize=(16, 4))

        # Display the original image
        axes[0].imshow(image.reshape(28, 28, 3))
        axes[0].set_title('Original Image')
        axes[0].axis('off')

        # Display the RGB channels
        axes[1].imshow(red_channel, cmap='gray')
        axes[1].set_title('Red Channel')
        axes[1].axis('off')
        axes[2].imshow(green_channel, cmap='gray')
        axes[2].set_title('Green Channel')
        axes[2].axis('off')
        axes[3].imshow(blue_channel, cmap='gray')
        axes[3].set_title('Blue Channel')
        axes[3].axis('off')

        plt.tight_layout()
        plt.show()
    else:
        print("Please load the dataset first.")




# Function to train neural network
def train_neural_network(e):
    # Your code to train neural network here
    pass

# Function to save model
def save_model(f):
    # Your code to save the model here
    pass

# Function to load model
def load_model(g):
    # Your code to load the model here
    pass

# Function to test neural network
def test_neural_network(h):
    # Your code to test neural network here
    pass

# Function for expert system-style Q&A
def expert_system_qa(i):
    # Your code for expert system-style Q&A here
    pass

# Create buttons for each functionality
load_dataset_button = widgets.Button(description="Load Dataset")
generate_histogram_button = widgets.Button(description="Generate Histogram")
view_rgb_channels_button = widgets.Button(description="View RGB Channels")
train_neural_network_button = widgets.Button(description="Train Neural Network")
save_model_button = widgets.Button(description="Save Model")
load_model_button = widgets.Button(description="Load Model")
test_neural_network_button = widgets.Button(description="Test Neural Network")
expert_system_qa_button = widgets.Button(description="Expert System Q&A")

# Set button click event handlers
load_dataset_button.on_click(load_dataset)
generate_histogram_button.on_click(lambda x: generate_histogram(dataset))
view_rgb_channels_button.on_click(view_rgb_channels)
train_neural_network_button.on_click(train_neural_network)
save_model_button.on_click(save_model)
load_model_button.on_click(load_model)
test_neural_network_button.on_click(test_neural_network)
expert_system_qa_button.on_click(expert_system_qa)

# Create tabs for each functionality
tab_contents = [
    widgets.VBox([load_dataset_button]),
    widgets.VBox([generate_histogram_button]),
    widgets.VBox([view_rgb_channels_button]),
    widgets.VBox([train_neural_network_button]),
    widgets.VBox([save_model_button]),
    widgets.VBox([load_model_button]),
    widgets.VBox([test_neural_network_button]),
    widgets.VBox([expert_system_qa_button])
]
tab_titles = ['Load Dataset', 'Generate Histogram', 'View RGB Channels', 'Train Neural Network', 'Save Model',
              'Load Model', 'Test Neural Network', 'Expert System Q&A']

# Create the tabs
tabs = widgets.Tab()
tabs.children = tab_contents

# Set tab titles
for i in range(len(tabs.children)):
    tabs.set_title(i, tab_titles[i])

# Display the tabs
display(tabs)
