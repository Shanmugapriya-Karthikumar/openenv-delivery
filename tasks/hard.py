from env import DeliveryEnv

def run():
    env = DeliveryEnv()
    state = env.reset()

    actions = [
        "deliver",  # wrong start
        "select_order_1",
        "go_to_restaurant",
        "pick_order",
        "go_to_customer",
        "deliver"
    ]

    total_reward = 0

    for action in actions:
        state, reward, done = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward