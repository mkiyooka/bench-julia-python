bench-julia-python

Julia, Python (pure / NumPy / Numba), C++, Rust の処理速度比較ベンチマーク。

## 実行環境

|                | macOS                  | Linux                   |
| -------------- | ---------------------- | ----------------------- |
| CPU            | Apple Silicon (M4 Max) | AMD EPYC-Milan (4 vCPU) |
| アーキテクチャ | osx-arm64              | linux-64                |
| 環境構築       | pixi                   | pixi                    |
| 時間計測       | hyperfine              | hyperfine               |

## ベンチマーク題材

| 題材           | 概要                                                | 特性                           |
| -------------- | --------------------------------------------------- | ------------------------------ |
| モンテカルロ法 | 乱数 10,000,000 点で円周率を推定                    | ループ性能、乱数生成           |
| N体問題        | 太陽系5体の重力シミュレーション (1,000,000ステップ) | 浮動小数点演算、メモリアクセス |
| シンプソン法   | 数値積分で円周率を算出 (50,000,000分割)             | 数学関数評価、ループ           |
| Rule 110       | 1次元セルオートマトン (幅5,000 x 20,000世代)        | 条件分岐、状態遷移             |

## 結果

### モンテカルロ法 (円周率推定, N=10,000,000)

| 実装               | macOS 平均 | 最速比 | Linux 平均 | 最速比 |
| ------------------ | ---------- | ------ | ---------- | ------ |
| Rust               | 119.7 ms   | 3.21x  | 90.7 ms    | 1.00x  |
| C++                | 37.3 ms    | 1.00x  | 178.7 ms   | 1.97x  |
| Julia (ループ)     | 123.5 ms   | 3.31x  | 386.5 ms   | 4.26x  |
| Python (NumPy)     | 137.1 ms   | 3.67x  | 795.2 ms   | 8.76x  |
| Julia (ベクトル化) | 287.6 ms   | 7.71x  | 1,223 ms   | 13.48x |
| Python (Numba)     | 297.8 ms   | 7.98x  | 1,811 ms   | 19.96x |
| Python             | 565.4 ms   | 15.16x | 4,429 ms   | 48.82x |

### N体問題 (5体, 1,000,000ステップ)

| 実装           | macOS 平均 | 最速比 | Linux 平均 | 最速比  |
| -------------- | ---------- | ------ | ---------- | ------- |
| Rust           | 31.4 ms    | 1.00x  | 56.8 ms    | 1.00x   |
| C++            | 37.2 ms    | 1.18x  | 83.3 ms    | 1.47x   |
| Julia          | 223.5 ms   | 7.12x  | 571.5 ms   | 10.06x  |
| Python (Numba) | 397.1 ms   | 12.65x | 1,639 ms   | 28.87x  |
| Python         | 3,026 ms   | 96.37x | 23,750 ms  | 418.28x |

### シンプソン法 (数値積分, N=50,000,000)

| 実装               | macOS 平均 | 最速比 | Linux 平均 | 最速比  |
| ------------------ | ---------- | ------ | ---------- | ------- |
| C++                | 30.9 ms    | 1.00x  | 76.5 ms    | 1.00x   |
| Rust               | 31.3 ms    | 1.01x  | 79.0 ms    | 1.03x   |
| Julia (ループ)     | 138.0 ms   | 4.47x  | 448.2 ms   | 5.86x   |
| Python (Numba)     | 274.2 ms   | 8.87x  | 893.2 ms   | 11.67x  |
| Python (NumPy)     | 559.4 ms   | 18.10x | 2,240 ms   | 29.27x  |
| Julia (ベクトル化) | 691.6 ms   | 22.38x | 2,355 ms   | 30.78x  |
| Python             | 2,277 ms   | 73.69x | 19,612 ms  | 256.29x |

### Rule 110 (幅5,000 x 20,000世代)

