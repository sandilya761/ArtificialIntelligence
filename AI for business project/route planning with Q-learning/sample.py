import random


class HyperParameters:

    def __init__(self, discount_factor=0.75, learning_rate=0.9, num_iterations=1000):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations


# Part-1 defining the environment
# define the states, actions, rewards
class Environment:
    def __init__(self, environment_graph, goal_state):
        self.environment_graph = environment_graph
        self.goal_state = goal_state

        # this line makes sure that the agent can go to goal state
        # from goal state (self loop in a graph)
        self.environment_graph[self.goal_state].append(self.goal_state)

        self.qvalues = self._initialize_qvalues()
        self.state_list = self._get_state_list()

    def _initialize_qvalues(self):
        qvalues = {}
        for state, action_list in self.environment_graph.items():
            for action in action_list:
                qvalues[(state, action)] = 0
        return qvalues

    def _get_state_list(self):
        return list(self.environment_graph.keys())

    def get_possible_actions(self, state):
        return list(self.environment_graph[state])

    def get_reward(self, state, action):
        # if the agent is going to goal state from goal state then return reward=1
        # else return reward=0
        return {(self.goal_state, self.goal_state): 1}.get((state, action), 0)

    def run_step(self, parameters):
        current_state = random.choice(self.state_list)
        current_action = random.choice(self.get_possible_actions(current_state))
        next_state = current_action

        possible_actions_of_next_state = self.get_possible_actions(next_state)
        next_qvalues = [self.qvalues[(next_state, next_action)] for next_action in possible_actions_of_next_state]

        next_qmax = max(next_qvalues)

        temporal_difference = self.get_reward(current_state, current_action) + (parameters.discount_factor * next_qmax) - self.qvalues[(current_state, current_action)]

        self.qvalues[(current_state, current_action)] += parameters.learning_rate * temporal_difference

    def get_route_to_goal(self, start_state):
        path = [start_state]
        current_state = start_state  # initializing
        while current_state != self.goal_state:
            possible_actions = self.get_possible_actions(current_state)
            current_state = max(possible_actions, key=lambda action: self.qvalues[(current_state, action)])

            path.append(current_state)

        return path


# Part-2 building the AI solution
# implement the Q-learning algorithm and train it
if __name__ == "__main__":
    environment_graph = {
        0: [1],
        1: [0, 2, 5],
        2: [1, 6],
        3: [7],
        4: [8],
        5: [1, 9],
        6: [2, 7],
        7: [3, 6, 11],
        8: [4, 9],
        9: [5, 8, 10],
        10: [9, 11],
        11: [7, 10],
    }

    parameters = HyperParameters()
    warehouse_env = Environment(environment_graph, 6)

    # finding the optimal policy
    for _ in range(parameters.num_iterations):
        warehouse_env.run_step(parameters)

    # Part-3 production
    # tool to return the shortest route towards
    # the top priority location

    # evaluating the policy
    print(warehouse_env.get_route_to_goal(4))
