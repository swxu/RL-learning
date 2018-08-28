import gym
from RLBrain import DeepQNetwork

env = gym.make('CartPole-v0')
env = env.unwrapped

print(env.action_space)     # how many actions could be used
print(env.observation_space) # how many observations of states could be used
print(env.observation_space.high)   # maximum
print(env.observation_space.low)    # minimum

RL = DeepQNetwork(n_actions=env.action_space.n,
                  n_features=env.observation_space.shape[0],
                  learning_rate=0.01, e_greedy=0.9,
                  replace_target_iter=100, memory_size=2000,
                  e_greedy_increment=0.008)

total_steps = 0

for i_episode in range(100):

    observation = env.reset()
    ep_r = 0
    while True:
        env.render()

        action = RL.choose_action(observation)

        next_observation, reward, done, info = env.step(action)

        # x ==> 车的水平位移, r1 是车越偏离中心, 分越少
        # theta ==> 是棒子离垂直的角度, 角度越大越不垂直, r2 是棒越垂直分越高
        x, x_dot, theta, theta_dot = next_observation
        r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8
        r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5
        reward = r1 + r2    # 既考虑位置又考虑角度

        RL.store_transition(observation, action, reward, next_observation)

        if total_steps > 1000:
            RL.learn()

        ep_r += reward

        if done:
            print('episode:', i_episode,
                  'ep_r:', round(ep_r, 2),
                  'epsilon:', round(RL.epsilon, 2))
            break

        observation = next_observation
        total_steps += 1

# output cost
RL.plot_cost()
