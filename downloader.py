import requests
import time
import sys



#files
DATA=[]
TEC=[]

#timeOut (sec)
timeOut=0.5

iriModel=int(sys.argv[1])
#
url='https://kauai.ccmc.gsfc.nasa.gov/ir_server/iri/submitForm'


#year of data
dates=sys.argv[2].split('-')
year=int(dates[0])
#month and day : mmdd
mmdd=dates[1]

#hour
hour=dates[2]

long=sys.argv[3].split('-')
Lon=[long[0],long[1],float(long[2])]
lats=sys.argv[4].split('-')
Lat=[int(lats[0]),int(lats[1]),float(lats[2])]
print(Lat)

#longitude
lon=Lon[0]
#height
height=sys.argv[5]
#tecHeight
tecHeight="1500"



def download(lat):
    payload={"whichIri":iriModel,"geoFlag":0,"latitude":lat,"longitude":lon,"year":year,
            "mmdd":mmdd,"timeFlag":1,"hour":hour,"height":height,"profileType":3,
            "start":Lon[0],"stop":Lon[1],"stepSize":Lon[2],"dataOptions":0,
            "outputOptions":"1","tecHeight":tecHeight}
    re=requests.post(url, json=payload)
    return re


def extractParams(resp,TEC,DATA,lat):
    buffData=resp.content.decode('utf-8').split('\n')
    initIndex=[buffData.index(i) for i in buffData if 'GEOD' in i][0]+1
    if(initIndex!=1):
        buffData=[[float(j) for j in i.split(' ') if j!=''] for i in buffData[initIndex:]]
        DATA.append('latitide(degree): '+lat)
        [DATA.append(str(i)) for i in buffData]
        TEC.append([lat+','+str(i[0])+','+str(i[-2]) for i in buffData[:-1]])

def exe(timeOut,Lat,TEC,DATA):
    buffer=int((Lat[1]-Lat[0]+1)/Lat[2])
    for lat1 in range(buffer):
        lat=Lat[0]+lat1*Lat[2]
        print(lat)
        try:
            resp=download(str(lat))
            extractParams(resp,TEC,DATA,str(lat))
            time.sleep(timeOut)
            resp.close()
            #print('lat: '+str(lat)+' passed')
        except:
            pass

def saveFiles(DATA,TEC):
    file1=open('tec.txt','w')
    [[file1.write(j+'\n') for j in i ] for i in TEC]
    file1.close()
    file2=open('extractedData.txt','w')
    [file2.write(i+'\n') for i in DATA]
    file2.close()
    


exe(timeOut,Lat,TEC,DATA)
saveFiles(DATA,TEC)
