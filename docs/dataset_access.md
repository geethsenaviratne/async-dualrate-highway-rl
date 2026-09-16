# Dataset access (Week 1)

## highD (do this first, approval takes time)

Apply at https://www.highd-dataset.com/ (free non-commercial research licence).
The form asks for your full name, official university address, institution,
project type (tick **University Thesis**), and a description. Access is only
granted if the description is complete, so be specific.

**Suggested description (edit the details to match you):**

> I am a final-year undergraduate student in the BSc (Hons) in Computer Science
> programme at the Sri Lanka Institute of Information Technology (SLIIT), working
> on my research project (module SE4012) under the supervision of [supervisor name].
> My project studies an asynchronous dual-rate control architecture for
> autonomous highway driving, where a slow high-level planner and a fast
> reinforcement learning controller run at different rates on low-cost edge
> hardware.
>
> I would like to use the highD dataset to extract safety-critical scenarios
> (hard-braking events and lane cut-ins with low time-to-collision), and replay
> those human trajectories as background traffic in the open-source highway-env
> simulator. The data will be used only to train and evaluate my own control
> algorithms in simulation for my university thesis and any resulting academic
> publication. I will not share the dataset or any modified copy with anyone.

Use your university email address when applying.

Once approved: put the files in `data/raw/highd/` and clone the official tools:
`git clone https://github.com/RobertKrajewski/highD-dataset`

## NGSIM (free, no approval)

Search for "Next Generation Simulation (NGSIM) Vehicle Trajectories" on
https://data.transportation.gov and download the US-101 and I-80 data.
The full CSV is several GB. You can filter by `Location` on the portal before
downloading to keep it small.

Put the files in `data/raw/ngsim/`.

Remember while reading the data:
- Units are **feet** and feet/second.
- Positions are noisy; plan to smooth before computing acceleration.
- `Local_Y` is the longitudinal position along the road.

## Licence reminder

highD's terms forbid sharing the dataset or modified versions of it.
That is why `data/` is in `.gitignore`. Never push it to GitHub, even to a private repo
that others can access.
