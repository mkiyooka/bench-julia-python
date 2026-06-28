const SOLAR_MASS = 4π^2
const DAYS_PER_YEAR = 365.24

mutable struct Body
    x::Float64; y::Float64; z::Float64
    vx::Float64; vy::Float64; vz::Float64
    mass::Float64
end

function make_bodies()
    sun = Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS)
    jupiter = Body(
        4.84143144246472090e+00, -1.16032004402742839e+00, -1.03622044471123109e-01,
        1.66007664274403694e-03 * DAYS_PER_YEAR, 7.69901118419740425e-03 * DAYS_PER_YEAR,
        -6.90460016972063023e-05 * DAYS_PER_YEAR, 9.54791938424326609e-04 * SOLAR_MASS)
    saturn = Body(
        8.34336671824457987e+00, 4.12479856412430479e+00, -4.03523417114321381e-01,
        -2.76742510726862411e-03 * DAYS_PER_YEAR, 4.99852801234917238e-03 * DAYS_PER_YEAR,
        2.30417297573763929e-05 * DAYS_PER_YEAR, 2.85885980666130812e-04 * SOLAR_MASS)
    uranus = Body(
        1.28943695621391310e+01, -1.51111514016986312e+01, -2.23307578892655734e-01,
        2.96460137564761618e-03 * DAYS_PER_YEAR, 2.37847173959480950e-03 * DAYS_PER_YEAR,
        -2.96589568540237556e-05 * DAYS_PER_YEAR, 4.36624404335156298e-05 * SOLAR_MASS)
    neptune = Body(
        1.53796971148509165e+01, -2.59193146099879641e+01, 1.79258772950371181e-01,
        2.68067772490389322e-03 * DAYS_PER_YEAR, 1.62824170038242295e-03 * DAYS_PER_YEAR,
        -9.51592254519715870e-05 * DAYS_PER_YEAR, 5.15138902046611451e-05 * SOLAR_MASS)
    bodies = [sun, jupiter, saturn, uranus, neptune]
    px = 0.0; py = 0.0; pz = 0.0
    for b in bodies
        px += b.vx * b.mass
        py += b.vy * b.mass
        pz += b.vz * b.mass
    end
    sun.vx = -px / SOLAR_MASS
    sun.vy = -py / SOLAR_MASS
    sun.vz = -pz / SOLAR_MASS
    return bodies
end

function advance!(bodies, dt)
    n = length(bodies)
    @inbounds for i in 1:n
        bi = bodies[i]
        for j in (i+1):n
            bj = bodies[j]
            dx = bi.x - bj.x
            dy = bi.y - bj.y
            dz = bi.z - bj.z
            dsq = dx * dx + dy * dy + dz * dz
            dist = sqrt(dsq)
            mag = dt / (dsq * dist)
            bi.vx -= dx * bj.mass * mag
            bi.vy -= dy * bj.mass * mag
            bi.vz -= dz * bj.mass * mag
            bj.vx += dx * bi.mass * mag
            bj.vy += dy * bi.mass * mag
            bj.vz += dz * bi.mass * mag
        end
    end
    @inbounds for b in bodies
        b.x += dt * b.vx
        b.y += dt * b.vy
        b.z += dt * b.vz
    end
end

function energy(bodies)
    e = 0.0
    n = length(bodies)
    @inbounds for i in 1:n
        bi = bodies[i]
        e += 0.5 * bi.mass * (bi.vx^2 + bi.vy^2 + bi.vz^2)
        for j in (i+1):n
            bj = bodies[j]
            dx = bi.x - bj.x
            dy = bi.y - bj.y
            dz = bi.z - bj.z
            e -= bi.mass * bj.mass / sqrt(dx^2 + dy^2 + dz^2)
        end
    end
    return e
end

function main()
    n = 5_000_000
    bodies = make_bodies()
    println(energy(bodies))
    for _ in 1:n
        advance!(bodies, 0.01)
    end
    println(energy(bodies))
end

main()
