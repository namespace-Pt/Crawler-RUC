import os
import json
from crawlers import *
from password import student_id, password


if __name__ == "__main__":
    crawler = JWCrawler(
        student_id=student_id,
        password=password,
    )

    os.makedirs("data", exist_ok=True)
    grades = crawler.get_grade()
    json.dump(grades, open("data/grades.json", "w", encoding="utf-8"), ensure_ascii=False)