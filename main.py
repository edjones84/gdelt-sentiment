import json
from multiprocessing.pool import ThreadPool

import nltk
import requests as requests
import six

from typing import Any, Union

from deep_translator.exceptions import LanguageNotSupportedException
from requests import Response
from nltk.sentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
import iso639
from app_const import BASE_URL, RECORDS, TIME, REQUEST_HEADERS, DESTINATION_LANG, ALT_ISO691_COUNTRY_CODES

nltk.downloader.download('vader_lexicon')
#comment test

def query(query_term: str) -> str:
    """Function to output query term with spaces changed to %20"""
    stripped_query: str = query_term.replace(" ", "%20")
    return stripped_query


def gdelt_url_gen(query_term: str) -> str:
    """supplier function to return a url string"""
    # note there is no language set so we get articles from any language these are then translated using deep translator
    final_url: str = f"{BASE_URL}query={query(query_term)}&mode=ArtList&maxrecords={RECORDS}&format=json&timespan={TIME}"
    return final_url


def make_request(query_term: str) -> dict[str, Any]:
    """supplier function to make the request and return the request as a string"""
    requester: Response = requests.get(url=gdelt_url_gen(query_term), headers=REQUEST_HEADERS)
    return json.loads(requester.text)


def language_to_iso639_1(language: str) -> str:
    """wrapper around iso639 library to correctly handle hebrew and chinese in the desired formats for deep
    translator"""
    if language in ALT_ISO691_COUNTRY_CODES:
        return ALT_ISO691_COUNTRY_CODES[language]
    else:
        return iso639.to_iso639_1(language)


def translate_text(source_lang: str, text: str) -> str:
    """Translates text into the target language that is set as the default of english. Text that cant be translated is
    just left inplace. The Google Translator requires language codes to be in iso639, hence that mapping is applied.
    """
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    try:
        translated_text = GoogleTranslator(source=language_to_iso639_1(source_lang),
                                           target=DESTINATION_LANG).translate(text)
    except LanguageNotSupportedException as re:
        translated_text = text
    return translated_text


def translated_dict_gen(gdelt_dict_in: dict[str, str]) -> dict[str,str]:
    """Take on a dictionary that was generated from the gdelt and translate all titles, maintaining the origin
    language """
    return {
            **{'title': translate_text(source_lang=gdelt_dict_in['language'].lower(), text=gdelt_dict_in['title'])},
            **{'language': gdelt_dict_in['language']}
        }


def extract_titles(returned_request: dict[str, Any]) -> list[dict[str, str]]:
    """Loop through all items from the gdelt json list and return the translated versions of the titles,
    with the origin language. This utilises multithreading for the translation function"""
    articles = returned_request['articles']
    with ThreadPool(processes=10) as pool:
        extracted_titles = pool.map(translated_dict_gen, articles)
    return extracted_titles


def analyse_sentiments(string: str) -> dict[str, float]:
    """input a string and output the polarity scores for that string"""
    sia: SentimentIntensityAnalyzer = SentimentIntensityAnalyzer()
    return sia.polarity_scores(string)


def sentiment_dictionary_gen(list_to_analyse: list[dict[str, str]]) -> list[dict[str, Union[float, str]]]:
    """pass through a list of phrases and analyse the sentiment, outputting the title with scores"""
    output_scores: list[dict[str, float]] = []
    for item in list_to_analyse:
        tmp_dict: dict[str, Union[float, str]] = analyse_sentiments(item['title'])
        tmp_dict['title'] = item['title']
        tmp_dict['origin_language'] = item['language']
        output_scores.append(tmp_dict)
    return output_scores


def average_sentiments(input_scores: list[dict[str, float]]) -> float:
    """get all the sentiments for each text and average them to a single compound score"""
    list_counter: int = 0
    compound: float = 0
    for scores in input_scores:
        tmp_compound_score: float = scores['compound']
        compound += tmp_compound_score
        list_counter += 1

    return compound / list_counter


def main(search_term: str) -> None:
    response_json = make_request(search_term)
    print(response_json)
    titles: list[dict[str, str]] = extract_titles(response_json)
    scores_out: list[dict[str, Union[float, str]]] = sentiment_dictionary_gen(titles)
    print(scores_out)
    print(average_sentiments(scores_out))


if __name__ == '__main__':
    user_input = "Cost of Living"
    main(user_input)

