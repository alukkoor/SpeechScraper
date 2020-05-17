def get_links(count=5):
    '''
    Returns list of transcript links
    Count gives number of pages to collect
    '''
    from bs4 import BeautifulSoup
    import requests
    import re
    
    if count > 37:
        raise ValueError
    res = []
    for i in range(1, count+1):
        url = 'https://www.rev.com/blog/transcript-tag/us-state-governor-coronavirus-briefing-transcripts/page/' + str(i)
        page_response = requests.get(url)
        page_content = BeautifulSoup(page_response.content, 'html.parser')
        for tag in page_content.find_all('a'):
            link = tag.get('href')
            if re.search('blog/transcripts.+', link):
                res.append(link)
    return res


def scrape_speech(url):
    '''
    Returns entire transcript of speech
    '''
    from bs4 import BeautifulSoup
    import requests

    page_response = requests.get(url)
    soup = BeautifulSoup(page_response.content, 'html.parser')
    speech = [soup.title.get_text()]
    for br in soup.find_all('br'):
        if br.nextSibling:
            speech.append(br.next_sibling)
    return speech


def main():
    '''

    TODO: add functionality to write speeches to text files

    '''

    # Test scrape with J.B. Pritzker
    url = 'https://www.rev.com/blog/transcripts/illinois-governor-j-b-pritzker-coronavirus-press-conference-transcript-may-15'
    transcript = scrape_speech(url)
    print(*transcript, sep = '\n')
    
    # # Scrape all transcripts included in num pages
    # num = 5
    # url_list = get_links(num)
    # for url in url_list:
    #     transcript = scrape_speech(url)
    #     print(*transcript, sep='\n')
    

if __name__ == '__main__':
    main()