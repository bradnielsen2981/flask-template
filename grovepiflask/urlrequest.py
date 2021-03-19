import urllib.parse
import urllib.request
import time

#---EXTERNAL URL REQUEST LIBRARY---------------------------------------#
def sendurlrequest(url, dictofvalues):
    data = urllib.parse.urlencode(dictofvalues)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)

    #if data is returned
    with urllib.request.urlopen(req) as response:
        responsedata = response.read()
    return responsedata

if __name__ == '__main__':
    #send data to database
    dictofvalues = {"hiveid":1,"temp":32.3,"hum":70}
    url = "https://nielbrad.pythonanywhere.com/handleurlrequest"
    response = sendurlrequest(url, dictofvalues)
    print(response)