TOKEN= '13247fc54a074281afce31e2f1f4803b'
import requests
from textblob import TextBlob

api_key = TOKEN
url = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey={api_key}"
response = requests.get(url)
articles = response.json()["articles"]

sentiments = []

for article in articles:
    title = article["title"]
    content = article["content"]
    
    if not content:
        continue
    
    blob = TextBlob(content)
    
    sentiment = blob.sentiment.polarity
    
    sentiments.append(sentiment)
    
    #print(f"{title}: {sentiment}")

average_sentiment = sum(sentiments) / len(sentiments)

print(f"Sentimiento promedio: {average_sentiment}")
