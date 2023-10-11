import json
import re
from typing import Callable


def default_callback(req_field: str, keyword: str) -> None:
    print(f"Received {keyword} in field {req_field}!")


def parse_json(
    json_str: str,
    required_fields: list[str] = None,
    keywords: list[str] = None,
    keyword_callback: Callable = None,
) -> None:
    if required_fields is None:
        raise ValueError("required_fields can't be None")
    if keywords is None:
        raise ValueError("keywords can't be None")
    if keyword_callback is None:
        raise ValueError("keyword_callback can't be None")

    json_doc = json.loads(json_str)
    if required_fields and keywords:
        pattern = r"(\b" + r"\b|\b".join([kw.lower() for kw in keywords]) + r"\b)"
        for rf in required_fields:
            if rf in json_doc:
                for matched_kw in re.findall(pattern, json_doc[rf].lower()):
                    keyword_callback(rf, matched_kw)


if __name__ == "__main__":
    json_str = (
        '{"key1": "word1 word2word3", "key2": "word2 word3", "key3": "word3 word4"}'
    )
    required_fields = ["key1", "key3"]
    keywords = ["word3", "word4"]

    parse_json(json_str, required_fields, keywords)
