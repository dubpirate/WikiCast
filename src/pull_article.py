from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag, Comment
import urllib.request
import re

def remove_citations(text:str) -> str:
    '''Uses regex to remove the [52] style citations from the Wikipedia text.'''
    
    # Regex pattern identifying things between square brackets. 
    cit_pat = r'\[.*?\]'
    text = re.sub(cit_pat, '', text)
    return text

def output_file(text:str, url:str) -> str:
    """Saves the given text to the /text/ directory as {article_name}.txt, then returns the uri to the txt file."""
    
    article_name = url.split('/')[-1] 

    article_file_name = f'../text/{article_name}.txt' # Example: ../text/Tweed_Courthouse.txt

    with open(article_file_name, 'w') as article_file:
        article_file.write(text)

    return article_file_name

def parse_elements(raw_article) -> str:
    '''Parses HTML tags in the article body into polly readable text.
    
    returns: polly readable article text (string)'''
    text = ""
    
    for element in raw_article.find_all():
        if element.name == 'p':
            paragraph = element.getText()
            paragraph = remove_citations(paragraph)

            text += paragraph + ' \n'

        elif element.name in ['h1', 'h2', 'h3']:
            heading = element.getText()

            # We want to parse all the way down to the 'See Also' section of the article.
            if "See also" in heading:
                break

            heading = remove_citations(heading)

            text += heading + ". \n"

    return text

def article_to_file(url:str) -> str:
    '''Given a url, this function strips the Wikipedia article into an aws Polly readable txt file.
    
    returns: string of the new article's txt file.'''

    req = urllib.request.urlopen(url)
    article = req.read().decode()


    # Place to store the complete text.
    text = ""

    soup = BeautifulSoup(article, 'html.parser')
    
    # Finding the Article Title 
    title_tag = soup.find('h1', id='firstHeading') 
    title = title_tag.getText() + '. \n'

    text += title

    raw_article = soup.find('div', class_='mw-parser-output')

    article_body = parse_elements(raw_article)

    text += article_body

    article_file_name = output_file(text=text, url=url)

    return article_file_name
