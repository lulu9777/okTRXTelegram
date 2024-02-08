import ccxt
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import time
import os
from notification import handle_prediction_result  # import the function from notification.py

def get_past_hour_prices(exchange):
    now = datetime.now()
    past_hour = now - timedelta(weeks=4)  # Change to get past four weeks data
    ohlcv = exchange.fetch_ohlcv('TRX/USDT', '12h', since=int(past_hour.timestamp() * 1000))  # Use 12-hour interval
    return [x[4] for x in ohlcv]

def create_model():
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(None, 1)))  # Increase the number of neurons
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')  # Use mean squared error as the loss function
    return model

def main():
    exchange = ccxt.okex({
        'apiKey': '594xxxxx-ecf2-xxxx-952a-xxxxxa9139c4',
        'secret': '616D6667xxxxxxxxxxx6EDCB1738E',
        'password': 'xxxxxxxxxxxxx',
    })
    exchange.set_sandbox_mode(False)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    model_file = os.path.join(script_dir, "model.h5")

    if os.path.isfile(model_file):
        model = load_model(model_file)
    else:
        model = create_model()

    scaler = MinMaxScaler(feature_range=(0, 1))

    while True:
        try:
            prices = get_past_hour_prices(exchange)
            prices = np.array(prices).reshape(-1, 1)
            prices = scaler.fit_transform(prices)

            if len(prices) < 56:  # Ensure there is enough data to train the model
                print("Not enough data to train the model. Waiting for more data...")
                time.sleep(3600)
                continue

            if os.path.isfile(model_file):
                model.load_weights(model_file)

            # Reshape the data to be 3D
            prices = prices.reshape((prices.shape[0], 1, prices.shape[1]))

            # Split the data into training and validation sets
            train_prices, val_prices = train_test_split(prices, test_size=0.2, shuffle=False)

            # Use early stopping to stop training when the validation loss stops improving
            early_stopping = EarlyStopping(monitor='val_loss', patience=5)  # Increase patience value

            model.fit(train_prices[:-14], train_prices[14:], validation_data=(val_prices[:-14], val_prices[14:]), epochs=20, callbacks=[ModelCheckpoint(model_file), early_stopping])  # Use past data to predict price in one week

            predicted_price = model.predict(prices[-14:].reshape(1, -1, 1))  # Predict price in one week
            predicted_price = scaler.inverse_transform(predicted_price)

            handle_prediction_result(predicted_price[0][0])

            time.sleep(3600)

        except Exception as e:
            print("An error occurred: ", e)
            time.sleep(3600)

if __name__ == "__main__":
    main()
