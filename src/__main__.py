from pull_article import article_to_file
from to_polly import article_to_polly

article_url = str(input("Enter Wikipedia URL below\n >> "))

print('Scraping article...')
article_filename = article_to_file(article_url)

print(f'Article Scraped. Saved at {article_filename}')

print('Creating poly audio...')
audio_filename = article_to_polly(article_filename)

print(f'Completed. Audio saved at {audio_filename}')