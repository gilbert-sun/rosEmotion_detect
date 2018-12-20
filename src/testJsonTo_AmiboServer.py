
import os, pytz
import requests, time, datetime
import json, codecs

def read_json_file_DayActivity(wfile):
    json_data = ""

    if not os.path.exists(wfile):
        f = open(wfile, 'wb')
        json_data = json.loads( '{"device_id": "DeviceUser-Test","record_time": "2018-12-1","sit_cum_time": 0,"stand_cum_time": 0}' )
        json.dump(json_data, codecs.getwriter('utf-8')(f), indent=4,
                  ensure_ascii=False)
        f.close()

    with open(wfile, 'r') as f:
        data = f.read()

        json_data = json.loads(data)

    #print( "1-----json data: ---1-",json_data)#json.dumps(json_data))
    return json_data


def write_json_file_DayActivity(wfile ,Str):

    json_data = read_json_file_DayActivity (wfile)

    with open(wfile, 'wb') as f:

        json_data["record_time"]=Str["record_time"]

        json_data["sit_cum_time"]=Str["sit_cum_time"]

        json_data["stand_cum_time"]=Str["stand_cum_time"]
    #(json.loads(json.dumps(Str["stand_cum_time"], indent = 4, ensure_ascii = False )))

        json.dump(json_data , codecs.getwriter('utf-8')(f), indent = 4,
               ensure_ascii = False)
        print("3-----json data: ----\n", json.dumps(json_data) )



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
        print("3-----json data: ----\n", json.dumps(json_data))

def fallPosition_RepoFormat(px,py,pz):
    return ( {"detect_time": int(time.time()),"position": "{\"x\":"+ str(px) + ", \"y\":"+str(py)+", \"z\":"+ str(pz)+"}"} )

def face_RepoFormat(ans1,ans2):
    return {"type": ans1, "confident": ans2, "detect_time":int(time.time())}

def dayActivity_RepoFormat(ansSit,ansStand):
    #"%Y-%m-%d %H:%M:%S"
    return {"stand_cum_time": int(ansStand), "sit_cum_time": int(ansSit), "record_time": time.strftime("%Y-%m-%d")}

def showJson(fname='temp1.json'):
    with open(fname, 'r') as f:
        data = f.read()
        json_data = json.loads(data)
    print("=========debug============",json.dumps(json_data))
    return (json_data)

def client_dayActivity():
    print ("\n-------client_dayActivity--------begin")
    return showJson("client_dayActivity.json")

def client_dayFalling():
    print ("\n-------client_dayFalling--------begin")
    return showJson("temp21.json")

def client_faceType_emotion():
    print ("\n-------client_faceType_emotion--------begin")

    return showJson("client_faceType_emotion.json")




if __name__ == '__main__':
    #
    # json_data = read_json_file_DayActivity( "client_dayActivity.json")
    #
    # json_data["sit_cum_time"] += 1
    # json_data["stand_cum_time"] += 1
    #
    # print(write_json_file_DayActivity("client_dayActivity.json", dayActivity_RepoFormat(json_data["sit_cum_time"] , json_data["stand_cum_time"])))
    write_json_file('temp21.json', fallPosition_RepoFormat(4,12,33))
    urlAddr = "https://amibo-dev.myamibo.com/api"


    print("---AAA----------------------\n")

    headers = {'content-type': 'application/json','x-api-key':'pdBlWY6qJ81fZnOzBJIwW60XHv1Fd2Ai7ePPxSDg'}
    res = ""

    user_info = client_dayFalling()
    res = requests.post(urlAddr + "/activity/statistic/fall", data=json.dumps(user_info), headers=headers)
    # user_info = client_faceType_emotion()
    # res = requests.post(urlAddr + "/activity/statistic/face_type", data=json.dumps(user_info), headers=headers)

    print ("---res.headers----------------------\n",res.headers)
    print ("---res.content----------------------\n",res.content)
    print()

    print (time.strftime("%Y-%m-%d %H-%M-%S")) #.utcnow()

