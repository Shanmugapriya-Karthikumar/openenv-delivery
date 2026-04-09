from env import DeliveryEnv

def run():
    env = DeliveryEnv()
    state = env.reset()

    actions = [
        "select_order_1",
        "go_to_restaurant",
        "pick_order",
        "go_to_customer",
        "deliver",

        "select_order_2",
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