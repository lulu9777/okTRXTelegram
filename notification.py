import requests
import json

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    inline_keyboard = [
        [{"text": "🙋🏻‍♂️TRX兑换小T💰【运行中】⏱", "url": "https://t.me/bo6TTTTTT_bot"}],
        [{"text": "千人扫雷💸TRX秒提秒到💸【运行中】", "url": "https://t.me/qrsl_xt03_bot"}]
    ]
    reply_markup = {"inline_keyboard": inline_keyboard}
    data = {"chat_id": chat_id, "text": text, "reply_markup": json.dumps(reply_markup)}
    requests.post(url, data=data)

def handle_prediction_result(predicted_price):
    bot_token = "666xxxxxxxx2:AAFUt7Exxxxxxxxxxxxxx8zB0UUvbqo"
    chat_ids = [-1001xxxxxxxxx696, -10xxxxxxxxx36]  # Your list of chat IDs
    predicted_price_text = f"Predicted Price in One Week: {predicted_price:.5f}"  # Change to 5 decimal places
    print(predicted_price_text)
    for chat_id in chat_ids:
        send_telegram_message(bot_token, chat_id, predicted_price_text)
