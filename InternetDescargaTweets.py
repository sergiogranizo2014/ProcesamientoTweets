import tweepy
from io import open
import credenciales
import json
import time
#Ejercicio para escuchar Tweets en tiempo real#

def autenticar():
	auth = tweepy.OAuthHandler(credenciales.consumer_key, credenciales.consumer_secret)
	auth.set_access_token(credenciales.access_token, credenciales.access_token_secret)
	return auth

#Clase que hereda de StreaListener
class StdOutListener(tweepy.StreamListener):
	contador=0
    
	def on_status(self, status):

		return True

	def on_data(self, data):
		try:
			with open('NuevosTweetsABC.json', 'a') as f:
				f.write(data+",")
				return True
		except BaseException as e:
			pass
		return True


	def on_error(self, status_code):
		print('Error en el estado del codigo: ' + str(status_code))
		return True      

	def on_timeout(self):
		print('Timeout...')
		return True # To continue listening

	def on_limit(self, status):
		print("Limite de conexiones excedido, espere 15 minutos")
		time.sleep(15*60)
		return True

if __name__ == '__main__':
    listener = StdOutListener()
    auth=autenticar()
    stream = tweepy.Stream(auth, listener,tweet_mode='extended')

    #__________Criterio de Busqueda__________________________
    stream.filter(track=['#escort','#dulce','#nueva','#flaquita','#joven', '#fresca', '#lolita', '#prepago'],languages=["es"])



