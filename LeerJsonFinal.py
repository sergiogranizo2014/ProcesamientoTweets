#Librerias
################################################################################################
import json
from io import open
import re
import numpy as np
import pandas as pd  
from textblob import TextBlob 
import emoji

################### Carga de Ficheros Externos ################################################
#############Funcion para Carga datos ###############################
def cargar_datos(ruta,colFiltro):	
	with open(ruta,encoding="utf-8-sig") as f:
		columna=""
		try:
			data=json.load(f)
			columna=data[colFiltro]
			print("archivo " + ruta +" cargado correctamente")
		except Exception as e: 
			print("ERROR:  "+str(e))

	return columna

############## Ficheros Externos ############################
base_tweet=cargar_datos("nuevoFinal.json","tweets")	
base_verb=cargar_datos('ficheros_externos/verbos.json',"verbos")
base_adj=cargar_datos('ficheros_externos/adjetivos.json',"adjetivos")
base_stop=cargar_datos('ficheros_externos/stop.json',"stop")
base_pais=cargar_datos('ficheros_externos/pais.json',"pais")
base_emojis=cargar_datos('ficheros_externos/emojisV3.json',"emojis")
base_emojisG=cargar_datos('ficheros_externos/emo.json',"emojis")


############ Retirar palabras Stop #####################################
def retirar_Stop(lista_original):
	lista_nueva = []
	base_stop
	for i in lista_original:
		if i not in base_stop:
			lista_nueva.append(i)
	return lista_nueva

###############################################################################################
#####_________________Funcion para limpiar datos de caracteres extraños_________________#######
###############################################################################################
def limpiar_tokenizar(tweet):
	tweet2=quitar_unicode(tweet.lower())
	cadena=re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\\w+:\\/\\/\\S+)", " ", tweet2).split()
	cadenaSinDuplicados=eliminar_duplicado(cadena)
	cadenaLimpia1=remover_digitos(cadenaSinDuplicados)
	cadenaLimpia=retirar_Stop(cadenaLimpia1)
	return cadenaLimpia


def quitar_b(cadena):
	return cadena.lstrip("b" )	
##############################################################################################
####___________________Funcion para validar URL_______________________________________########
##############################################################################################
def validarNone(parametro):
	if(parametro=="None"):
		resultado="NO disponible"
	else:
		resultado =quitar_unicode(str(parametro))
	return resultado

##############################################################################################
####__________________Funcion que muestra los datos en columnas_______________________########
##############################################################################################
def mostrar_datos():
	tweets=base_tweet
	
	df=pd.DataFrame(data=[quitar_unicode(str(tweet['text'])) for tweet in tweets], columns=['tweet'])
	#df=pd.DataFrame(data=[quitar_caracteres_raros(tweet['text']).encode("utf-8") for tweet in tweets], columns=['tweet'])

	df['tweet tokenizado']=np.array([str(limpiar_tokenizar(str(tweet['text']))) for tweet in tweets])
	df['hashtag']=np.array([str(extrerHashtags(str(tweet['text']))) for tweet in tweets])
	df['hashtag_relevante']=np.array([str(extrerHashtagsRel(str(tweet['text']))) for tweet in tweets])

	df['fecha']=np.array([quitar_b(tweet['created_at']) for tweet in tweets])

	df['autor']=np.array([str(tweet['user']['name'].encode("utf-8")).replace(str(tweet['user']['name'].encode("utf-8")),
		quitar_unicode(str(tweet['user']['name'].encode("utf-8")))) for tweet in tweets])

	df['nick']=np.array([str(tweet['user']['screen_name'].encode("utf-8")).replace(str(tweet['user']['screen_name'].encode("utf-8")),
		quitar_unicode(str(tweet['user']['screen_name'].encode("utf-8")))) for tweet in tweets])

	df['ubicacion']=np.array([str(str(tweet['user']['location']).encode("utf-8")).replace(str(str(tweet['user']['location']).encode("utf-8")),
		validarNone(str(str(tweet['user']['location']).encode("utf-8")))) for tweet in tweets])

	df['URL']=np.array([str(str(tweet['user']['url']).encode("utf-8")).replace(str(str(tweet['user']['url']).encode("utf-8")),
		validarNone(str(str(tweet['user']['url']).encode("utf-8")))) for tweet in tweets])

	df['menciona_user']=np.array([mencionar_user(tweet['entities']) for tweet in tweets])

	
	df['menciona_pais']=np.array([hallar_pais(quitar_unicode(str(tweet['text']))) for tweet in tweets])

	df['seguidores']=np.array([tweet['user']['followers_count'] for tweet in tweets])

	df['verbos']=np.array([str(hallar_verbo(limpiar_tokenizar(str(tweet['text'])))) for tweet in tweets])
	df['adjetivos']=np.array([str(hallar_adjetivo(limpiar_tokenizar(str(tweet['text'])))) for tweet in tweets])

	df['pronombre']=np.array([str(imprimirPronombre(hallar_verbo(limpiar_tokenizar(str(tweet['text']))))) for tweet in tweets])
	df['Tercera_Persona']=np.array([str(verificaTerPer(imprimirPronombre(hallar_verbo(limpiar_tokenizar(str(tweet['text'])))))) for tweet in tweets])
	df['Plural/Singular']=np.array([str(verificaSinPlu(imprimirPronombre(hallar_verbo(limpiar_tokenizar(str(tweet['text'])))))) for tweet in tweets])
	return df

