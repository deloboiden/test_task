from flask import Flask, request, send_from_directory
import os
import hashlib

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.getcwd()), 'store')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        filename_hash = hashlib.md5(filename.encode()).hexdigest()
        sub_directory = filename_hash[:2]
        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory)):
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory, filename_hash))
        return filename_hash
    else:
        return ''

@app.route('/download/<filename>')
def download_file(filename):
    sub_directory = filename[:2]
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory, filename)):
        return 'file %s does not exist' % filename
    else:
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory), filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    sub_directory = filename[:2]
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory, filename)):
        return 'file %s does not exist' % filename
    else:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory, filename))
        if not os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory)):
            os.rmdir(os.path.join(app.config['UPLOAD_FOLDER'], sub_directory))
        return 'file %s removed' % filename

if __name__ == '__main__':
    app.run()
