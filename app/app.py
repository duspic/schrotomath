from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import backend
import utils
import cv2


# Load model
model = tf.keras.models.load_model(utils.MODEL_PATH)

# Instantiate Flask app 
app = Flask(__name__, template_folder='templates')



@app.route('/', methods = ['GET','POST'])
def index():
    global status,equation,unary,postfix,solution
    
    if request.method == 'POST':
        response = request.files.get('img')

        try:
            equation = cv2.imdecode(np.frombuffer(response.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            equation = utils.crop(equation)
            status = "Status: Got image."
        except:
            status = "Status: Couldn't get image. "
            output = backend.solve('')
            output['status'] = status
            return jsonify(output)
            
        
        
        chars = backend.detect(equation)
        predictions = backend.recognize(model,chars)
        output = backend.solve(predictions)
        output['status'] = status
        return jsonify(output)

    return render_template('index.html')


if __name__ == '__main__':
    from os import environ
    app.run(debug = False, host = '0.0.0.0', port=environ.get("PORT", 5000))