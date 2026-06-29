import math

import numpy as np
from numba import njit

SOLAR_MASS = 4 * math.pi * math.pi
DAYS_PER_YEAR = 365.24


def make_bodies():
    bodies = np.array(
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS],
            [
                4.84143144246472090e00,
                -1.16032004402742839e00,
                -1.03622044471123109e-01,
                1.66007664274403694e-03 * DAYS_PER_YEAR,
                7.69901118419740425e-03 * DAYS_PER_YEAR,
                -6.90460016972063023e-05 * DAYS_PER_YEAR,
                9.54791938424326609e-04 * SOLAR_MASS,
            ],
            [
                8.34336671824457987e00,
                4.12479856412430479e00,
                -4.03523417114321381e-01,
                -2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR,
                2.85885980666130812e-04 * SOLAR_MASS,
            ],
            [
                1.28943695621391310e01,
                -1.51111514016986312e01,
                -2.23307578892655734e-01,
                2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR,
                4.36624404335156298e-05 * SOLAR_MASS,
            ],
            [
                1.53796971148509165e01,
                -2.59193146099879641e01,
                1.79258772950371181e-01,
                2.68067772490389322e-03 * DAYS_PER_YEAR,
                1.62824170038242295e-03 * DAYS_PER_YEAR,
                -9.51592254519715870e-05 * DAYS_PER_YEAR,
                5.15138902046611451e-05 * SOLAR_MASS,
            ],
        ]
    )
    px = np.sum(bodies[:, 3] * bodies[:, 6])
    py = np.sum(bodies[:, 4] * bodies[:, 6])
    pz = np.sum(bodies[:, 5] * bodies[:, 6])
    bodies[0, 3] = -px / SOLAR_MASS
    bodies[0, 4] = -py / SOLAR_MASS
    bodies[0, 5] = -pz / SOLAR_MASS
    return bodies


@njit
def advance(bodies, dt):
    n = bodies.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            dx = bodies[i, 0] - bodies[j, 0]
            dy = bodies[i, 1] - bodies[j, 1]
            dz = bodies[i, 2] - bodies[j, 2]
            dsq = dx * dx + dy * dy + dz * dz
            dist = math.sqrt(dsq)
            mag = dt / (dsq * dist)
            bodies[i, 3] -= dx * bodies[j, 6] * mag
            bodies[i, 4] -= dy * bodies[j, 6] * mag
            bodies[i, 5] -= dz * bodies[j, 6] * mag
            bodies[j, 3] += dx * bodies[i, 6] * mag
            bodies[j, 4] += dy * bodies[i, 6] * mag
            bodies[j, 5] += dz * bodies[i, 6] * mag
    for i in range(n):
        bodies[i, 0] += dt * bodies[i, 3]
        bodies[i, 1] += dt * bodies[i, 4]
        bodies[i, 2] += dt * bodies[i, 5]


@njit
def energy(bodies):
    e = 0.0
    n = bodies.shape[0]
    for i in range(n):
        e += (
            0.5
            * bodies[i, 6]
            * (bodies[i, 3] ** 2 + bodies[i, 4] ** 2 + bodies[i, 5] ** 2)
        )
        for j in range(i + 1, n):
            dx = bodies[i, 0] - bodies[j, 0]
            dy = bodies[i, 1] - bodies[j, 1]
            dz = bodies[i, 2] - bodies[j, 2]
            e -= bodies[i, 6] * bodies[j, 6] / math.sqrt(dx**2 + dy**2 + dz**2)
    return e


@njit
def run(bodies, n, dt):
    for _ in range(n):
        advance(bodies, dt)


bodies_warmup = make_bodies()
advance(bodies_warmup, 0.01)
energy(bodies_warmup)
run(bodies_warmup, 1, 0.01)

n = 1_000_000
bodies = make_bodies()
print(f"{energy(bodies):.9f}")
run(bodies, n, 0.01)
print(f"{energy(bodies):.9f}")
