import requests

def request(url)-> dict[str]:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Erro na request dos artigos")

    return response.json()