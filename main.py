#!flask/bin/python
from flask import Flask, request, send_from_directory
import requests
import shutil
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    url = request.args.get('url')
    file_name = download(url)
    archive(file_name)
    move_file_to_downloads(file_name)
    move_file_to_archives(get_filename_without_extension(file_name) + '.tar.gz')
    uploads = os.path.join(os.getcwd(), "archives")
    return send_from_directory(directory=uploads, path=get_filename_without_extension(file_name) + '.tar.gz')


def download(url):
    res = requests.get(url, stream=True)
    file_name = url.split('/')[-1]

    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image successfully Downloaded: ', file_name)
        print("Done!")
        return file_name
    else:
        print('Image Couldn\'t be retrieved')


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
    app.run(debug=True)