def mostrar_solo_texto():
	tweets=base_tweet
	df=pd.DataFrame(data=[str(tweet['text'].encode("utf-8")).replace(str(tweet['text'].encode("utf-8")),
		(str(tweet['text'].encode("utf-8")))) for tweet in tweets], columns=['tweet'])
	return df

################################################################################################
###########_________________Funcion que trabajan exclusivamente con iteraciones________##############
################################################################################################
def crear_dataframe():
	verbos=base_verb
	dfv=pd.DataFrame(data=[verbo for verbo in verbos], columns=['verbo'])
	return dfv

#################################################################################################
##_Funcion que busca los verbos de acuerdo a la base de datos verbos.json__#######################
###########__Devuelve la lista de verbos encontrados___________________________________##########
def hallar_verbo(cadena):
	numVerbos=0
	#Lista de verbos
	dfv=crear_dataframe()
	listaV=dfv['verbo'].values.tolist()
	mi_list = []
	for item in cadena:
		if item in listaV:
			numVerbos=numVerbos+1
			mi_list.append(item)
	return mi_list
##############################################################################################
##############################################################################################

def buscarPersonas(verbo):
	verbos=base_verb
	persona=""
	listaN=verbos[verbo]
	#print(listaN)
	for i in (verbos[verbo]):
		if(i['tense']=='Infinitive'):
			break
		elif(i['tense']=='Pastparticiple'):
			break
		elif(i['tense']=='Gerund'):
			break
		else:
			persona=quitarTildes(i['performer'])
	return persona


################################################################################################
###########_________________Funcion que trabajan exclusivamente con los adjetivos_____##########
################################################################################################
def crear_dataframeA():
	adjetivos=base_adj
	dfa=pd.DataFrame(data=[adjetivo for adjetivo in adjetivos], columns=['adjetivo'])
	return dfa

def hallar_adjetivo(cadena):
	#Contador 
	numAdj=0
	#Lista
	dfa=crear_dataframeA()
	listaA=dfa['adjetivo'].values.tolist()
	mi_listA = []
	for item in cadena:
		if item in listaA:
			numAdj=numAdj+1
			mi_listA.append(item)
	return mi_listA
	##############################################################################################
	##############################################################################################

def quitar_unicode(tweet):
	tweetA=quitarN(tweet)
	tweet2=quitarTildes(tweetA)
	tweetB=quitar_caracteres_raros(tweet2)
	tweet1=quitar_b(tweetB)
	cadena=' '.join(re.sub("(@[A-Za-z0-9]+)|(\\\\[\\w]{3})", " ", tweet1).split())
	return cadena

def eliminar_duplicado(lista_original):
	lista_nueva = []
	for i in lista_original:
		if i not in lista_nueva:
			lista_nueva.append(i)
	return lista_nueva

def quitarN(cadena):
	return cadena.replace("\\n","")

def quitarTildes(cadena):
	carAnt = ['Á','á','É','é','Í','í','Ó','ó','Ú','ú','Ñ','ñ']
	#carAnt = ["\u2026"]

	carNue = ['a','a','e','e','i','i','o','o','u','u','ni','ni']

	for y in range(len(cadena)):
		for x in range(len(carAnt)):
			cadena=cadena.replace(carAnt[x],carNue[x])
	return cadena

