import os
import json
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, Response
from werkzeug.utils import secure_filename, send_from_directory
import gc_homeland_v9
from gc_homeland_v9 import read_preprocessing, ocr_phase
# from flask_ngrok import run_with_ngrok

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['pdf','PDF'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_for_pdf(filename_for_pdf):
  get_pre_img = read_preprocessing(filename_for_pdf)
  get_OCR_json = ocr_phase(get_pre_img)

  # dict_sampe = {
  #   "file_output": filename_for_pdf,
  # }
  
  return get_OCR_json

# Bagian GET
@app.route('/', methods=['GET'])
def ocr_index():
  return render_template('ocr.html')


@app.route('/api/filepdf', methods=['POST'])
def upload_file():
      print("proses sedang di upload")
      # check if the post request has the file part
      try:
        print(request.files)
        print("request satu lancar")
      except Exception as e:
        print(e)

      # return "Gagal"
      
      if 'file' not in request.files:
          # flash('No file part')
          return "request 2 No file part"
          # print("sampai if 1 aman")
      file = request.files['file']

      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
          return "Filename salah" 
          # print('sampai sini aman')
          # print("sampai if 2 aman")
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          file.save(file_path)
        
          do_ocr_things = ocr_for_pdf(file_path)

          print("Request ke 3 aman")
          respon = str(do_ocr_things)
          res = Response(respon, mimetype='application/json')
          res.headers["Content-Disposition"] = "attachment;filename=hehe.json"
          return res

      return "Request ocr lancar"




app.run()