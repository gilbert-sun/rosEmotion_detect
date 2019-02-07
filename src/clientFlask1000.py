import os, pytz
import requests, calendar, datetime,  os
import pprint
import json, codecs
from time import time


'''
1).crontab -e
54 17 * * *   /bin/sh /home/gilbert0/cronTest/repoDayActive.sh >> /home/gilbert0/cronTest/test.log 2>&1

2). run shell script reportFaceType.sh
python client_faceType_emotion.py >> client_faceType_emotion.log 2>&1

3). run parserJson.py  ==> to call write_json_file () 
    write_json_file('temp13.json', face_RepoFormat(2,0.98) )
'''
class logo():
    def __init__(self):
        print ("------------------------------------Step 0:Begin")
        print ("@@   @@@@@@@@@@    @@@@@@@@     @@")
        print ("@@       @@        @@    @@     @@")
        print ("@@       @@        @@@@@@@@     @@")
        print ("@@       @@        @@   @@@     @@")
        print ("@@       @@        @@    @@@    @@")
        print ("------------------------------------Step 0:End")
        print ("\n----------  Beginning: for debug   ----------")


def write_json_file(wfile ,Str):
    json_data = ""

    if not os.path.exists(wfile):
        f = open(wfile, 'wb')
        json_data = json.loads( '{"device_id": "DeviceUser-Test", "statistic_list": []}' )
        json.dump(json_data, codecs.getwriter('utf-8')(f), indent=4,
                  ensure_ascii=False)
        f.close()

    with open(wfile, 'r') as f:
        data = f.read()
        #print (type(data))
        json_data = json.loads(data)
        #print ("--",type(json_data))
        json_data["statistic_list" ].append (json.loads(json.dumps(Str, indent = 4, ensure_ascii = False )))
    #print( "1-----json data: ----",json.dumps(json_data))

    with open(wfile, 'wb') as f:
        json.dump(json_data , codecs.getwriter('utf-8')(f), indent = 4,
               ensure_ascii = False)
        print("3-----json data: ----\n", json.dumps(json_data) )


def face_RepoFormat(ans1,ans2):
    return {"type": ans1, "confident": ans2, "detect_time":   int(time()) }

    with open(fname, 'r') as f:
        data = f.read()
        json_data = json.loads(data)
    # print("=========debug============",json.dumps(json_data))
    return json_data


def default(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(
            calendar.timegm(obj.timetuple())  # * 1000 + obj.microsecond / 1000
        )
        #millis = int ( obj.now(tz=pytz._UTC()).timestamp()) # *1000 )
        return millis
    raise TypeError('Not sure how to serialize %s' % (obj,))

    # user_info = {'name': 'letian', 'password': '123'}

    # r = requests.post('http://127.0.0.1:5000/activity/statistic/fall', data=user_info)
    # print (r.text)
    # r = requests.post('https://amibo-dev.myamibo.com/api/activity/statistic/fall', headers=headers)

def showJson(file):
    with open(file,"r") as f:
	data = f.read()
        jsonData = json.loads(data)
        return (jsonData)

# def write_json_file(wfile ,Str):
#     json_data = ""
#     with open(wfile, 'r') as f:
#         data = f.read()
#         #print (type(data))
#         json_data = json.loads(data)
#         #print ("--",type(json_data))
#         json_data["statistic_list" ].append (json.loads(Str))
#     #print( "1-----json data: ----",json.dumps(json_data))
#
#     with open(wfile, 'wb') as f:
#         json.dump(json_data , codecs.getwriter('utf-8')(f), indent = 4,
#                ensure_ascii = False)
#         print("3-----json data: ----\n", json.dumps(json_data) )

def client_faceType_emotion():
    print ("\n-------client_faceType_emotion--------begin")
    pathName =""
    with open("jsonPath.txt","r") as f:
		pathName = f.readlines()
    return showJson(pathName + "client_faceType_emotion.json")



def client_dayActivity():
    print ("\n-------client_dayActivity--------begin")
    return showJson("client_dayActivity.json")

def client_dayFalling():
    print ("\n-------client_dayFalling--------begin")
    return showJson("client_dayFalling.json")

if __name__ == '__main__':

    #logo()

    sname = os.path.basename(__file__)

    urlAddr = "https://amibo-dev.myamibo.com/api"
    #"http://127.0.0.1:5000"
    #"https://amibo-dev.myamibo.com/api"


    print("---AAA----------------------\n")

    headers = {'content-type': 'application/json','x-api-key':'pdBlWY6qJ81fZnOzBJIwW60XHv1Fd2Ai7ePPxSDg'}
    res = ""
    # res = requests.post("http://127.0.0.1:5000/activity/statistic/fall", data=json.dumps(user_info), headers=headers)



    sname = os.path.basename(__file__)
    if sname == "client_faceType_emotion.py":
        user_info = client_faceType_emotion()
        res = requests.post(urlAddr+"/activity/statistic/face_type", data=json.dumps(user_info),headers=headers)
        print("\n ", sname ," : ", res)
    elif sname == "client_dayActivity.py":
        user_info = client_dayActivity()
        res = requests.post(urlAddr+"/activity/statistic/day_activity", data=json.dumps(user_info),headers=headers)
        print("\n ", sname," : ", res)
    elif sname == "client_dayFalling.py":
        user_info = client_dayFalling()
        res = requests.post(urlAddr+"/activity/statistic/fall", data=json.dumps(user_info),headers=headers)
        print("\n ", sname," : ", res)
    else:
        user_info = showJson("temp1.json")
        #print ("---BBB user info----------------------\n",user_info)
        res = requests.post(urlAddr+"/activity/statistic/fall", data=json.dumps(user_info),headers=headers)
        print ("\nNothing to fit")
        print("\n ",sname," : ", res)




    print ("\n")
    print ("---BBB user info------------",user_info)

    print ("\n")
    print ("---CCC-resp header---------------------",res.headers)

    print ("\n")
    print ("---DDD-resp content---------------------",res.content)

    os.system("rm /media/nvidia/OS_Install/pyfacV3/client_faceType_emotion.json")
   



    #print (datetime.datetime.now()) #.utcnow()
    #print ("---EEE----------------------\n",json.dumps(datetime.datetime.now(), default=default))
