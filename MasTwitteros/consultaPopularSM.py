import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream
#tweepy es la libreria que trae tweets desde
#la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API
#bloqueara esta cuenta de ejemplo
ckey = "bYKH7MKYT26HtQLDVpk7QbRtH"
csecret = "6giNkYcA4QdW0ziVzDrBt4LlXyqCV3n70C9zb0YLuIcLFxdM0d"
atoken = "333591034-rhUf0DOclVCLlzcd9RUhtCRQs0Gx2q3Fvty6WsyZ"
asecret = "j1BFnPjTiGJnltfcerwMtz2binhxnJO1YZgmwoa9uUGdj"
#####################################
#VARIABLES

QUITO_LOC = [-78.710331,-0.446671,-78.241671,0.036792]
SECTOR_QUITO = [-78.5236433689,-0.2528339981,-78.5218677466,-0.2524263063]
TENDENCIA = ['#DilesNO','#ConsultaPopular','#ConsultaPopularEC',
'#SiRotundo','#EcuadorDespierta','#TodoSi','ConsultaMentirosa','7VecesSí',
'PorlaPatriaDilesNo','7VecesNo','ecuadordicesí','guayasdicesí','pichinchadicesí',
'guayasdiceno','ecuadordiceno','PorlaPatriaDilesSí','@Lenin','@MashiRafael',
'#ConsultaPopularYa','#EcuadorSaleAVotar','#ConsultaPopular2018','ATuFuturoDileSì']

#####################################

class listener(StreamListener):
    def __init__(self, path=None):
        self.path = path
        self.siesta = 0
        self.nightnight = 0
        
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y
            #cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print("Guardado " + "=> " + dictTweet["_id"])
        except:
            print("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print ('Error:', str(status_code))

        if status_code == 420:
            sleepy = 60 * math.pow(2, self.siesta)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print("A reconnection attempt will occur in " + \
            str(sleepy/60) + " minutes.")
            print('''
            *******************************************************************
            From Twitter Streaming API Documentation
            420: Rate Limited
            The client has connected too frequently. For example, an 
            endpoint returns this status if:
            - A client makes too many login attempts in a short period 
              of time.
            - Too many copies of an application attempt to authenticate 
              with the same credentials.
            *******************************************************************
            ''')
            time.sleep(sleepy)
            self.siesta += 1
        else:
            sleepy = 5 * math.pow(2, self.nightnight)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print("A reconnection attempt will occur in " + \
            str(sleepy) + " seconds.")
            time.sleep(sleepy)
            self.nightnight += 1
        return True   
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())


#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('populares')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['populares']

   
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(track=["quito","ecuador"])
#twitterStream.filter(locations=QUITO_LOC)
twitterStream.filter(languages=['es'],track=TENDENCIA)
#twitterStream.filter(track=["quito","ecuador"], async=True)

##
