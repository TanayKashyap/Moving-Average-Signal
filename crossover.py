import pandas as pd
import yfinance as yf  # You can use any other method to get stock data
from twilio.rest import Client

# Function to check moving average crossover and send email
def check_crossover(stock_symbol):
    twilio_account_sid = 'AC496d203fddbc633d132e37baa6589b69'
    twilio_auth_token = '805f4a9426c836462a8edd25d09afb32'
    from_twilio_number = '+15169906339'
    to_phone_number = '+12265051094'

    # Get historical stock data
    stock_data = yf.Ticker(stock_symbol).history(period='max',interval='1d')

    # Calculate short-term and long-term moving averages
    short_window = 20
    long_window = 50

    stock_data['Short_MA'] = stock_data['Close'].rolling(window=short_window, min_periods=1).mean()
    stock_data['Long_MA'] = stock_data['Close'].rolling(window=long_window, min_periods=1).mean()

    # Check for moving average crossover
    if stock_data['Short_MA'].iloc[-1] > stock_data['Long_MA'].iloc[-1] and stock_data['Short_MA'].iloc[-2] <= stock_data['Long_MA'].iloc[-2]:
        body = f'MA crossover signal: Short-term MA crossed above Long-term MA for {stock_symbol}.'
        send_sms(twilio_account_sid, twilio_auth_token, from_twilio_number, to_phone_number, body)
    else:
        print("Did not cross")

def send_sms(account_sid, auth_token, from_number, to_number, body):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number
    )

    print(f"SMS sent: {message.sid}")

stock_symbols = ['ATD.TO','BAM.TO','EQB.TO','AAPL','VFV.TO']

for symbol in stock_symbols:
    check_crossover(symbol)