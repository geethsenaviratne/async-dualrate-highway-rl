"""
Week 1 study exercise - the kinematic bicycle model, written from scratch.

Run:  python study/week1_bicycle_model.py

Read first: Rajamani, "Vehicle Dynamics and Control", ch. 2 (kinematic model)
            Polack et al. 2017, "The kinematic bicycle model: a consistent
            model for planning feasible trajectories for autonomous vehicles?"

Equations (centre-of-gravity reference, rear-wheel steering = 0):
    beta     = arctan( l_r / (l_f + l_r) * tan(delta) )   # sideslip angle
    x_dot    = v * cos(psi + beta)
    y_dot    = v * sin(psi + beta)
    psi_dot  = v / l_r * sin(beta)                       # yaw rate
    v_dot    = a

What this script shows
A) The 500 ms "blind spot" distance at highway speeds.
B) A normal (4 s) and an evasive (1.5 s) lane change at 100/130/150 km/h,
   integrated at 100 Hz (dt = 10 ms, your SAC rate).
C) Peak lateral acceleration compared with ~0.5 * mu * g, the rough limit where
   Polack et al. say the kinematic model stops being trustworthy.
   -> This is why RQ2 (tire slip / rollover) needs more than a kinematic model.
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- parameters
L_F, L_R = 1.2, 1.6        # CoG to front / rear axle [m] (typical sedan)
DT = 0.01                  # 100 Hz
G, MU = 9.81, 0.9          # gravity, dry-asphalt friction coefficient
LANE_WIDTH = 3.5           # [m]
VLA_LATENCY = 0.5          # [s]
OUT = Path(__file__).resolve().parents[1] / "results" / "week1"


def kinematic_bicycle(state, delta, a):
    """state = [x, y, psi, v] -> state derivative."""
    x, y, psi, v = state
    beta = np.arctan(L_R / (L_F + L_R) * np.tan(delta))
    return np.array([
        v * np.cos(psi + beta),
        v * np.sin(psi + beta),
        v / L_R * np.sin(beta),
        a,
    ])


def rk4_step(state, delta, a, dt=DT):
    """4th-order Runge-Kutta, same integrator highway-env uses for dynamics."""
    k1 = kinematic_bicycle(state, delta, a)
    k2 = kinematic_bicycle(state + dt / 2 * k1, delta, a)
    k3 = kinematic_bicycle(state + dt / 2 * k2, delta, a)
    k4 = kinematic_bicycle(state + dt * k3, delta, a)
    return state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate_lane_change(speed_kmh, duration, amplitude, extra=1.0):
    """One full sine period of steering -> heading returns to ~0, car shifts sideways."""
    v0 = speed_kmh / 3.6
    state = np.array([0.0, 0.0, 0.0, v0])
    n = int((duration + extra) / DT)
    log = {"t": [], "x": [], "y": [], "psi": [], "delta": [], "ay": []}
    for k in range(n):
        t = k * DT
        delta = amplitude * np.sin(2 * np.pi * t / duration) if t < duration else 0.0
        d = kinematic_bicycle(state, delta, 0.0)
        # lateral acceleration ~ v * (yaw rate + d(beta)/dt); v * yaw rate is the main term
        log["t"].append(t); log["x"].append(state[0]); log["y"].append(state[1])
        log["psi"].append(state[2]); log["delta"].append(delta); log["ay"].append(state[3] * d[2])
        state = rk4_step(state, delta, 0.0)
    return {k: np.array(v) for k, v in log.items()}


def find_amplitude(speed_kmh, duration, target=LANE_WIDTH):
    """Bisection: steering amplitude that gives exactly one lane of lateral shift."""
    # Grow the upper bound slowly: too large an amplitude makes the car turn
    # around, and then "more steering" no longer means "more lateral shift".
    lo, hi = 0.0, 1e-3
    while simulate_lane_change(speed_kmh, duration, hi)["y"][-1] < target:
        lo, hi = hi, hi * 1.5
    for _ in range(40):
        mid = (lo + hi) / 2
        y_end = simulate_lane_change(speed_kmh, duration, mid)["y"][-1]
        lo, hi = (mid, hi) if y_end < target else (lo, mid)
    return (lo + hi) / 2


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("A) Distance travelled during one 500 ms VLA update")
    for kmh in (60, 100, 130, 150):
        print(f"   {kmh:>3} km/h -> {kmh / 3.6 * VLA_LATENCY:5.1f} m without a new plan")

    limit = 0.5 * MU * G
    print(f"\nB/C) Lane changes (kinematic-model validity limit ~0.5*mu*g = {limit:.1f} m/s^2)")
    print(f"   {'speed':>9} {'type':>8} {'steer amp':>10} {'peak a_y':>10} {'valid?':>8}")

    fig, axes = plt.subplots(3, 1, figsize=(9, 10))
    for kmh in (100, 130, 150):
        for duration, label in ((4.0, "normal"), (1.5, "evasive")):
            amp = find_amplitude(kmh, duration)
            log = simulate_lane_change(kmh, duration, amp)
            peak = np.max(np.abs(log["ay"]))
            ok = "yes" if peak <= limit else "NO"
            print(f"   {kmh:>5} km/h {label:>8} {np.degrees(amp):8.2f} deg "
                  f"{peak:7.2f} m/s2 {ok:>8}")
            name = f"{kmh} km/h, {label}"
            style = "-" if label == "normal" else "--"
            axes[0].plot(log["x"], log["y"], style, label=name)
            axes[1].plot(log["t"], np.degrees(log["delta"]), style, label=name)
            axes[2].plot(log["t"], log["ay"], style, label=name)

    axes[0].set(xlabel="x [m]", ylabel="y [m]", title="Path of a one-lane change")
    axes[1].set(xlabel="time [s]", ylabel="steering [deg]", title="Steering input")
    axes[2].axhline(limit, color="k", lw=0.8); axes[2].axhline(-limit, color="k", lw=0.8)
    axes[2].set(xlabel="time [s]", ylabel="a_y [m/s^2]",
                title="Lateral acceleration (curves overlap: depends on duration, not speed; black = model limit)")
    for ax in axes:
        ax.grid(alpha=0.3)
    axes[0].legend(fontsize=8, ncol=2)
    fig.tight_layout()
    path = OUT / "bicycle_lane_changes.png"
    fig.savefig(path, dpi=130)
    print(f"\nPlot saved to {path}")

    print("\nThings to notice and write in your notes:")
    print(" - Steering needed for the same lane change gets SMALLER as speed goes up.")
    print("   So a fixed +/-5% steering residual means very different things at 60 vs 150 km/h.")
    print(" - Evasive lane changes exceed the kinematic model's valid range,")
    print("   which is exactly the regime your hazard scenarios live in.")
    print(f" - A 1.5 s lane change needs ~{2*np.pi*LANE_WIDTH/1.5**2:.1f} m/s^2 at ANY speed, above")
    print(f"   mu*g = {MU*G:.1f} m/s^2: real tires can't do it, but the kinematic model happily will.")


if __name__ == "__main__":
    main()
