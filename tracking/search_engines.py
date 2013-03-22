from collections import namedtuple
from urlparse import urlparse, parse_qs

Engine = namedtuple('Engine', ['name', 'get_query'])

def param_query_getter(param):
    def get_query_from_param(url):
        params = parse_qs(urlparse(url).query)
        try:
            query = params[param][0]
        except KeyError:
            return None
        return query.replace('+', ' ')
    return get_query_from_param

ENGINES = [Engine('yandex', param_query_getter('text')),
           Engine('google', param_query_getter('q')),
           Engine('go.mail.ru', param_query_getter('q'))]

def get_engine(url):
    parsed_url = urlparse(url)
    for engine in ENGINES:
        if engine.name in parsed_url.hostname:
            return engine
    return None

def get_query(url, engine):
    return engine.get_query(url)
