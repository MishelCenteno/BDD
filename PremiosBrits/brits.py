
import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "SEvk2LCbY6Jies6leTYG2LhIM"
csecret = "2P3OXvLQTBRUlu2SJhlduxx2tA9wbWitSaqDY39YzjL3nv5ZDx"
atoken = "1026854286-ZFTBo7TVvsvi4cg2I7eR5bSD3R1EFYSFBjvWNxh"
asecret = "rhJcrVfaQID0HKriR49mGPvz79ZQkBwJ1VOdsoSI0URv6"

#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('brits')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['brits']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["#BRITVIDHARRYSTYLES","#BRITVIDLIAMPAYNE","#BRITVIDZAYN"])
#twitterStream.filter(locations=[-78.5236272757,-0.2524048489,-78.5218945686,-0.2519864283])
