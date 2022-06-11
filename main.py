#!flask/bin/python
from flask import Flask, request, redirect, render_template, send_file, url_for
import requests
import shutil
import os

app = Flask(__name__, static_folder='archives')


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if len(request.form['url']) == 0 :
            error = 'Paste URL PlS'
        else:
            # redirect to route
            return redirect(url_for('download', url=request.form['url']))
    return render_template('index.html', error=error)


@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    file_name = download_from_url(url)
    archive(file_name)
    move_file_to_downloads(file_name)
    move_file_to_archives(get_filename_without_extension(file_name) + '.tar.gz')
    path = os.path.join(os.getcwd(), 'archives')
    full_path = os.path.join(path, get_filename_without_extension(file_name) + '.tar.gz')
    return send_file(full_path, attachment_filename=get_filename_without_extension(file_name) + '.tar.gz')


def download_from_url(url):
    res = requests.get(url, stream=True)
    file_name = get_file_name_from_url(url)

    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('File successfully Downloaded: ', file_name)
        print("Done!")
        return file_name
    else:
        print('File Couldn\'t be retrieved')


def get_file_name_from_url(url):
    fragment_removed = url.split("#")[0]  # keep to left of first #
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return ""
    return os.path.basename(scheme_removed)


# move file to directory
def move_file_to_downloads(file_name):
    try:
        shutil.move(file_name, "downloads/")
    except:
        pass

    print('File moved: ', file_name)


# move file to directory
def move_file_to_archives(file_name):
    try:
        shutil.move(file_name, "archives/")
    except:
        pass
    print('File moved: ', file_name)


# get filename without extension
def get_filename_without_extension(file_name):
    return file_name.split('.')[0]


# archive file
def archive(file_name):
    path = os.getcwd()
    print(path)
    shutil.make_archive(path + "/" + get_filename_without_extension(file_name),
                        'gztar', path, file_name)
    print('Archive created: ', get_filename_without_extension(file_name))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000)
