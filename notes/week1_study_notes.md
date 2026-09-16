# Week 1 study notes

Fill these in as you read. Short answers in your own words are enough.
These notes become the "Background" chapter of your thesis later.

## 1. Kinematic bicycle model (Rajamani ch. 2, sections 2.1–2.3)

- What does the model assume about the tires? (Hint: what happens to slip at the wheels?)
- Write the four equations for x, y, ψ and v, plus the equation for β.
- What is β physically? How is it different from a *tire* slip angle?
- Why is the model only trustworthy at low lateral acceleration?
- From `study/week1_bicycle_model.py`: why does the steering needed for a lane change
  get smaller as speed increases? What does that mean for a fixed ±5% steering residual?

## 2. Dynamic bicycle model (Rajamani ch. 2, section 2.3 onwards)

- What two extra states does it add? (lateral velocity, yaw rate)
- Write the front and rear tire slip angle equations.
- What is cornering stiffness, and what happens to tire force when slip gets large?
  (linear model vs saturation / Pacejka)
- highway-env's `BicycleVehicle` (turned on with `dynamical=True`) uses this model with a
  **linear** tire and toy parameters. List what you would need to change to make it realistic.

## 3. Friction circle and rollover

- Friction circle: how are longitudinal and lateral tire forces limited together?
- Why can't a car brake at full force AND swerve at full force at the same time?
- Rollover threshold: static stability factor SSF = track width / (2 × CoG height).
  Compute it for a sedan (track 1.55 m, CoG 0.55 m) and an SUV (track 1.6 m, CoG 0.75 m).
- Given the friction limit, can a passenger car on dry asphalt roll over from steering alone?
  (This affects whether "rollover" should stay in RQ2.)

## 4. Polack et al. (2017)

- What limit on lateral acceleration do they propose for the kinematic model?
- What does that mean for evasive manoeuvres in your hazard scenarios?

## 5. Decision to take to your supervisor

Pick one and write why:
- [ ] Option A: realistic dynamic bicycle model + tire model for the ego car (answers RQ2 directly)
- [ ] Option B: keep the kinematic model and reframe RQ2 around lateral acceleration vs μg
- [ ] Option C: other

## 6. Questions I still have

-
