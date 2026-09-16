"""
Week 1 (end of week) - first contact with Soft Actor-Critic.

Run:  python study/week1_sac_warmup.py pendulum     # ~5-15 min on a laptop CPU
      python study/week1_sac_warmup.py highway      # smoke test only
      tensorboard --logdir runs                     # watch the learning curves

Read first: OpenAI Spinning Up -> "Soft Actor-Critic" page.

Pendulum-v1 is the classic "does my SAC work?" test: the reward should climb
from about -1200 to about -200 within ~20k steps. If it does, your install and
your understanding of the training loop are fine.

The highway run is NOT expected to drive well. It only proves SAC can talk to
highway-env with continuous [accel, steer] actions at 100 Hz.
"""
import sys

import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.evaluation import evaluate_policy


def pendulum():
    env = gym.make("Pendulum-v1")
    model = SAC("MlpPolicy", env, learning_starts=1000, verbose=1,
                tensorboard_log="runs/", seed=0)
    model.learn(total_timesteps=20_000, tb_log_name="sac_pendulum")
    mean, std = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"\nPendulum mean reward over 10 episodes: {mean:.0f} +/- {std:.0f}")
    print("Good result: better than about -300.")
    model.save("runs/sac_pendulum")


def highway():
    import highway_env
    gym.register_envs(highway_env)
    env = gym.make("highway-v0", config={
        "action": {"type": "ContinuousAction"},
        "observation": {"type": "Kinematics", "vehicles_count": 5,
                        "features": ["presence", "x", "y", "vx", "vy"],
                        "absolute": False, "normalize": True},
        "simulation_frequency": 100,
        "policy_frequency": 100,
        "vehicles_count": 20,      # fewer cars = faster simulation
        "duration": 20,
    })
    model = SAC("MlpPolicy", env, learning_starts=1000, verbose=1,
                tensorboard_log="runs/", seed=0)
    model.learn(total_timesteps=20_000, tb_log_name="sac_highway_smoke")
    model.save("runs/sac_highway_smoke")
    print("\nSmoke test finished. Poor driving is expected at this stage.")


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "pendulum"
    {"pendulum": pendulum, "highway": highway}[task]()
