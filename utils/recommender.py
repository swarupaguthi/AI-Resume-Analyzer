def recommend_field(skills):
    if "Machine Learning" in skills or "AI" in skills:
        return "Artificial Intelligence / Machine Learning"
    elif "Web Development" in skills or "Flask" in skills:
        return "Web Development"
    elif "Python" in skills:
        return "Python Developer"
    else:
        return "General IT / Software Development"


def recommend_courses(field):
    courses = {
        "Artificial Intelligence / Machine Learning": [
            "Machine Learning with Python",
            "Deep Learning Specialization",
            "AI for Everyone"
        ],
        "Web Development": [
            "Full Stack Web Development",
            "Flask for Beginners",
            "React Basics"
        ],
        "Python Developer": [
            "Python Programming Masterclass",
            "Data Structures in Python"
        ],
        "General IT / Software Development": [
            "Computer Fundamentals",
            "Programming Basics"
        ]
    }
    return courses.get(field, [])