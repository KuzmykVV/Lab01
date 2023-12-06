import gym
import matplotlib.pyplot as plt
import numpy as np
import ray

ray.init()

class KingOfTheHill(gym.Env):
    def __init__(self):
        super(KingOfTheHill, self).__init__()
        self.observation_space = gym.spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(3)
        # Інші необхідні параметри та ініціалізація

    def step(self, actions):
        new_state = np.random.uniform(low=0, high=100, size=(1,))
        reward = np.random.uniform(low=0, high=1)
        done = False  # Ініціалізуємо значення done як False
        return new_state, reward, done

    def reset(self):
        # Генерація початкового спостереження та ініціалізація агентів
        initial_observation = np.random.uniform(low=0, high=100, size=(1,))  # Приклад початкового стану

        # Ініціалізація агентів у початкових позиціях
        self.agents_positions = {}
        for i in range(num_agents):
            self.agents_positions[i] = np.random.uniform(low=0, high=100, size=(1,))  # Початкові позиції агентів

        return initial_observation

# Agent class with slight modifications for Ray implementation
@ray.remote
class Agent:
    def __init__(self, agent_id, observation_space, action_space):
        self.agent_id = agent_id
        self.observation_space = observation_space
        self.action_space = action_space
        self.q_table = np.random.rand(100, 3)  # Initial Q-table for training

    def choose_action(self, obs):
        action = np.argmax(self.q_table[int(obs)])
        return action

    def update(self, obs, action, reward, next_obs, done):
        current_q_value = self.q_table[int(obs), action]
        next_max_q = np.max(self.q_table[int(next_obs)])
        new_q = current_q_value * (reward * next_max_q - current_q_value)
        self.q_table[int(obs), action] = new_q


# Function to train agents in parallel using Ray
@ray.remote
def train_agents_parallel(env, agents, num_episodes):
    rewards_per_episode = []
    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        count = 0
        while not done and count < 1000:
            count += 1
            actions = [agent.choose_action.remote(obs) for agent in agents]
            actions = ray.get(actions)
            next_obs, reward, done = env.step(actions)
            next_obs_ids = [agent.update.remote(obs, actions[idx], reward, next_obs, done) for idx, agent in enumerate(agents)]
            ray.get(next_obs_ids)
            obs = next_obs
            total_reward += reward
        rewards_per_episode.append(total_reward)

        print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

    return rewards_per_episode


def analyze_results(rewards_per_episode):
    plt.plot(rewards_per_episode)
    plt.xlabel('Епізод')
    plt.ylabel('Винагорода')
    plt.title('Зміна винагороди від епізоду')
    plt.show()

# Creating environment and agents
env = KingOfTheHill()
num_agents = 3
agents = [Agent.remote(agent_id=i, observation_space=env.observation_space, action_space=env.action_space) for i in range(num_agents)]

# Parallel training of agents
num_episodes = 20
rewards_ids = [train_agents_parallel.remote(env, agents, num_episodes) for _ in range(num_agents)]
rewards = ray.get(rewards_ids)

# Aggregate rewards from different agents for analysis
avg_rewards = np.mean(rewards, axis=0)
analyze_results(avg_rewards)

ray.shutdown()