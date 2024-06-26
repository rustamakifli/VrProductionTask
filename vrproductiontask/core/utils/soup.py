from bs4 import BeautifulSoup

def extract_iframe_src(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    iframe = soup.find('iframe')
    
    if iframe:
        src = iframe.get('src')
        return src
    
    return None