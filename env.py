import random

class DeliveryEnv:
    def __init__(self):
        self.state_data = None

    def reset(self):
        self.state_data = {
            "location": "start",
            "order_picked": False,
            "delivered": False,
            "time": 0,
            "traffic": random.choice([True, False])
        }
        return self.state_data

    def step(self, action):
        reward = -1

        if action == "go_to_restaurant":
            self.state_data["location"] = "restaurant"

        elif action == "go_to_customer":
            if self.state_data["traffic"]:
                self.state_data["time"] += 2
                reward -= 2
            self.state_data["location"] = "customer"

        elif action == "pick_order":
            if self.state_data["location"] == "restaurant":
                self.state_data["order_picked"] = True
                reward += 5
            else:
                reward -= 5

        elif action == "deliver":
            if self.state_data["location"] == "customer" and self.state_data["order_picked"]:
                self.state_data["delivered"] = True
                if self.state_data["time"] <= 5:
                    reward += 20
                else:
                    reward += 10
            else:
                reward -= 10

        self.state_data["time"] += 1
        done = self.state_data["delivered"] or self.state_data["time"] > 10

        return self.state_data, reward, done

    def state(self):
        return self.state_data