def imprimirPronombre(lista_original):
		lista=hallar_verbo(lista_original)
		listaPersonas=[]
		for verbo in lista:
			listaPersonas.append(buscarPersonas(verbo))
		return listaPersonas

def remover_digitos(lista_original):
	lista_nueva = []
	for i in lista_original:
		if  re.match('[0-9]',i):
			pass
		else:
			lista_nueva.append(i)
	return lista_nueva

def analizar_sentimiento(tweet):
		analisis=TextBlob(str(tweet))
		if analisis.sentiment.polarity>0:
			return "SI"
		elif analisis.sentiment.polarity==0:
			return "NEUTRO"
		else:
			return "NO"

def verificaTerPer(lista):
	tercera=['el','ella','ellos','ellas']
	if lista:
		for i in tercera:
			valor=(str(lista).find(i))
			if valor>0:
				break
	
		if valor>0: 		
			return "SI"
		else:
			return "NO"
	else:
		return ""

def verificaSinPlu(lista):
	valor=0
	singular=['yo','tu','el']
	if lista:
		for i in singular:
			for j in lista:
				if(i==j):
					valor=1
					break
		
		if valor>0: 		
			return "SINGULAR"
		else:
			return "PLURAL"
	else:
		return ""
def crear_dataframeE():
	emojis=base_emojis
	dfe=pd.DataFrame(data=[emoji for emoji in emojis], columns=['emoji'])
	return dfe

def verificaEmoji(cadena):
	mi_list=[]
	cadena=cadena.encode("utf-8")
	dfv=crear_dataframeE()
	emoticones=dfv['emoji'].values.tolist()
	for emoticon in emoticones:
		valor=str(cadena).find(emoticon)
		if valor>0:
			mi_list.append(emoticon)		
	return mi_list

def hallar_emojis(lista):
	valores=base_emojisG
	lis_emo=[]
	if lista:
		for l in lista:
			if l in valores:
				valor = valores.get(l)
				lis_emo.append(emoji.emojize(valor))
	return lis_emo

def extrerHashtags(cadena):
	hash="#"
	listahash=[]
	for palabra in cadena.split():
		if hash in palabra:
			listahash.append(palabra)
	return listahash

def extrerHashtagsRel(cadena):
		track=['#escort' , '#dulce','#nueva','#flaquita','#joven', '#fresca', '#lolita', '#prepago']
		listahash=[]
		for palabra in cadena.split():
			if palabra in track:
				listahash.append(palabra)
		return listahash
def quitar_caracteres_raros(tweet):

	cadena= re.sub("(\\\\(\\w|[0-9])(\\w|[0-9])(\\w|[0-9])(\\w|[0-9])(\\w|[0-9]))+","", tweet)
	return cadena

def hallar_pais(cadena):
		#Lista
		cadena=cadena.lower()
		paises=base_pais
		dfa=pd.DataFrame(data=[pais for pais in paises], columns=['pais'])
		listaA=dfa['pais'].values.tolist()

		mi_listA = []

		for palabra in cadena.split():
			if palabra in listaA:
				mi_listA.append(palabra)
		return mi_listA

def mencionar_user(item):

	if (item)['user_mentions']:
		menciones=[]
		for j in range(len((item)['user_mentions'])):
			menciones.append((item)['user_mentions'][j]['screen_name'])
		return menciones
	else:
		menciones=[]
		return menciones

if __name__ == '__main__':
	
	#Prueba
	
	df=mostrar_datos()
	
	tweets=base_tweet
	
	df['emoticones']=np.array([str(hallar_emojis(verificaEmoji(tweet['text']))) for tweet in tweets])
	df['sospechoso']=np.array([analizar_sentimiento(tweet['text']) for tweet in tweets])

	print("Generando CSV")
	
	#Importar a un archivo CSV
	df.to_csv('TweetsProcesados.csv',header=True, index=False, sep=';',columns=['tweet','tweet tokenizado','hashtag','hashtag_relevante','fecha','autor','nick','ubicacion','URL','menciona_user','menciona_pais','seguidores','verbos','adjetivos','pronombre','Tercera_Persona','Plural/Singular','emoticones'])
	print("proceso finalizado TweetsFinal.csv creado satisfactoriamente")
