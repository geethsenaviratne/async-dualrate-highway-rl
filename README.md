# Asynchronous Dual-Rate Hierarchical Policy for Highway Driving

SE4012 research project. Slow planner (2 Hz) + fast bounded residual SAC controller (100 Hz),
evaluated on NGSIM / highD hazard scenarios in highway-env.

## Setup

```bash
# Python 3.10–3.12 recommended
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install torch first, matching your machine (see pytorch.org for the exact command)
pip install torch
pip install -r requirements.txt

python scripts/check_env.py        # should end with "All checks finished."
```

Initialise git and push to a **private** GitHub repo:

```bash
git init && git add . && git commit -m "Week 1: project skeleton"
```

## Week 1 plan

| Day | Build | Study |
|---|---|---|
| 1 | Create the venv, install packages, run `scripts/check_env.py`. Push the repo to GitHub. | — |
| 1 | **Submit the highD request** (text ready in `docs/dataset_access.md`). Start the NGSIM download. | — |
| 2 | Run `study/week1_bicycle_model.py`, open the plot in `results/week1/`. | Rajamani ch. 2.1–2.2 (kinematic model). Notes sections 1. |
| 3 | Change `L_F`, `L_R`, `MU` and lane-change durations in the script; see what changes. | Polack et al. 2017. Notes section 4. |
| 4 | Run `check_env.py` part 4 again and read `highway_env/vehicle/dynamics.py`. | Rajamani ch. 2.3+ (dynamic model, tire slip). Notes section 2. |
| 5 | — | Friction circle and rollover (SSF). Notes section 3. |
| 6 | `python study/week1_sac_warmup.py pendulum`, then `highway`. Look at TensorBoard. | Spinning Up: SAC page (first read only). |
| 7 | Tidy notes, fill in section 5, write a short summary for your supervisor. | — |

**Week 1 is done when:**
- [ ] `check_env.py` passes on your machine
- [ ] highD request submitted, NGSIM downloading or downloaded
- [ ] Bicycle model script runs and you can explain every equation in it
- [ ] SAC reaches better than about −300 on Pendulum
- [ ] `notes/week1_study_notes.md` filled in, including the RQ2 decision

## Layout

```
data/        raw/ and processed/ datasets (git-ignored)
pipeline/    extract.py, upsample.py, harmonise.py        (weeks 3–6)
sim/         dataset_vehicle.py, ego_dynamics.py, envs.py (weeks 7–9)
control/     nominal_tracker.py, planner.py, fusion.py    (weeks 10–13)
training/    train_sac.py, configs/                       (weeks 14–16)
runtime/     async_runner.py                              (weeks 17–18)
eval/        metrics.py, run_benchmark.py                 (weeks 9, 21–22)
scripts/     one-off tools (check_env.py)
study/       learning exercises
notes/       weekly study notes
docs/        dataset access, supervisor updates
results/     plots and tables
```
