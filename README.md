bench-julia-python

Julia, Python (pure / Numba), C++, Rust の処理速度比較ベンチマーク。

## 実行環境

- macOS (Apple Silicon, osx-arm64)
- 環境構築: pixi
- 時間計測: hyperfine

## ベンチマーク題材

| 題材 | 概要 | 特性 |
|---|---|---|
| モンテカルロ法 | 乱数 10,000,000 点で円周率を推定 | ループ性能、乱数生成 |
| N体問題 | 太陽系5体の重力シミュレーション (5,000,000ステップ) | 浮動小数点演算、メモリアクセス |
| シンプソン法 | 数値積分で円周率を算出 (100,000,000分割) | 数学関数評価、ループ |
| Rule 110 | 1次元セルオートマトン (幅10,000 x 50,000世代) | 条件分岐、状態遷移 |

## 結果

### モンテカルロ法 (円周率推定, N=10,000,000)

| 言語 | 平均実行時間 | 最速比 |
|---|---|---|
| C++ | 37.6 ms | 1.00x |
| Julia | 115.5 ms | 3.07x |
| Rust | 118.2 ms | 3.14x |
| Python (Numba) | 343.3 ms | 9.13x |
| Python | 592.0 ms | 15.74x |

### N体問題 (5体, 5,000,000ステップ)

| 言語 | 平均実行時間 | 最速比 |
|---|---|---|
| Rust | 159.7 ms | 1.00x |
| C++ | 191.9 ms | 1.20x |
| Julia | 507.2 ms | 3.17x |
| Python (Numba) | 543.1 ms | 3.40x |
| Python | 14,647 ms | 91.69x |

### シンプソン法 (数値積分, N=100,000,000)

| 言語 | 平均実行時間 | 最速比 |
|---|---|---|
| C++ | 60.2 ms | 1.00x |
| Rust | 60.5 ms | 1.00x |
| Julia | 173.0 ms | 2.87x |
| Python (Numba) | 312.5 ms | 5.19x |
| Python | 4,482 ms | 74.45x |

### Rule 110 (幅10,000 x 50,000世代)

| 言語 | 平均実行時間 | 最速比 |
|---|---|---|
| C++ | 185.1 ms | 1.00x |
| Rust | 251.8 ms | 1.36x |
| Julia | 393.0 ms | 2.12x |
| Python (Numba) | 535.8 ms | 2.89x |
| Python | 29,373 ms | 158.69x |

## 考察

### C++ / Rust

全ベンチマークで最速グループ。シンプソン法ではほぼ同速だが、モンテカルロ法ではC++が優位（乱数生成器の差が影響）、N体問題ではRustが優位。条件分岐主体のRule 110ではC++がRustを上回った。

### Julia

JIT起動コストを含めても C++/Rust の 2-3倍 程度の実行時間に収まる。事前コンパイル不要で高い性能を実現しており、数値計算のプロトタイピングに適している。

### Python (Numba)

JITコンパイルのオーバーヘッドを含めて C++/Rust の 3-9倍 程度。純粋Pythonに `@njit` を付与するだけで大幅に高速化できる手軽さが利点。ただしJulia と比較すると同等かやや遅い。

### Python (純粋)

C++/Rust と比較して 16-159倍 遅い。ベンチマークの計算特性によって差が大きく変動する。特に条件分岐と状態遷移が主体の Rule 110 では最大の差（約159倍）が出た。

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
    - nbody.jl
    - simpson.jl
    - rule110.jl
- python/
    - monte_carlo_pi.py
    - monte_carlo_pi_numba.py
    - nbody.py
    - nbody_numba.py
    - simpson.py
    - simpson_numba.py
    - rule110.py
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
```
