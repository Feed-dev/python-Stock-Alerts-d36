import requests
from newsapi import NewsApiClient
from twilio.rest import Client

# fill in your own API keys and phone numbers
newsapi = NewsApiClient(api_key="YOUR OWN API KEY FROM NEWSAPI")
account_sid = "YOUR TWILIO ACCOUNT SID"
auth_token = "YOUR TWILIO AUTH TOKEN"
client = Client(account_sid, auth_token)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=APIKEY'
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# request stock data
r = requests.get(STOCK_ENDPOINT)
data = r.json()
time_series = data['Time Series (Daily)']

# get prices and calculate difference
yesterday = list(time_series.keys())[0]
yesterday_closing_price = time_series[yesterday]['4. close']
print(yesterday_closing_price)

day_before_yesterday = list(time_series.keys())[1]
day_before_yesterday_closing_price = time_series[day_before_yesterday]['4. close']
print(day_before_yesterday_closing_price)

positive_difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if positive_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage_difference = (positive_difference / float(yesterday_closing_price)) * 100
print(percentage_difference)

# use the News API to get articles when the difference is greater than 5%
if percentage_difference > 0.1:
    all_articles = newsapi.get_everything(q=COMPANY_NAME, language='en', sort_by='relevancy')
    first_three_articles = all_articles['articles'][:3]

    articles = all_articles['articles']
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in articles]
    print(formatted_articles)

    # send the articles via SMS
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='VIRTUAL_TWILIO_NUMBER',
            to='VERIFIED_NUMBER'
        )
        print(message.status)
