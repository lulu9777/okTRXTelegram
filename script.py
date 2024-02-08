import requests
import time
import random
import logging

# 配置日志
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, data=data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message: {e}")

def fetch_and_send_message(bot_token, chat_id):
    try:
        response = requests.get('https://apilist.tronscan.org/api/transaction?sort=-timestamp&limit=1')
        response.raise_for_status()  # raise an exception if the request was unsuccessful
        trx_info = response.json()

        if 'toAddress' in trx_info['data'][0]:
            trx_address = trx_info['data'][0]['toAddress']
            send_telegram_message(bot_token, chat_id, trx_address)
        else:
            logging.error("toAddress not found in the response")
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.error(f"Failed to fetch transaction info: {e}")

def main():
    bot_token = '63xxxxx309:AAGIBxxxxxxxxxxxxxx6IHH4gEzLwardEY2Sw'
    chat_ids = [-100xxxxxxx696, -10xxxxxxxx636]

    while True:
        for chat_id in chat_ids:
            fetch_and_send_message(bot_token, chat_id)
            time.sleep(random.randint(3600, 10800))  # sleep for a random interval between 1 and 3 hours

if __name__ == "__main__":
    main()
