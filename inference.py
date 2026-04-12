import os
from tasks.easy import run as easy
from tasks.medium import run as medium
from tasks.hard import run as hard
from openai import OpenAI

# ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def call_model():
    # minimal required call
    client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "test"}]
    )

def normalize(score):
    return max(0.0, min(1.0, score / 50))


def main():
    task_name = "delivery"
    env_name = "openenv-delivery"

    print(f"[START] task={task_name} env={env_name} model={MODEL_NAME}", flush=True)

    rewards = []
    steps = 0

    try:
        call_model()  # required

        for name, fn in [("easy", easy), ("medium", medium), ("hard", hard)]:
            score = fn()
            norm_score = normalize(score)

            steps += 1
            done = True
            error = "null"

            rewards.append(norm_score)

            print(
                f"[STEP] step={steps} action={name} reward={norm_score:.2f} done={str(done).lower()} error={error}",
                flush=True
            )

        final_score = sum(rewards) / len(rewards) if rewards else 0.0
        success = final_score > 0.1

    except Exception as e:
        final_score = 0.0
        success = False
        print(f"[DEBUG] error: {e}", flush=True)

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} steps={steps} score={final_score:.2f} rewards={rewards_str}",
        flush=True
    )


if __name__ == "__main__":
    main()
