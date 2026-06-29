Python版を基準とした各言語の実装比較

## Python -> Numba での変更点

Numba版はPure Python版に対して最小限の変更で高速化を実現している。
以下、4つのベンチマークそれぞれの変更点を示す。

### モンテカルロ法

変更点は2箇所のみ。

- `from numba import njit` のインポート追加
- 関数に `@njit` デコレータを付与
- ウォームアップ呼び出し `monte_carlo_pi(1000)` を追加

関数本体のコードは一切変更なし。`random.random()` もNumba内でそのまま動作する。

### シンプソン法

モンテカルロ法と同じパターン。

- `from numba import njit` のインポート追加
- 関数に `@njit` デコレータを付与
- ウォームアップ呼び出し `simpson(1000)` を追加

関数本体のコードは一切変更なし。

### N体問題

他のベンチマークと異なり、データ構造の変更が必要になる。

- **データ構造の変更**: Pure Python版はリストのリスト(`list[list[float]]`)で各天体を表現するが、Numba版では `numpy.ndarray` (5x7の2次元配列)に変更。Numbaは任意のPythonオブジェクトを扱えないため、NumPy配列への変換が必要。
- **関数の分離**: Pure Python版ではトップレベルに直接ループを書いているが、Numba版ではメインループを `run()` 関数に切り出して `@njit` を付与。
- **3関数に `@njit`**: `advance`, `energy`, `run` の3関数それぞれにデコレータを付与。
- **ウォームアップ**: 3関数すべてを事前に小さい引数で呼び出し、JITコンパイルを完了させる。
- **アクセス方法の変更**: `body[0]` (リストインデックス) から `bodies[i, 0]` (NumPy 2次元インデックス) への書き換え。

このベンチマークではNumba化に際して、単なるデコレータ付与ではなくデータ構造の再設計が求められる。Numbaが効率的に扱える型（NumPyのプリミティブ配列）に合わせる作業が発生する。

### Rule 110

N体問題と同様、配列をNumPyに変更する必要がある。

- **データ構造の変更**: Pure Python版の `list[int]` から `numpy.ndarray` (`dtype=np.int32`) に変更。
- **関数の分離**: 1世代の更新を `step()` 関数に、世代ループ全体を `run()` 関数に切り出し。Pure Python版は1つの関数内に全処理を書いているが、Numba版では内側ループと外側ループを別関数にする設計が有効。
- **ルールテーブルの外部化**: Pure Python版では関数内でルールテーブルを定義しているが、Numba版ではNumPy配列として関数の外で定義し、引数として渡す。
- **ウォームアップ**: 小さいサイズ (幅100, 10世代) で事前呼び出し。

### Numba化のまとめ

| 変更の種類 | モンテカルロ | シンプソン | N体 | Rule 110 |
|---|---|---|---|---|
| `@njit` デコレータ追加 | o | o | o | o |
| ウォームアップ呼び出し | o | o | o | o |
| データ構造の変更 | - | - | o | o |
| 関数の分離・再設計 | - | - | o | o |
| NumPyインポート追加 | - | - | o | o |

スカラー値のみを扱うベンチマーク(モンテカルロ、シンプソン)ではデコレータを付けるだけで済む。一方、コレクション型(リスト、配列)を扱うベンチマーク(N体、Rule 110)ではNumPy配列への変換と関数設計の変更が必要になる。

## Julia / C++ で記述量が増える箇所

JuliaとC++はPythonと比較して、言語の性質上コードが増える箇所がある。

### Julia

Juliaのコードは全体的にPythonと記述量がほぼ同等で、増加する箇所は少ない。

- **型注釈**: 関数引数に `n::Int` のように型を明示する。Pythonのtype hintと同程度だが、Juliaでは性能に直結するため省略しにくい。
- **1-based indexing**: 配列のインデックスが1始まりのため、Rule 110のルールテーブル参照で `rule[index + 1]` とオフセットが必要。
- **`@inbounds` マクロ**: ループ内の配列アクセスで境界チェックを省略するマクロ。パフォーマンスのために付与するが、Pythonにはない記述。N体問題とRule 110で使用。
- **`mutable struct`**: N体問題では`mutable struct Body` を定義する。Pythonのリストと異なり、構造体の定義が明示的に必要。

一方、Juliaでは以下が簡潔になる。

- `for _ in 1:n` は `for _ in range(n)` とほぼ同等
- 三項演算子 `i > 1 ? current[i-1] : 0` はPythonより短い
- `println` と f-string相当の `"$var"` 構文は同程度

### C++

C++はPythonと比較して記述量が明確に増える。

- **型宣言**: すべての変数に型が必要。`double x = dist(rng);` のように、Pythonの `x = random.random()` に比べて冗長。
- **struct定義**: N体問題で `struct Body` のメンバを明示的に列挙。7つのフィールド (`x, y, z, vx, vy, vz, mass`) をすべて型付きで宣言する必要がある。
- **ヘッダインクルード**: `#include <cstdio>`, `#include <cmath>`, `#include <random>`, `#include <vector>` 等。Pythonの `import` より細かい粒度でインクルードが必要。
- **main関数**: `int main() { ... return 0; }` のボイラープレート。
- **乱数生成**: Pythonの `random.random()` 1行に対し、C++では `std::mt19937_64 rng(42);` と `std::uniform_real_distribution<double> dist(0.0, 1.0);` の2行の初期化が必要。
- **定数宣言**: `constexpr double PI = 3.141592653589793;` のように、`constexpr` と型を明記。Pythonの `SOLAR_MASS = 4 * math.pi * math.pi` より冗長。
- **出力書式**: `std::printf("Pi ≈ %.10f\n", pi_est);` は `print(f"Pi ≈ {pi_est}")` に比べて書式指定子が必要。

### Rust

RustはC++と同程度の記述量だが、以下の特徴がある。

- **所有権・ミュータビリティ**: `let mut bodies` のように変更可能な変数には `mut` を明示。関数引数でも `bodies: &mut [Body; N]` と参照の種類を指定。
- **型変換**: `i as f64`, `count as f64` のように整数と浮動小数点の変換が明示的。Pythonでは暗黙的に行われる処理。
- **derive属性**: `#[derive(Clone, Copy)]` を構造体に付与する必要がある(N体問題)。
- **イテレータ記法**: `current.iter().map(|&x| x as u64).sum()` のようなイテレータチェーン。Pythonの `sum(current)` と比べて記述量が増える。

### 言語間の記述量比較

N体問題を例にとると:

| 言語 | 行数(概算) | 増加要因 |
|---|---|---|
| Python | 68行 | - (基準) |
| Python (Numba) | 80行 | ウォームアップ、関数分離 |
| Julia | 65行 | mutable struct定義があるが、全体的に簡潔 |
| C++ | 115行 | struct定義、型宣言、ヘッダ、main関数 |
| Rust | 137行 | struct定義、型変換、所有権、derive |

シンプソン法のような単純なループ処理では言語間の差は小さくなる:

| 言語 | 行数(概算) |
|---|---|
| Python | 15行 |
| Python (Numba) | 21行 |
| Julia | 17行 |
| C++ | 22行 |
| Rust | 19行 |
