import json

def parse_grades(grades):
    parsed_grades = []
    for grade in grades:
        if grade["kcname"] is None:
            continue
        parsed_grade = {}
        parsed_grade["department"] = grade["kkdwname"]
        parsed_grade["course"] = grade["kcname"]
        parsed_grade["teacher"] = grade["jsname"]
        parsed_grade["attendance&assignments"] = grade["cjxm1"]
        parsed_grade["final grade"] = grade["cjxm3"]
        parsed_grade["overall grade"] = grade["zcjname1"]
        parsed_grade["gpa"] = grade["jd"]
        parsed_grade["credit"] = grade["xf"]
        parsed_grades.append(parsed_grade)
    return parsed_grades