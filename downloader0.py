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
dates=dates[1].split(':')
#month and day : mmdd
# mmdd="0211"
mmdd=dates[0]

#hour
# hour="10"
hour=dates[1]



#Longitude [start,stop,step]
# Lon=["0","360",1]
long=sys.argv[2].split('-')
Lon=[long[0],long[1],float(long[2])]
#Longitude [start,stop,step]
# Lat=[30,40,1]
lats=sys.argv[3].split('-')
Lat=[int(lats[0]),int(lats[1]),float(lats[2])]

# #latitude
# lat=str(Lat[0])
#longitude
lon=Lon[0]
#height
# height="300"
height=sys.argv[4]
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
        # print(buffData)
        DATA.append('latitide(degree): '+lat)
        DATA.append(str(buffData))
        TEC.append([lat+','+str(i[0])+','+str(i[-2]) for i in buffData[:-1]])

def exe(timeOut,Lat,TEC,DATA):
    for lat in range(Lat[0],Lat[1],Lat[2]):
        try:
            resp=download(str(lat))
            extractParams(resp,TEC,DATA,str(lat))
            time.sleep(timeOut)
            resp.close()
            print('lat: '+str(lat)+' passed')
        except:
            pass

def saveFiles(DATA,TEC):
    file1=open('tec.txt','w')
    [[file1.write(j+'\n') for j in i ] for i in TEC]
    file1.close()
    file2=open('extractedData.txt','w')
    [[file2.write(str(j)+'\n') for j in i ] for i in DATA]
    file2.close()
    
print(sys.argv[1])

exe(timeOut,Lat,TEC,DATA)
saveFiles(DATA,TEC)
