from tasks.easy import run as easy
from tasks.medium import run as medium
from tasks.hard import run as hard

def evaluate():
    scores = {
        "easy": easy(),
        "medium": medium(),
        "hard": hard()
    }

    avg_score = sum(scores.values()) / 3

    return {
        "scores": scores,
        "average_score": avg_score
    }

# 🔥 THIS PART IS VERY IMPORTANT
if __name__ == "__main__":
    print("Running evaluator...")
    result = evaluate()
    print(result)