import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'ComicStream Server Settings'},
    {'type': 'bool',
     'title': 'A boolean setting',
     'desc': 'Boolean description text',
     'section': 'Server',
     'key': 'boolexample'},
    {'type': 'numeric',
     'title': 'Page Buffer',
     'desc': 'How many pages to prefetch',
     'section': 'Server',
     'key': 'pagebuffer'},
    {'type': 'options',
     'title': 'An options setting',
     'desc': 'Options description text',
     'section': 'Server',
     'key': 'optionsexample',
     'options': ['option1', 'option2', 'option3']},
    {'type': 'string',
     'title': 'Server URL',
     'desc': 'URL for server',
     'section': 'Server',
     'key': 'url'},
    {'type': 'path',
     'title': 'Buffer Directory',
     'desc': 'Where to store Page Buffer',
     'section': 'Server',
     'key': 'bufferdir'}])