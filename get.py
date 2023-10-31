import requests  
import json

def ocr(filename):
    payload = {'isOverlayRequired': False,
            'apikey': 'K89073348188957',
            'language': 'por',
            }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                        files={filename: f},
                        data=payload,
                        )
        d = r.content.decode()
    return json.loads(d)

if __name__ == "__main__":
    data = ocr('./card.jpg')
    print(data['ParsedResults'][0]["ParsedText"])