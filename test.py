from scraper_api import ScraperAPIClient

client = ScraperAPIClient('a381cfe9890b9976dc24ce04a8cf0755')
data = client.get('https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html')
print(data)
