import json
import requests

# TODO: change for >500 results
SEARCH_ENDPOINT_URL = "http://lda.data.parliament.uk/commonsoralquestions.json?_view=Commons+Oral+Questions&_pageSize=500&_search={}&_page=0"
SYNONYM_ENDPOINT_URL = "http://lda.data.parliament.uk/terms.json?_view=Thesaurus&_pageSize=500&_search=%22{}%22&_page=0&_sort=attribute"

links_to_articles = {}


def get_synonyms(word):
    synonyms = []

    full_query = SYNONYM_ENDPOINT_URL.format(word)
    response = requests.get(full_query)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        # print(response_json)

        most_exact = response_json['result']['items'][0]
        # print('Most exact match:', most_exact)
        for match in most_exact['exactMatch']:
            # if the match is not an URL
            if isinstance(match, dict):
                synonyms.append(match['prefLabel']['_value'])

    return synonyms


def search_articles(word, URL):
    """
    Returns a list of articles for the given word.
    """
    for synonym in get_synonyms(word):
        print(synonym, end='\t')

        full_query = URL.format(word)
        response = requests.get(full_query)

        if response.status_code == 200:
            response_json = json.loads(response.text)

            for question in response_json['result']['items']:
                URL = question["_about"]

                if links_to_articles.get(word):
                    links_to_articles[word].append(URL)
                else:
                    links_to_articles[word] = [URL]


def search_all():
    with open("words.txt", "r") as infile:
        for line in infile:
            word = line.strip()

            print("Searching for:", word)
            search_articles(word, SEARCH_ENDPOINT_URL)

print("\n[*]get_synonyms")
print(get_synonyms("tax"))

# print("\n[*]search_articles")
# search_articles("Islamic State", SEARCH_ENDPOINT_URL)

# print("\n[*]search_all")
# search_all()
# print(links_to_articles)
