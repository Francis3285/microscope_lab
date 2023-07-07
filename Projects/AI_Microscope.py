import cv2
import os
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from microdot import Microdot, Response
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

...


app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc(content):
    return f'''
        <html>
            <head>
                <title>AI Microscope Dashboard</title>
                <style>
                    ul {{
                        list-style-type: none;
                        margin: 0;
                        padding: 0;
                        overflow: hidden;
                        background-color: #f1f1f1;
                    }}

                    li {{
                        float: left;
                    }}

                    li a {{
                        display: block;
                        color: #000;
                        text-align: center;
                        padding: 14px 16px;
                        text-decoration: none;
                    }}

                    li a:hover {{
                        background-color: #ddd;
                    }}

                    .active {{
                        background-color: #4CAF50;
                        color: white;
                    }}
                </style>
            </head>
            <body>
                <h1>AI Microscope Dashboard</h1>
                <div>
                    <ul>
                        <li><a href="/">Help & Guide</a></li>
                        <li><a href="/microscope-connection">Microscope Connection</a></li>     
                        <li><a href="/load-data">Load Data</a></li>
                        <li><a href="/view-data">View Data</a></li>
                        <li><a href="/label-data">Label Data</a></li>
                        <li><a href="/train-model">Train Model</a></li>
                        <li><a href="/save-model">Save Model</a></li>
                        <li><a href="/load-model">Load Model</a></li>
                        <li><a href="/test-model">Test Model</a></li>
                        <li><a href="/run-model">Run Model</a></li>
                        <li><a href="/visualize">Visualize</a></li>
                    </ul>
                </div>
                <div>
                    {content}
                </div>
            </body>
        </html>
    '''
#======================================================================================================================================
@app.route('/')
def home(request):
    content = '''
        <h2>Instructions to the User / Help Features</h2>
        <p>Welcome to the AI Microscope Dashboard! This dashboard provides various features to assist you with your microscope-related tasks.</p>
        <p>Here are some instructions to help you navigate through the different features:</p>
        <h3>Connect to Real Instrument</h3>
        <p>Use this feature to establish a connection with your real microscope instrument. Make sure the instrument is properly connected to your computer.</p>        
        <h3>Load Data</h3>
        <p>Load previously saved data for viewing or further analysis. This feature allows you to load and access archived data.</p>
        <h3>View Data</h3>
        <p>Visualize and explore the loaded data. You can view images, videos, or other recorded information from your microscope.</p>
        <h3>Label Data</h3>
        <p>Assign labels or annotations to the loaded data. This helps in categorizing or marking specific features or regions of interest.</p>
        <h3>Train Model</h3>
        <p>Train a machine learning model using the labeled data. This enables the model to automatically classify or detect certain patterns or structures in the microscope images.</p>
        <h3>Save Model</h3>
        <p>Save the trained model for future use. This allows you to reuse the trained model without repeating the training process.</p>
        <h3>Load Model</h3>
        <p>Load a pre-trained model to perform classification or detection tasks on new microscope images. This feature allows you to utilize existing models.</p>
        <h3>Test Model</h3>
        <p>Evaluate the performance of the loaded or trained model on test data. This helps in assessing the accuracy and reliability of the model.</p>
        <h3>Run Model on New Images</h3>
        <p>Apply the loaded or trained model on new microscope images captured in real-time. This feature provides real-time analysis and predictions.</p>
        <h3>Visualize Model Outputs</h3>
        <p>Visualize the outputs or predictions of the model on the microscope images. This feature allows you to interpret and analyze the results.</p>
    '''
    return htmldoc(content)


