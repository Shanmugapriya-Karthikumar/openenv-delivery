from env import DeliveryEnv

def run():
    env = DeliveryEnv()
    state = env.reset()

    actions = [
        "go_to_restaurant",
        "go_to_customer",
        "go_to_restaurant",
        "pick_order",
        "go_to_customer",
        "deliver"
    ]

    total_reward = 0

    for action in actions:
        state, reward, done = env.step(action)
        total_reward += reward

    return total_reward