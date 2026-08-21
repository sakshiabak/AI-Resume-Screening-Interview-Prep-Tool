"""
question_bank.py
Generates mock interview questions based on skills matched between
the resume and the job description.
"""

import random

QUESTION_BANK = {
    "python": [
        "What is the difference between a list and a tuple in Python?",
        "Explain how memory management works in Python.",
        "What are Python decorators and when would you use one?",
    ],
    "java": [
        "Explain the difference between JDK, JRE, and JVM.",
        "What is the difference between an abstract class and an interface?",
        "How does garbage collection work in Java?",
    ],
    "sql": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "How would you optimize a slow SQL query?",
        "Explain normalization and why it's important.",
    ],
    "machine learning": [
        "Explain the bias-variance tradeoff.",
        "How do you handle overfitting in a machine learning model?",
        "What is the difference between supervised and unsupervised learning?",
    ],
    "deep learning": [
        "Explain how backpropagation works.",
        "What is the vanishing gradient problem and how do you solve it?",
        "Compare CNNs and RNNs — when would you use each?",
    ],
    "data structures": [
        "When would you use a linked list over an array?",
        "Explain how a hash table handles collisions.",
        "What is the time complexity of common operations on a binary search tree?",
    ],
    "algorithms": [
        "Explain the difference between BFS and DFS.",
        "What is dynamic programming and when should you use it?",
        "Walk me through how you'd approach an optimization problem.",
    ],
    "react": [
        "Explain the difference between state and props in React.",
        "What are React hooks and why were they introduced?",
        "How does the virtual DOM improve performance?",
    ],
    "django": [
        "Explain the MVT architecture in Django.",
        "How does Django handle database migrations?",
        "What is middleware in Django and how have you used it?",
    ],
    "flask": [
        "How is Flask different from Django?",
        "How would you structure a large Flask application?",
        "Explain how you'd handle authentication in a Flask app.",
    ],
    "aws": [
        "What AWS services have you used and for what purpose?",
        "Explain the difference between EC2 and Lambda.",
        "How would you design a highly available architecture on AWS?",
    ],
    "docker": [
        "What is the difference between a Docker image and a container?",
        "Explain the purpose of a Dockerfile.",
        "How would you reduce the size of a Docker image?",
    ],
    "git": [
        "What is the difference between 'git merge' and 'git rebase'?",
        "How do you resolve a merge conflict?",
        "Explain your typical Git branching strategy.",
    ],
    "system design": [
        "How would you design a URL shortening service?",
        "Explain the concept of horizontal vs vertical scaling.",
        "How would you design a rate limiter?",
    ],
    "dbms": [
        "What is ACID in the context of databases?",
        "Explain the different types of database indexing.",
        "What is the difference between a clustered and non-clustered index?",
    ],
    "computer networks": [
        "Explain the difference between TCP and UDP.",
        "What happens when you type a URL into a browser and hit enter?",
        "Explain the OSI model layers briefly.",
    ],
    "operating systems": [
        "Explain the difference between a process and a thread.",
        "What is a deadlock and how can it be prevented?",
        "Explain paging and segmentation in memory management.",
    ],
    "communication": [
        "Tell me about a time you had to explain a technical concept to a non-technical audience.",
        "How do you handle disagreements within a team?",
    ],
    "teamwork": [
        "Describe a challenging team project and your role in it.",
        "How do you handle a teammate who isn't contributing equally?",
    ],
    "leadership": [
        "Tell me about a time you led a project or a team.",
        "How do you motivate a team during a tight deadline?",
    ],
    "project management": [
        "How do you prioritize tasks when managing multiple deadlines?",
        "What project management tools/methodologies have you used?",
    ],
}

GENERIC_QUESTIONS = [
    "Tell me about a project where you used {skill}.",
    "What challenges have you faced while working with {skill}, and how did you solve them?",
    "How would you explain {skill} to someone with no technical background?",
    "Rate your proficiency in {skill} and justify it with an example.",
]

BEHAVIORAL_QUESTIONS = [
    "Tell me about yourself.",
    "Why do you want to work for this company?",
    "Describe a time you failed and what you learned from it.",
    "Where do you see yourself in 5 years?",
    "Why should we hire you over other candidates?",
]


def generate_questions(matched_skills, num_technical=5, num_behavioral=3):
    """
    Generate a mixed set of technical (based on matched skills) and
    behavioral interview questions.
    """
    technical_questions = []

    skills_pool = list(matched_skills) if matched_skills else []
    random.shuffle(skills_pool)

    for skill in skills_pool:
        if len(technical_questions) >= num_technical:
            break
        bank = QUESTION_BANK.get(skill)
        if bank:
            technical_questions.append(random.choice(bank))
        else:
            template = random.choice(GENERIC_QUESTIONS)
            technical_questions.append(template.format(skill=skill))

    # If not enough matched-skill questions, pad with generic ones
    while len(technical_questions) < num_technical and skills_pool:
        skill = random.choice(skills_pool)
        template = random.choice(GENERIC_QUESTIONS)
        q = template.format(skill=skill)
        if q not in technical_questions:
            technical_questions.append(q)
        else:
            break

    behavioral_questions = random.sample(
        BEHAVIORAL_QUESTIONS, min(num_behavioral, len(BEHAVIORAL_QUESTIONS))
    )

    return {
        "technical": technical_questions,
        "behavioral": behavioral_questions,
    }
