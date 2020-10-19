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

dictofvalues = {"data1":"WHY AM I HERE?"}
url = "https://nielbrad.pythonanywhere.com/handleurlrequest"

response = sendurlrequest(url, dictofvalues)
#time.sleep(3)
print(response)

#ANOTHER CHANGE
print("THis changed")