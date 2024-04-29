#!/usr/bin/python

import argparse
import json
import requests
import textwrap
import os
from datetime import datetime

def convert_to_datetime(created_at):
    original_format = "%a %b %d %H:%M:%S %z %Y"
    return datetime.strptime(created_at, original_format)

def get_tweet_ids_and_dates(json_data):
    print("[*] Cargando JSON....")
    result = []
    try:
        data = json.loads(json_data)
    except:
        print("error al cargar json")
        pass

    for d in data:   
        try:
            tweet = d['tweet']            
            tweet_info = {
                'id_str': tweet['id_str'],
                'created_at': tweet['created_at'],
                'expanded_url': None  
            }
            entities = tweet.get('entities', {})
            if 'media' in entities:
                media = entities['media']
                if media:
                    tweet_info['expanded_url'] = media[0]['expanded_url']
            result.append(tweet_info)
        except ValueError:
            pass

    return result


def parse_req_headers(session):
    sess = {}

    with open(session) as f:
        for line in f:
            try:
                k, v = line.split(':', 1)
                val = v.strip()
                sess[k] = val
            except ValueError:
                pass
    print("[*] Cargando sesión....")
    return sess

def main(args):
    print("Valor de args.js:", args.js) 
    if args.js:
        tweets = args.js
        if not os.path.exists(tweets):
            raise FileNotFoundError(f"No se ha encontrado el archivo {tweets}")
    else: 
        tweets = "tweets.js"
        if not os.path.exists(tweets):
            raise FileNotFoundError("No se ha encontrado el archivo tweets.js")

    f = open(tweets, encoding='UTF-8')
    raw = f.read()
    f.close()

    
    i = raw.find('[')
    tweet_info_list = get_tweet_ids_and_dates(raw[i:])
    

    if not args.request:
        if not os.path.exists("session"):
            raise Exception("No se ha encontrado el archivo session, utilice -r para señalar cual quiere usar.")
        else:
            session = parse_req_headers("session")
    else:
        session = parse_req_headers(args.request)
   
    if args.time:
        comparison_date_str = args.time
        comparison_date = datetime.strptime(comparison_date_str, "%d/%m/%Y")

    for tweet_info in tweet_info_list:
        tweet_media = None
        tweet_id = tweet_info['id_str']
        tweet_date = tweet_info['created_at']
        tweet_datetime = convert_to_datetime(tweet_date)
        if args.time:
            if not args.media:
                if tweet_datetime.date() < comparison_date.date():
                    delete_tweet(session, tweet_id, tweet_datetime)
            else:
                tweet_media = tweet_info['expanded_url']
                if tweet_datetime.date() < comparison_date.date() and tweet_media:
                    delete_tweet(session, tweet_id, tweet_datetime)
        elif args.media:
            if tweet_media:
                delete_tweet(session, tweet_id, tweet_datetime)
        else: 
            delete_tweet(session, tweet_id, tweet_datetime)

deltweets = 0

def delete_tweet(session, tweet_id, TWtime):
    global deltweets
    print(f"[*] borrando tweet: {tweet_id}, publicado en: {TWtime}")
    delete_url = "https://twitter.com/i/api/graphql/VaenaVgh5q5ih7kvyVjgtg/DeleteTweet"
    data = {"variables":{"tweet_id": tweet_id, "dark_request": False}, "queryId": "VaenaVgh5q5ih7kvyVjgtg"}

    
    session["content-type"] = 'application/json'
    r = requests.post(delete_url, data=json.dumps(data), headers=session)
    print(r.status_code, r.reason)
    deltweets += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Herramienta para eliminar tweets en X',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
    [ * ] Se esperan los archivos 'tweets.js' y 'session' en el directorio de ejecución.
    
    Para eliminar todos los tweets, simplemente ejecuta:
    ./Deleting-X.py
    
    Para especificar archivos diferentes o aplicar filtros adicionales, puedes usar estas flags:
    
    ./Deleting-X.py -js archivo.js -r session   # Elimina todos los tweets
    ./Deleting-X.py --media                    # Elimina solo tweets con contenido multimedia vinculado
    ./Deleting-X.py -t 01/01/2010              # Elimina tweets anteriores a esta fecha
    
    Puedes combinar estas configuraciones:
    
    ./Deleting-X.py -js tweets.js -r session --media -t 01/01/2010   # Elimina contenido multimedia anterior a la fecha especificada
    
    Si no especificas -js o -h, la herramienta buscará automáticamente archivos con esos nombres por defecto.
"""))
    
    parser.add_argument('-m', '--media', action='store_true', help='Eliminar imágenes')
    parser.add_argument('-js', '--js', help='carga el archivo de tweets id')
    parser.add_argument('-r', '--request', help='carga el archivo con las cookies de sesión')
    parser.add_argument('-t', '--time', help='Borrar en un rango de tiempo')
    args = parser.parse_args()
    main(args)
    print(f"{deltweets} tweets borrados")
