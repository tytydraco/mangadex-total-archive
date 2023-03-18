from flask import Flask, render_template, request, send_file
import os
import subprocess

DOWNLOADS_DIR='downloads'

if not os.path.exists(DOWNLOADS_DIR):
    os.mkdir(DOWNLOADS_DIR)

app = Flask(__name__)

@app.route('/')
def index():
    downloads = os.listdir(DOWNLOADS_DIR)
    return render_template('index.html', list=downloads)

@app.route('/view/<folder>')
def display_pdf(folder):
    dir = f'{DOWNLOADS_DIR}/{folder}'
    pdf = f'{dir}/All chapters.pdf'
    
    if not os.path.exists(pdf):
        count = 0
        for _, _, files in os.walk(dir):
            count += len(files)
        return f'No PDF found, may still be downloading. Number of files: {count}'
    
    return send_file(pdf, mimetype='application/pdf')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    subprocess.Popen(['python3',
                             '-m',
                             'mangadex_downloader',
                             '--path', DOWNLOADS_DIR,
                             '--language', 'en',
                             '-f', 'pdf-single',
                             '-r',
                             '--use-compressed-image',
                             url])

    return 'Download has been started. Go back and wait.'

if __name__ == '__main__':
    app.run(debug=True)
