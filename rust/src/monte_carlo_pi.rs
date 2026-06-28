use rand::Rng;

fn monte_carlo_pi(n: i64) -> f64 {
    let mut rng = rand::thread_rng();
    let mut count: i64 = 0;
    for _ in 0..n {
        let x: f64 = rng.gen();
        let y: f64 = rng.gen();
        if x * x + y * y <= 1.0 {
            count += 1;
        }
    }
    4.0 * count as f64 / n as f64
}

fn main() {
    let n = 10_000_000;
    let pi_est = monte_carlo_pi(n);
    println!("Pi ≈ {:.10}", pi_est);
}
