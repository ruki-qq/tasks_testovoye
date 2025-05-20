import requests
import time

API = "https://ru.wikipedia.org/w/api.php"
ON_PAGE = 500
CATEGORY = "Категория:Животные_по_алфавиту"
CURR_CHAR = "А"
NUM_OF_MEMBERS = {}


def get_categories(continues_from: str = "") -> list[str]:
    result: requests.Response = requests.get(
        API,
        params={
            "action": "query",
            "list": "categorymembers",
            "cmtitle": CATEGORY,
            "cmtype": "page|subcat",
            "cmlimit": ON_PAGE,
            "format": "json",
            "cmcontinue": continues_from,
        },
    )
    return result.json()


def get_members(res: list[str]) -> str:
    global NUM_OF_MEMBERS, CURR_CHAR
    for member in res["query"]["categorymembers"]:
        member_title: str = member["title"][0]
        if member_title in NUM_OF_MEMBERS:
            NUM_OF_MEMBERS[member_title] += 1
        else:
            NUM_OF_MEMBERS[member_title] = 1
        CURR_CHAR = member_title


def main():
    continues = ""
    while continues is not None:
        result = get_categories(continues)
        continues = result["continue"]["cmcontinue"] if "continue" in result else None
        get_members(result)
        time.sleep(0.5)
    with open("beasts.csv", "w", encoding="utf8") as f:
        for key in NUM_OF_MEMBERS:
            f.write(f"{key},{NUM_OF_MEMBERS[key]}\n")
    print(NUM_OF_MEMBERS)


if __name__ == "__main__":
    main()
