"""
Week 1 - Environment check.

Run:  python scripts/check_env.py

What it verifies
1. All packages import and prints their versions.
2. highway-env runs with CONTINUOUS actions [acceleration, steering] at 100 Hz.
3. How fast the simulator is on your machine (real-time factor).
   RTF > 1  -> faster than real time (good for training)
   RTF < 1  -> slower than real time (training at 100 Hz will be slow)
4. The hidden `dynamical=True` option, which swaps the kinematic car for a
   dynamic bicycle model with front/rear tire slip angles (relevant to RQ2).
"""
import time
from importlib.metadata import version, PackageNotFoundError

import numpy as np


def print_versions():
    print("=" * 60)
    print("1) Package versions")
    for pkg in ["gymnasium", "highway-env", "stable-baselines3", "torch",
                "numpy", "pandas", "scipy", "matplotlib"]:
        try:
            print(f"   {pkg:<18} {version(pkg)}")
        except PackageNotFoundError:
            print(f"   {pkg:<18} NOT INSTALLED")
    try:
        import torch
        print(f"   CUDA available:    {torch.cuda.is_available()}")
    except Exception as e:  # missing or broken torch install
        print(f"   torch import failed: {type(e).__name__} - reinstall torch")


def make_env(vehicles_count=50, dynamical=False):
    import gymnasium as gym
    import highway_env
    gym.register_envs(highway_env)

    config = {
        "action": {"type": "ContinuousAction", "dynamical": dynamical},
        "observation": {
            "type": "Kinematics",
            "vehicles_count": 5,
            "features": ["presence", "x", "y", "vx", "vy", "heading"],
            "absolute": False,     # ego-relative, like your pipeline
            "normalize": False,    # raw metres and m/s, easier to read
        },
        "simulation_frequency": 100,   # physics step = 10 ms
        "policy_frequency": 100,       # one action every 10 ms (your SAC rate)
        "vehicles_count": vehicles_count,
        "duration": 10,                # seconds
    }
    return gym.make("highway-v0", config=config)


def run_episode(env, seconds=5.0):
    obs, info = env.reset(seed=0)
    steps = int(seconds * 100)
    t0 = time.perf_counter()
    for _ in range(steps):
        action = np.array([0.0, 0.0], dtype=np.float32)  # keep speed, go straight
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            break
    wall = time.perf_counter() - t0
    return obs, info, seconds / wall


def check_highway_env():
    print("=" * 60)
    print("2) highway-env with continuous actions at 100 Hz")
    env = make_env()
    print(f"   action space:      {env.action_space}  -> [accel, steer], scaled to [-1, 1]")
    print(f"   observation shape: {env.observation_space.shape}  (5 vehicles x 6 features)")
    obs, info, rtf = run_episode(env)
    print("   observation [presence, x, y, vx, vy, heading]")
    print("   row 0 = ego (absolute values), rows 1+ = other cars relative to ego:")
    for row in obs[:3]:
        print("   ", np.array2string(row, precision=2, suppress_small=True))
    print(f"   info: speed={info['speed']:.1f} m/s, crashed={info['crashed']}")
    env.close()

    print("=" * 60)
    print("3) Simulator speed (real-time factor, 5 simulated seconds)")
    for n in (50, 20, 5):
        env = make_env(vehicles_count=n)
        _, _, rtf = run_episode(env)
        env.close()
        flag = "OK" if rtf >= 1 else "slower than real time"
        print(f"   {n:>2} vehicles: RTF = {rtf:5.2f}  ({flag})")


def check_dynamic_model():
    print("=" * 60)
    print("4) Dynamic bicycle model (dynamical=True)")
    env = make_env(vehicles_count=5, dynamical=True)
    env.reset(seed=0)
    ego = env.unwrapped.vehicle
    print(f"   ego class: {type(ego).__name__}")
    print(f"   built-in params: MASS={ego.MASS}, INERTIA_Z={ego.INERTIA_Z:.2f}, "
          f"cornering stiffness front/rear={ego.FRICTION_FRONT}/{ego.FRICTION_REAR}")
    print("   NOTE: these are toy values (mass = 1). Realistic values are roughly")
    print("         mass 1500 kg, Iz 2500 kg m^2, cornering stiffness ~80 000 N/rad.")
    # A short steering pulse, then look at the lateral states
    for k in range(100):
        steer = 0.05 if k < 50 else 0.0
        env.step(np.array([0.0, steer], dtype=np.float32))
    state = ego.state.flatten()  # [x, y, heading, speed, lateral_speed, yaw_rate]
    print(f"   after 1 s steering pulse: lateral speed={state[4]:.3f} m/s, "
          f"yaw rate={state[5]:.3f} rad/s")
    env.close()


if __name__ == "__main__":
    print_versions()
    check_highway_env()
    check_dynamic_model()
    print("=" * 60)
    print("All checks finished.")
