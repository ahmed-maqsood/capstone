#!/usr/bin/python3
from tensorflow.keras.models import model_from_json
from pathlib import Path
import numpy as np
import cv2
import time
from datetime import datetime
import pandas as pd
#import serial
#import os


def read_image(file_path):
    #read image
    img = cv2.imread(file_path)
    #rotate image
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    #apply greyscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #crop image to 224, 224
    img = img[35:259, 128:352]
    #add censor bars
    img = cv2.line(img, (165, 45-45), (115, 95-45), (0, 0, 0), 10)
    img = cv2.line(img, (45, 45-45), (95, 95-45), (0, 0, 0), 10)
    img = cv2.line(img, (45, 45-45), (165, 45-45), (0, 0, 0), 10)
    img = cv2.line(img, (55, 55-45), (155, 55-45), (0, 0, 0), 10)
    img = cv2.line(img, (65, 65-45), (145, 65-45), (0, 0, 0), 10)
    img = cv2.line(img, (75, 75-45), (135, 75-45), (0, 0, 0), 10)
    img = cv2.line(img, (85, 85-45), (125, 85-45), (0, 0, 0), 10)
    img = cv2.line(img, (95, 95-45), (115, 95-45), (0, 0, 0), 10)
    #normalize pixel colour valus to 0-1
    img = img/255
    #expand pixel dimensions from (224,224,1) to (224,224,3) essentially faking RGB color channels
    img = np.expand_dims(img, axis=-1)
    img = np.repeat(img, 3, axis=2)
    #output image
    return img

def predict_with_CNN(img, model):
    print('getting ready to predict')
    # basically put image into an array so u can predict it
    list_of_images = np.expand_dims(img, axis=0)

    # Make a prediction using our created model
    results = model.predict(list_of_images)

    class_number = np.argmax(results[0])
    likelihood = np.max(results[0])

    class_names = {
        0: "normal",
        1: "under_extruded",
        2: "over_extruded",
        3: "no_pattern"

    }
    class_name = class_names[class_number]

    # Print the result
    print(f"Predicted Class: {class_name}")
    print(f"Likelihood: {likelihood * 100}%")

    return (class_number, class_name, likelihood*100)

def load_model():
    # Load the model's structure in the .json file
    file_path = Path("model_mobilenet_1.00_224_structure.json")
    model_structure = file_path.read_text()
    model = model_from_json(model_structure)

    # Load the weight's file from the .h5 file
    model.load_weights("model_mobilenet_1.00_224_weights.h5")

    return model

def searching_for_new_file(full_dir):
    break_loop = False
    while(break_loop == False):
        time.sleep(3)
        print('searching...')
        if full_dir.exists():
            break_loop = True
            print('file found')

def img_delete(full_dir):
    full_dir.unlink()
    print('snapshot deleted')

def log(log_name, img_num, class_name, class_number, likelihood, flowrate):
    array = {'file':[img_num], 'class':[class_name], 'class#':[class_number], '%':[likelihood], 'flow':[flowrate]}
    df = pd.DataFrame(array)

    with open(log_name, 'a') as log:
        df.to_csv(log, index=False, header=False, line_terminator='\n')

    print("log updated")

def command(ser, command):
    start_time = datetime.now()
    ser.write(str.encode(command))
    time.sleep(1)

def printer_stuff(flowrate, max_flowrate, min_flowrate, class_number, likelihood):
    #under extrution stuff
    if class_number == 1:
        print('Under-extrusion detected')
        if flowrate == max_flowrate:
            print('flowrate reaching maximum value')
        elif likelihood >= 90 and flowrate <= max_flowrate:
            flowrate = flowrate + 10
        else:
            flowrate = flowrate + 5
        # ser = serial.Serial('/dev/ttyUSB0', 115200)
        # command(ser, f"M221 S{flowrate}\r\n")
        # ser.close()
        print("Adjusted flowrate to: " + str(flowrate) + r"%")

    #over extrusion stuff
    elif class_number == 2:
        print('Over-extrusion detected')
        if flowrate == min_flowrate:
            print('flowrate reaching minimum value')
        elif likelihood >= 90 and flowrate >= min_flowrate:
            flowrate = flowrate - 10
        else:
            flowrate = flowrate - 5
            # ser = serial.Serial('/dev/ttyUSB0', 115200)
        # command(ser, f"M221 S{flowrate}\r\n")
        # ser.close()
        print("Adjusted flowrate to: " + str(flowrate) + r"%")

    #normal extrusion stuff
    elif class_number == 0:
        print('Normal')

    #no pattern stuff
    else:
        print('No pattern')

    #return the new flowrate
    return flowrate

def main():
    #loads CNN model
    model = load_model()

    #set directory, log file, etc. name here
    directory = r"C:\Users\ahmed\Desktop\Capstone"
    original_name = 'snapshot'
    full_dir = Path(directory + '\\' + original_name + '.png')
    log_name = 'test.csv'

    #flowrate stuff
    flowrate = 100  # default as 100
    max_flowrate = 160
    min_flowrate = 50

    img_num = 0

    while(True):
        #fine a new snapshot.png
        searching_for_new_file(full_dir)
        time.sleep(0.5)
        #read snapshot.png and process it for prediction
        img = read_image(str(full_dir))
        #predict image using CNN
        class_number, class_name, likelihood = predict_with_CNN(img, model)
        #delete snapshot.png to make room for a new one to apear
        img_delete(full_dir)
        #log data into csv file
        log(log_name, img_num, class_name, class_number, likelihood, flowrate)
        #update img_num to keep track of snapshot#
        img_num = img_num + 1

        #adjust flowrate
        flowrate = printer_stuff(flowrate, max_flowrate, min_flowrate, class_number, likelihood)


if __name__ == "__main__":
    main()