#============================================================================================
# Microscope Connection
@app.post('/capture-image')
def capture_image(folder_name):
    cap = cv2.VideoCapture(0)

   # Define the directories to save frames
    desktop = os.path.expanduser("~/Desktop")  # adjust as needed
    directory1 = os.path.join(desktop, "images/train/class_1")
    directory2 = os.path.join(desktop, "images/val/class_1")


    # Create the directories if they don't exist
    os.makedirs(directory1, exist_ok=True)
    os.makedirs(directory2, exist_ok=True)

    frame_counter1 = 0
    frame_counter2 = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Draw text on the frame
        cv2.putText(frame, "Press 'c' to capture to train", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'v' to capture to val", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Webcam Feed', frame)

        key = cv2.waitKey(1)

        # If 'c' is pressed on the keyboard, save the frame in directory1
        if key & 0xFF == ord('c'):
            frame_path = os.path.join(directory1, f'frame_{frame_counter1}.png')
            cv2.imwrite(frame_path, frame)
            print(f'{frame_path} saved!')
            frame_counter1 += 1

        # If 'v' is pressed on the keyboard, save the frame in directory2
        elif key & 0xFF == ord('v'):
            frame_path = os.path.join(directory2, f'frame_{frame_counter2}.png')
            cv2.imwrite(frame_path, frame)
            print(f'{frame_path} saved!')
            frame_counter2 += 1

        # If 'q' is pressed on the keyboard, break the loop and close the application
        elif key & 0xFF == ord('q'):
            break

    # After the loop release the capture
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    return f'<h2>Image captured successfully and saved in folder: {folder_name}</h2>'


@app.route('/microscope-connection')
def microscope_connection(request):
    content = '''
        <h2>Microscope Connection</h2>
        <p>Click the button below to capture an image from the microscope and save it in a specific folder.</p>
        <form action="/capture-image" method="POST">cc
            <button type="submit" name="folder" value="Folder 1">Save in Folder 1</button>
            <button type="submit" name="folder" value="Folder 2">Save in Folder 2</button>
        </form>
    '''
    return htmldoc(content)


#======================================================================================================================================
@app.route('/load-data')
def load_data(request):
    directory = '/home/mpcr/Desktop/images/train/class_1'
    image_size = (224, 224)  # adjust this to the size of your images
    global data
    data = []

    for filename in os.listdir(directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # check for other image formats as needed
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # read in grayscale, use cv2.IMREAD_COLOR for color images
            if img is not None:
                img = cv2.resize(img, image_size)
                img_flattened = img.reshape(-1)
                data.append(img_flattened)

    return htmldoc(f'<h1>Successfully loaded {len(data)} images</h1>')



#======================================================================================================================================
def savefig_b64():
    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    im_b64 = base64.b64encode(buf.getvalue())
    imdata = f'data:image/png;base64,{im_b64.decode("utf-8")}'
    return imdata


#======================================================================================================================================
@app.route('/view-data')
def view_data(request):
 
    num_images = len(data)
    num_cols = 4
    num_rows = (num_images + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
    axes = axes.flatten()

    for i, img_flattened in enumerate(data):
        img = img_flattened.reshape(224, 224)
        axes[i].imshow(img, cmap='gray')
        axes[i].axis('off')

    for j in range(num_images, num_cols * num_rows):
        axes[j].axis('off')

    plt.tight_layout()
    imdata = savefig_b64()
    plt.close()  # Close the figure to free up resources

    return htmldoc(f'<image src={imdata} />')


#======================================================================================================================================

@app.route('/label-data')
def label_data(request):
    num_images = len(data)
    num_cols = 4
    num_rows = (num_images + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
    axes = axes.flatten()

    labels = []
    for i, img_flattened in enumerate(data):
        img = img_flattened.reshape(224, 224)
        axes[i].imshow(img, cmap='gray')
        axes[i].axis('off')

        # Assuming labeling is done manually, let's generate some random labels for demo purposes
        label = i % 2  # alternate between labels 0 and 1
        labels.append(label)
        axes[i].set_title(f'Label: {label}')  # Display the label on the plot

    for j in range(num_images, num_cols * num_rows):
        axes[j].axis('off')

    plt.tight_layout()
    imdata = savefig_b64()
    plt.close()  # Close the figure to free up resources

    # Save the labels to a DataFrame (you could also save this to a file)
    global df
    df = pd.DataFrame({
        'image': [img.tolist() for img in data],  # Store the flattened images
        'label': labels  # Store the labels
    })

    return htmldoc(f'<h2>Successfully labeled {len(data)} images</h2><image src={imdata} />')


#======================================================================================================================================

# # Train Model
# @app.route('/train-model')
# def train_model(request):
#     global model
#     model = Sequential()

#     # Configure the parameters of the model according to your needs
#     model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(224,224,1)))
#     model.add(Conv2D(32, kernel_size=3, activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2,2)))
#     model.add(Flatten())
#     model.add(Dense(2, activation='softmax'))  # assuming binary classification; for multi-class classification, increase this number

#     model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#     # Transform the data and labels into a format suitable for training
#     X = np.array(df['image'].to_list()).reshape(-1, 224, 224, 1)  # reshape into format (num_images, height, width, num_channels)
#     y = df['label'].values

#     # Split the data into training and validation sets
#     X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)  # adjust the test_size and random_state as needed

#     # Normalize the images
#     X_train = X_train / 255
#     X_val = X_val / 255

#     # Augment the images
#     datagen = ImageDataGenerator(
#         featurewise_center=True,
#         featurewise_std_normalization=True,
#         rotation_range=20,
#         width_shift_range=0.2,
#         height_shift_range=0.2,
#         horizontal_flip=True)

#     # Compute quantities required for featurewise normalization
#     # (std, mean, and principal components if ZCA whitening is applied).
#     datagen.fit(X_train)

#     # Train the model
#     history = model.fit(datagen.flow(X_train, y_train, batch_size=32), validation_data=(X_val, y_val), epochs=5)  # adjust the batch_size and epochs as needed

#     # Show the training history
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
#     ax1.plot(history.history['loss'], color='b', label="Training loss")
#     ax1.plot(history.history['val_loss'], color='r', label="validation loss")
#     ax1.set_xticks(np.arange(1, 5, 1))
#     ax1.set_yticks(np.arange(0, 1, 0.1))
#     ax2.plot(history.history['accuracy'], color='b', label="Training accuracy")
#     ax2.plot(history.history['val_accuracy'], color='r',label="Validation accuracy")
#     ax2.set_xticks(np.arange(1, 5, 1))
#     legend = plt.legend(loc='best', shadow=True)
#     plt.tight_layout()
#     imdata = savefig_b64()
#     plt.close()  # Close the figure to free up resources

#     return htmldoc(f'<h2>Successfully trained the model</h2><image src={imdata} />')

#======================================================================================================================================


# Add routes for other tabs similarly

if __name__ == '__main__':
    app.run(debug=True, port=8008)
