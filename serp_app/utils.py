import string
import json
import bs4
import requests

from collections import Counter


def first_number_from_string(string):
    result_string = ''  # output table
    found = False  # if number has been found already

    # check every char of the string
    for char in string:
        if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            result_string += char
            found = True
        elif char != ',' and found:
            break
        else:
            continue

    # result_string to number
    result = None
    if result_string != '':
        result = int(result_string)

    return result


def get_statistics(results):
    headers = ''
    descriptions = ''
    for result in results:
        headers += result[0] + ' '
        descriptions += result[2] + ' '

    headers = headers.translate(str.maketrans('', '', string.punctuation)).lower().split()
    descriptions = descriptions.translate(str.maketrans('', '', string.punctuation)).lower().split()
    headers_and_descriptions = headers + descriptions

    h_wc = Counter(headers)
    d_wc = Counter(descriptions)
    hd_wc = Counter(headers_and_descriptions)

    h_json = json.dumps(h_wc.most_common(10))
    d_json = json.dumps(d_wc.most_common(10))
    hd_json = json.dumps(hd_wc.most_common(10))

    return h_json, d_json, hd_json


def query_google(query, no_results_to_return=10, user_agent='', proxy=''):
    url = f'http://www.google.com/search?q={query}&num={no_results_to_return}&ie=UTF-8'

    session = requests.Session()

    # setting headers
    request_headers = {
        'Accept': 'text/html,application/xhtml,application/xml',
        'Accept-Language': 'en-US,en;q=0.9;pl-PL,pl;q=0.7',
        'Dnt': '1'
    }
    if user_agent != '':
        request_headers['User-Agent'] = f'{user_agent}'
    else:
        # TODO: make this default if empty!
        request_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
    session.headers.update(request_headers)

    # setting proxy
    if proxy != '':
        session.proxies.update({'http': proxy})

    # fetching and parsing
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # getting number of Google Search results
    number_of_results = 0
    no_results_string = soup.find(id="resultStats")
    if no_results_string:
        number_of_results = first_number_from_string(no_results_string.text)

    # getting the real results
    results = []
    search_results = soup.find_all('div', 'g')
    for res in search_results:
        header = res.find('h3')
        link = res.find('a')
        description = res.find('div', 's')
        if not header or not link or not description:
            continue
        else:
            results.append((header.text, link.get('href'), description.text))

    h_stats, d_stats, hd_stats = get_statistics(results)

    return number_of_results, results, h_stats, d_stats, hd_stats
