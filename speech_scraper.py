def get_links(count=5):
    '''
    Returns list of transcript links
    Count gives number of pages to collect
    '''
    from bs4 import BeautifulSoup
    import requests
    import re
    
    if count > 37:
        count = 37
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
            speech.append(str(br.next_sibling))
    return speech


def write_txt(transcript):
    '''
    Write transcript to text file
    '''
    import os
    dirname = 'transcripts/'
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    title = transcript[0]
    states = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 
        'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 
        'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
        'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
        'New Jersey', 'New Mexico', 'New York', 'North Carolina', 
        'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
        'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
        'West Virginia', 'Wisconsin', 'Wyoming']

    for state in states:
        if state in title:
            name = state
            break

    filename = dirname + name + '1.txt'
    num = 1
    while os.path.exists(filename) :
        num += 1
        filename = dirname + name + str(num) + '.txt'

    with open(filename, 'w') as file:
        transcript = '\n'.join(transcript)
        file.write(transcript)

def main():
    
    # Test scrape with J.B. Pritzker
    url = 'https://www.rev.com/blog/transcripts/illinois-governor-j-b-pritzker-coronavirus-press-conference-transcript-may-15'
    transcript = scrape_speech(url)
    write_txt(transcript)
    
    # # Scrape all transcripts included in num pages
    # num = 5
    # url_list = get_links(num)
    # for url in url_list:
    #     transcript = scrape_speech(url)
    #     write_txt(transcript)
    

if __name__ == '__main__':
    main()