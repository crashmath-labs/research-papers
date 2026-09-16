# Provably Fair Crash Rounds Dataset (Sample Archive)

**Identifier**: `CRASHMATH-DATA-2026-04`  
**Authors**: Dr. Daniel Reeves, Ph.D. & Elena Varga, M.Sc.  
**Institution**: [CrashMath Quantitative Research Labs](https://crashmath.org)  
**License**: [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

---

## Dataset Description

This dataset contains a contiguous sequence of **10,000 Provably Fair crash game rounds** generated using standard industry cryptographic specifications (`HMAC-SHA256`).

It serves as the reproducible benchmark dataset analyzed in the academic preprint:
> *Reeves, D., & Varga, E. (2026). Empirical Evaluation of 50,000 Provably Fair Rounds: Autocorrelation, House Edge Invariance, and Resistance to Machine Learning Predictors.* Technical Report CRASHMATH-TECH-2026-04, CrashMath Quantitative Research Labs.

---

## Cryptographic Parameters

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Algorithm** | `HMAC-SHA256` | Standard Hash-based Message Authentication Code |
| **Server Seed** | `d82f7c04e286e9b109b8f729f345861b58a2d1297e6b528a49c916298516e874` | Fixed revealed 256-bit server seed entropy |
| **Client Seed** | `crashmath_empirical_verification_2026` | Public verifiable client entropy salt |
| **Nonce Range** | `1` to `10,000` | Strictly sequential incremental nonce |
| **House Edge ($e$)** | `0.03` ($3.0\%$) | Operational house edge parameter |
| **Mantissa Width** | 52 bits (`0` to $2^{52}-1$) | First 13 hex nibbles of the digest |

---

## Column Schema

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `round_id` | `INTEGER` | Unique round index (1-indexed) |
| `server_seed` | `STRING (hex64)` | The revealed secret server seed used as HMAC key |
| `client_seed` | `STRING` | The public client seed string |
| `nonce` | `INTEGER` | Sequential counter appended to client seed (`"{client_seed}:{nonce}"`) |
| `combined_hash` | `STRING (hex64)` | The raw 64-character hexadecimal `HMAC-SHA256` digest |
| `hex52` | `STRING (hex13)` | The first 13 characters of `combined_hash` representing the 52-bit integer |
| `r_ratio` | `FLOAT [0, 1)` | Uniform float derived by $\text{int52} / 2^{52}$ |
| `crash_multiplier` | `FLOAT (>= 1.00)` | Final crash point multiplier, truncated to 2 decimal places |
| `instant_crash` | `BOOLEAN (0 or 1)` | Flag indicating whether $r < e$, triggering an immediate 1.00x crash |
| `house_edge` | `FLOAT` | House edge parameter applied ($0.03 = 3.0\%$) |

---

## Mathematical Derivation Formula

1. **Digest Generation**:
   $$\text{digest} = \text{HMAC-SHA256}(\text{key}=\text{server\_seed}, \text{msg}=\text{client\_seed} \mathbin{\Vert} \text{nonce})$$

2. **52-bit Uniform Ratio $r$**:
   $$h_{52} = \text{int}(\text{digest}[0:13], 16)$$
   $$r = \frac{h_{52}}{2^{52}}$$

3. **Multiplier Calculation**:
   $$\text{Crash Multiplier} = \begin{cases} 
   1.00, & \text{if } r < e \\
   \left\lfloor \frac{100 \times (1 - e)}{100 \times (1 - r)} \times 100 \right\rfloor \div 100, & \text{if } r \ge e
   \end{cases}$$

---

## Reproducible Verification

To verify every single row against HMAC-SHA256 and confirm statistical i.i.d. properties:

```bash
python scripts/verify_dataset.py datasets/50k_crash_rounds_sample.csv
```
