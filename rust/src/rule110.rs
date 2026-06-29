fn main() {
    let width: usize = 5_000;
    let generations: usize = 20_000;
    let rule: [u8; 8] = [0, 1, 1, 1, 0, 1, 1, 0];

    let mut current: Vec<u8> = vec![0; width];
    let mut next: Vec<u8> = vec![0; width];
    current[width - 1] = 1;

    for _ in 0..generations {
        for i in 0..width {
            let left = if i > 0 { current[i - 1] } else { 0 };
            let center = current[i];
            let right = if i < width - 1 { current[i + 1] } else { 0 };
            let index = (left * 4 + center * 2 + right) as usize;
            next[i] = rule[index];
        }
        std::mem::swap(&mut current, &mut next);
    }

    let count: u64 = current.iter().map(|&x| x as u64).sum();
    println!("Population: {}", count);
}