| 実装                  | macOS 平均 | 最速比  | Linux 平均 | 最速比  |
| --------------------- | ---------- | ------- | ---------- | ------- |
| C++                   | 38.8 ms    | 1.00x   | 106.2 ms   | 1.00x   |
| Rust                  | 52.0 ms    | 1.34x   | 142.4 ms   | 1.34x   |
| Julia                 | 154.0 ms   | 3.97x   | 477.2 ms   | 4.49x   |
| Python (NumPy)        | 314.1 ms   | 8.10x   | 1,261 ms   | 11.87x  |
| Python (Numba 最適化) | 363.9 ms   | 9.38x   | 1,400 ms   | 13.18x  |
| Python (Numba 最小)   | 376.8 ms   | 9.71x   | 1,458 ms   | 13.73x  |
| Python                | 5,747 ms   | 148.12x | 55,106 ms  | 518.89x |

## 考察

### C++ / Rust

全ベンチマークで最速グループ。シンプソン法ではほぼ同速（差1-3%）だが、モンテカルロ法ではmacOSでC++が優位、LinuxではRustが優位と環境によって逆転する（乱数生成器やコンパイラの差が影響）。N体問題では両環境でRustが優位。

### Julia

ループ版はJIT起動コストを含めてもC++/Rustの3-10倍程度。ベクトル化版（ブロードキャスト `.` 演算子）はモンテカルロ・シンプソンの両方でループ版より遅い。大量の一時配列確保がオーバーヘッドとなるため、Juliaではループを素直に書いた方が速い。

### Python (NumPy)

問題の構造によって効果が大きく異なる。モンテカルロ法では全計算をベクトル演算に置き換えられるためmacOSではC++の3.7倍に迫る性能を実現。Rule 110でも世代ループ内のセル更新をベクトル化でき、Numbaに匹敵する速度。ただしN体問題のように逐次的な相互作用が本質の問題ではベクトル化の恩恵がないため、ベンチマーク対象から除外した。

### Python (Numba)

JITコンパイルのオーバーヘッドを含めてC++/Rustの8-29倍程度。Rule 110ではNumba最小版（`@njit`を付けただけ）と最適化版（関数分離+NumPy配列）の性能差はほぼなく、デコレータ付与だけで十分な高速化が得られることを示している。

### Python (純粋)

C++/Rustと比較して15-519倍遅い。Linux環境ではmacOSよりさらに差が広がる傾向がある。

### 環境間の比較

macOS (Apple M4 Max) はLinux (AMD EPYC-Milan 4 vCPU) と比較して、全ベンチマークで2-3倍高速。M4 Maxの高い単体コア性能が反映されている。ただし相対的な言語間の順位はほぼ一致しており、ベンチマークの妥当性を裏付けている。

## セットアップ

```bash
pixi install
pixi run setup-julia
```

## 使い方

```bash
# 全ベンチマーク実行
pixi run bench

# 個別実行
pixi run bench-monte-carlo
pixi run bench-nbody
pixi run bench-simpson
pixi run bench-rule110
```

## ディレクトリ構成

```text
- julia/
    - monte_carlo_pi.jl
    - monte_carlo_pi_vectorized.jl
    - nbody.jl
    - simpson.jl
    - simpson_vectorized.jl
    - rule110.jl
- python/
    - monte_carlo_pi.py
    - monte_carlo_pi_numpy.py
    - monte_carlo_pi_numba.py
    - nbody.py
    - nbody_numba.py
    - simpson.py
    - simpson_numpy.py
    - simpson_numba.py
    - rule110.py
    - rule110_numpy.py
    - rule110_numba_minimal.py
    - rule110_numba.py
- cpp/
    - CMakeLists.txt
    - src/
        - monte_carlo_pi.cpp
        - nbody.cpp
        - simpson.cpp
        - rule110.cpp
- rust/
    - Cargo.toml
    - src/
        - monte_carlo_pi.rs
        - nbody.rs
        - simpson.rs
        - rule110.rs
- docs/
    - language-comparison.md
```
