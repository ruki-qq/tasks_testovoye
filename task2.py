import requests
import time

API = "https://ru.wikipedia.org/w/api.php"
ON_PAGE = 500
CATEGORY = "Категория:Животные_по_алфавиту"
CURR_CHAR = "А"
LAST_CHAR = "Я"
member_count = 0
NUM_OF_MEMBERS = {}

def get_categories(continues_from:str = '') -> list[str]:
    result = requests.get(API, params={
        "action": "query",
        "list": "categorymembers",
        "cmtitle": CATEGORY,
        "cmtype": "page|subcat",
        "cmlimit": ON_PAGE,
        "format": "json",
        "cmcontinue": continues_from})
    return result.json()

def get_members(res: list[str]) -> str:
    global NUM_OF_MEMBERS, CURR_CHAR, member_count
    with open("beasts.csv", "a", encoding="utf8") as f:
        for animal in res["query"]["categorymembers"]:
            member_title: str = animal["title"][0]
            print(animal)
            if member_title in NUM_OF_MEMBERS:
                NUM_OF_MEMBERS[member_title] += 1
            else:
                NUM_OF_MEMBERS[member_title] = 1
                f.write(CURR_CHAR + f" {member_count}" +  "\n")
            CURR_CHAR = member_title
    return CURR_CHAR
def main():
    continues = ''
    my_char = ''
    while my_char != LAST_CHAR:
        result = get_categories(continues)
        continues = result["continue"]["cmcontinue"]
        my_char = get_members(result)
        time.sleep(2)
    print(NUM_OF_MEMBERS)

main()
class Op:
    def __init__(self):
        pass
