import requests 
import pandas as pd 
from bs4 import BeautifulSoup

def get_num_links():
    """
    Inputing the number of links that should be considered 

    Returns:
    num_links*36 (The step is 36)
    """
    try:
        num_links = int(input('Input the number of lists (max 79): '))
        if num_links < 0 or num_links > 79:
            raise ValueError
    except:
        raise ValueError
    return num_links*36

def formate_links(num_links):
    """
    The preparation of list filled with links of each character
    Taken from API 

    Inputs: 
    num_links (int): The number of the links that should be considered

    Returns: 
    The list of links
    """
    links = []
    for i in range(0, num_links, 36):
        api_url = f'https://www.marvel.com/v1/pagination/grid_cards?offset={i}&limit=36&entityType=character&sortField=title&sortDirection=asc'
        try:
            response = requests.get(api_url)
        except Exception as _ex:
            print("Error: ", _ex)
            return 0
        data=response.json()
        records = data.get('data', {}).get('results', []).get('data', [])
        _links = [record.get('link', {}).get('link') for record in records]
        links.extend(_links)
    print("[I] The links list successfuly created.")
    return links



def get_every_value(links):
    """
    Parsing data of every character from the site 
    
    Inputs: 
    links []: The links list

    Returns:
    data dict(): The dictionary of data
    """
    name = [] 
    link = []
    universe = []
    aliases = []
    edu = []
    origin = [] 
    identity = []
    relatives = [] 

    for l in links:
        url = 'https://www.marvel.com' + l
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        _name = soup.find('span', class_='masthead__eyebrow')
        name.append(_name.get_text() if _name else 'No data')

        universe_para = soup.find('p', string='Universe')
        universe.append(universe_para.find_next('ul').find('li').get_text() if universe_para else 'No data')

        aliases_para = soup.find('p', string='Other Aliases')
        aliases.append(aliases_para.find_next('ul').find('li').get_text() if aliases_para else 'No data')

        edu_para = soup.find('p', string='Education')
        edu.append(edu_para.find_next('ul').find('li').get_text() if edu_para else 'No data')

        origin_para = soup.find('p', string='Place of Origin')
        origin.append(origin_para.find_next('ul').find('li').get_text() if origin_para else 'No data')

        identity_para = soup.find('p', string='Identity')
        identity.append(identity_para.find_next('ul').find('li').get_text() if identity_para else 'No data')

        relatives_para = soup.find('p', string='Known Relatives')
        relatives.append(relatives_para.find_next('ul').find('li').get_text() if relatives_para else 'No data')
        
        link.append(l)
    data = {
        'name': name,
        'link': link,
        'universe': universe,
        'aliases': aliases, 
        'education': edu, 
        'origin': origin,
        'identity': identity,
        'relatives': relatives,
    }
    print('[I] All the data had been parsed successfully.')
    return data

def create_csv(res):
    """
    The preparation of .csv dataset

    Inputs:
    res dict(): The ready data dictionary

    Returns:
    Creates 'characters.csv' dataset 
    """
    df=pd.DataFrame(res)
    df.to_csv('characters.csv')

def main():
    num_links = get_num_links()
    links = formate_links(num_links)
    res = get_every_value(links)
    create_csv(res)


if __name__ == '__main__':
    main()

