from dotenv import load_dotenv
import requests
import os
from urllib.parse import urlparse
import argparse

load_dotenv()

parser = argparse.ArgumentParser()

API_URL = "https://api-ssl.bitly.com/v4/"


def is_bitlink(url, headers):
    parsed_url = urlparse(url)
    bitlink_id = f"{parsed_url.hostname}{parsed_url.path}"

    request_addres = f'{API_URL}/bitlinks/{bitlink_id}'

    response = requests.get(request_addres, headers=headers)
    return response.ok


def minimize_url(url, headers):
    payload = {
        "long_url": url,
        "domain": "bit.ly"
    }
    response = requests.post(
        f'{API_URL}shorten',
        json=payload,
        headers=headers
    )
    response.raise_for_status()

    decoded_response = response.json()

    return decoded_response["link"]


def count_clicks(bitlink, headers):
    parsed_url = urlparse(bitlink)
    response = requests.get(
        f'{API_URL}bitlinks/{parsed_url.hostname}{parsed_url.path}/clicks/summary',
        headers=headers
    )
    response.raise_for_status()
    return response.json()["total_clicks"]


def main():
    parser.add_argument("url", help="just help",
                        default=0, nargs="?", type=str)
    args = parser.parse_args()
    
    token = os.environ['BITLY_TOKEN']

    headers = {
        'Authorization': f'Bearer {token}'
    }

    input_link = args.url

    try:
        if is_bitlink(input_link, headers):
            print("Клики:", count_clicks(input_link, headers))
        else:
            print("Битлинк:", minimize_url(input_link, headers))
    except requests.exceptions.HTTPError as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()
