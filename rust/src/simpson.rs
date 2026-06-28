fn simpson(n: i64) -> f64 {
    let h = 1.0 / n as f64;
    let mut s = 4.0 / (1.0 + 0.0 * 0.0) + 4.0 / (1.0 + 1.0 * 1.0);
    for i in 1..n {
        let x = i as f64 * h;
        if i % 2 == 0 {
            s += 2.0 * 4.0 / (1.0 + x * x);
        } else {
            s += 4.0 * 4.0 / (1.0 + x * x);
        }
    }
    s * h / 3.0
}

fn main() {
    let n = 100_000_000;
    let pi_est = simpson(n);
    println!("Pi ≈ {:.10}", pi_est);
}
