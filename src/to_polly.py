import boto3

default_region = 'us-east-2'
defaultUrl = f'https://polly.{default_region}.amazonaws.com'

def read_article(article_uri:str) -> str:
    '''Converts the contents of an article txt file into a single string, and returns it.'''
    article = None

    with open(article_uri, 'r') as article_file:
        article = article_file.read()
        article = article.replace('\n', '')
        article = ' '.join(article.split())

        print(f'Article length (chars): {len(article)}')

    return article

def connect_to_polly(region=default_region, endpoint_url=defaultUrl):
    return boto3.client('polly', region_name=region, endpoint_url=endpoint_url)

def speak(polly, text, output_uri=None, format='mp3', voice='Kendra'):
    resp = polly.synthesize_speech(OutputFormat=format, Text=text, VoiceId=voice)

    if output_uri == None:
        output_uri == '../audio/temp.' + format

    soundfile = open(output_uri, 'wb')
    
    sound_bytes = resp['AudioStream'].read()
    soundfile.write(sound_bytes)

    soundfile.close()

def article_to_polly(article_uri):
    '''Converts the given text into Polly generated audio.'''
    article = read_article(article_uri)

    audio_filename = '../audio/' + article_uri.split('.')[2].split('/')[2] + '.mp3'

    print(f'Audio Filename: {audio_filename}')

    polly = connect_to_polly()

    speak(polly=polly, text=article, output_uri=audio_filename)

    return audio_filename