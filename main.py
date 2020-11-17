import requests
import hashlib

url = ' http://localhost:5000/'
filename = "test.txt"
files = {'file': open(filename, 'rb')}
hash = hashlib.md5(filename.encode()).hexdigest()

def upload_file():
    r = requests.post(url+'upload', files=files)
    print(r.status_code)
    print(r.text)

def download_file(filename):
    r = requests.get(url+'download/%s' % filename)
    print(r.status_code)
    print(r.text)

def delete_file(filename):
    r = requests.get(url+'delete/%s' % filename)
    print(r.status_code)
    print(r.text)

upload_file()
download_file(hash)
delete_file(hash)
