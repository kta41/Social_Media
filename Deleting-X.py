import sys
import json
import requests
from datetime import datetime

def convert_to_datetime(created_at):
    original_format = "%a %b %d %H:%M:%S %z %Y"
    return datetime.strptime(created_at, original_format)

def get_tweet_ids_and_dates(json_data):
    result = []
    data = json.loads(json_data)

    for d in data:
        tweet = d['tweet']
        tweet_info = {
            'id_str': tweet['id_str'],
            'created_at': tweet['created_at'],
            'media_url': None  # Establecer media_url a None por defecto
        }
        entities = tweet.get('entities', {})
        if 'media' in entities:
            media = entities['media']
            if media:
                # Si hay información de medios, tomar la primera URL de media_url
                tweet_info['media_url'] = media[0]['media_url']
        result.append(tweet_info)

    return result


def parse_req_headers(request_file):
    sess = {}

    with open(request_file) as f:
        for line in f:
            try:
                k, v = line.split(':', 1)
                val = v.strip()
                sess[k] = val
            except ValueError:
                # Ignora las líneas vacías
                pass

    return sess

def main(ac, av):
    if ac != 4:
        print(f"[!] uso: {av[0]} <jsonfile> <req-headers> <later_date>")
        return

    f = open(av[1], encoding='UTF-8')
    raw = f.read()
    f.close()

    # Saltar datos hasta el primer '['
    i = raw.find('[')
    tweet_info_list = get_tweet_ids_and_dates(raw[i:])

    session = parse_req_headers(av[2])

    comparison_date_str = av[3]
    comparison_date = datetime.strptime(comparison_date_str, "%d/%m/%Y")

    for tweet_info in tweet_info_list:
        tweet_id = tweet_info['id_str']
        tweet_date = tweet_info['created_at']
        tweet_media = tweet_info['media_url']

        tweet_datetime = convert_to_datetime(tweet_date)
        
        #if tweet_media:
        #    print(f"Tweet con ID {tweet_id} tiene una imagen en {tweet_media}")
                
        # Compara las fechas
        if tweet_datetime.date() < comparison_date.date():
         
            delete_tweet(session, tweet_id, tweet_datetime)
            # Tal vez agregar algún retraso aleatorio aquí para evitar futuras limitaciones de velocidad

def delete_tweet(session, tweet_id, TWtime):
    print(f"[*] borrando tweet:{tweet_id}, publicado en: {TWtime}")
    delete_url = "https://twitter.com/i/api/graphql/VaenaVgh5q5ih7kvyVjgtg/DeleteTweet"
    data = {"variables": {"tweet_id": tweet_id, "dark_request": False}, "queryId": "VaenaVgh5q5ih7kvyVjgtg"}

    # Configurar o reconfigurar el encabezado de tipo de contenido correcto
    session["content-type"] = 'application/json'
    r = requests.post(delete_url, data=json.dumps(data), headers=session)
    print(r.status_code, r.reason)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
