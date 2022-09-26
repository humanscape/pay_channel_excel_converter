import re
from collections import defaultdict

from constants import WS_NEW_HEADERS

regex_n_people = re.compile("[0-9]인")

def word_converter(words, nick_to_human, CELL_LIST):
    USAGE = ("점심","저녁","식사")
    result = {
        "usage":None,
        "kor_names": "",
        "cell_counter": defaultdict(int)
    }
    for word in words:
        if (
            (not word or word == " ") 
            or 
            (regex_n_people.match(word))
        ):  continue
        
        if any(usage in word for usage in USAGE) \
            and result["usage"] is None :
            result["usage"] = word
            continue

        if word not in nick_to_human:
            return ({"usage":None,"kor_names": None})

        if nick_to_human[word]:
            if result["kor_names"] :
                result["kor_names"] += ","
            result["kor_names"] += nick_to_human[word].kor_name
            result["cell_counter"][nick_to_human[word].cell_name] += 1

    return result

def comment_converter(comment, nick_to_human):
    CELL_LIST = WS_NEW_HEADERS[WS_NEW_HEADERS.indx("셀")+1:-1]
    words = comment.replace("/"," "
        ).replace(",", " "
        ).replace("(", " "
        ).replace(")"," "
        ).split(" ")
    return word_converter(words , nick_to_human, CELL_LIST)