import numpy as np
import solver
import utils
import cv2

def detect(img):
    ### Detects black blobs on image, sets a ROI and prepares it for the model to predict ###

    thresh = utils.preproc(img)
    cnts = utils.findContours(thresh)


    chars = {}
    for c in cnts:

        # Make sure it's an actual character by setting a minimal area size
        if cv2.contourArea(c) > 75:

            # Extract ROI and starting position on x axis
            roi,x = utils.extractChar(thresh,c,position=True)
            chars[x] = utils.scaleAndPad(roi)
    
    return chars

def recognize(model,chars):
    ### Goes trough each detected char and makes a prediction ###

    # Sorts detected characters by their starting position on X axis
    # In other words, sorts them left to right
    sorted_keys = sorted(chars)
    predictions = []

    for key in sorted_keys:

        char = chars[key]
        # Model expects a batch of images, (batch_size, img_width, img_height, img_channels)
        # Since this is a single image, batch_size = 1, it's square so img_width = img_height and it's B&W so img_channels = 1)
        char = char.reshape(1,utils.IMG_SIZE,utils.IMG_SIZE,1)
        # Get the most probable prediction from the model
        prediction = model.predict(char)
        class_no = np.argmax(prediction)
        # Check for probability. If it isn't high enough, discard the prediction
        probability = prediction[:,class_no][0]
        if probability < utils.PROB_TH:
            continue
        # Decode the prediction into class name
        char = utils.CLASS_NAMES[class_no]
        predictions.append(char)
    
    return predictions

def solve(predictions):
    # Returns each step; from a list of detected chars to an eventual solution

    output = {}

    eq = solver.predictionsToEquation(predictions)
    output["equation"] = "Equation:" + solver.preparePrint(eq)

    eq_unary = solver.unaryMinuses(eq)
    output["unary"] = "Chunked Equation:" + str(eq_unary)

    postfix = solver.shuntingYard(eq_unary)
    output["postfix"] = "Postfix:" + str(postfix)

    solution = solver.solvePostfix(postfix)
    output["solution"] = "Solution:" + solver.preparePrint(solution)

    return output
