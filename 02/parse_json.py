import json
import re
from typing import Callable

def default_callback(keyword:str) -> None:
    print(f'Received {keyword}!')

def parse_json(json_str: str,
               required_fields:list[str] = None,
               keywords:list[str] = None,
               keyword_callback:Callable = default_callback
               ) -> None:
    json_doc = json.loads(json_str)
    pattern = f"({'|'.join(keywords)})"
    for rf in required_fields:
        for matched_kw in re.findall(pattern, json_doc[rf]):
            keyword_callback(matched_kw)

if __name__ == '__main__':
    json_str = '{"key1": "word1 word2", "key2": "word2 word3", "key3": "word3 word4"}'
    required_fields = ['key1', 'key3']
    keywords = ['word3', 'word4']

    parse_json(json_str, required_fields, keywords)

