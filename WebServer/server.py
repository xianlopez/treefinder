import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import sys

sys.path.insert(0, '/home/xian/brainlab')
from net_config import PredictConfiguration
import BrainLabNet
import tools

args = PredictConfiguration()
net = BrainLabNet.BrainLabNet(args, 'interactive')
net.start_interactive_session(args)

basedir = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_tree_name(img_path):
    input_batch = net.reader.get_batch([img_path])
    predictions = net.forward_batch(input_batch, args)
    winner = np.argmax(predictions)
    classname = net.classnames[winner]
    return classname

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    error = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            error = 'No file selected'
            return render_template('form.html', error=error)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = 'No file selected'
            return render_template('form.html', error=error)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_save)
            answer = get_tree_name(path_save)
            return render_template('answer.html', nome_arbore=answer)
    else:
	    return render_template('form.html', error=error)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)






