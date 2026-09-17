# CrashMath Quantitative Research Labs — Technical Papers & Datasets

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Preprint: CRASHMATH--TECH--2026--04](https://img.shields.io/badge/Preprint-CRASHMATH--TECH--2026--04-purple.svg)](https://crashmath.org/papers/provably-fair-empirical-study-2026.pdf)
[![Reproducibility: 100% Verified](https://img.shields.io/badge/Reproducibility-100%25%20Verified-blue.svg)](scripts/verify_dataset.py)
[![Peer Review: Open Science](https://img.shields.io/badge/Protocol-HMAC--SHA256-orange.svg)](https://crashmath.org)

Official preprint repository, LaTeX sources, empirical verification datasets, and peer-review artifacts from **CrashMath Quantitative Research Labs**.

---

## 🏛️ Research Mission

CrashMath Quantitative Research Labs conducts rigorous mathematical audits, cryptographic validations, and statistical probability analyses of online multiplier gaming protocols.

Our objective is to replace opaque claims with **open-source mathematical proof**, reproducible datasets, and deterministic verification tools.

---

## 📑 Catalog of Technical Papers

### 📄 Paper 1: CRASHMATH-TECH-2026-04

> **"Empirical Evaluation of 50,000 Provably Fair Rounds: Autocorrelation, House Edge Invariance, and Resistance to Machine Learning Predictors"**  
> **Authors**: CrashMath Quantitative Research Labs  
> **Published**: April 2026  
> **Format**: [PDF Technical Report](papers/CRASHMATH-TECH-2026-04/paper.pdf) (Mirror: [crashmath.org/papers](https://crashmath.org/papers/provably-fair-empirical-study-2026.pdf)) | [LaTeX Source](papers/CRASHMATH-TECH-2026-04/paper.tex) | [BibTeX](papers/CRASHMATH-TECH-2026-04/references.bib)

#### Abstract
Provably Fair crash games constitute an increasingly prevalent class of online multiplier-based games governed by cryptographic commitment schemes. Despite pervasive claims by commercial third parties regarding predictive signal bots and martingale staking systems, systematic empirical verification remains sparse. 

In this paper, we conduct an exhaustive cryptographic and statistical evaluation of 50,000 consecutively verified rounds generated under the HMAC-SHA256 commitment protocol. We evaluate serial dependence across lags $k \in [1, 50]$ using Pearson autocorrelation, the Ljung-Box test ($Q(20) = 18.42, p = 0.56$), and the Wald-Wolfowitz runs test ($Z = 0.42, p = 0.67$), confirming that round outcomes satisfy independent and identically distributed (i.i.d.) random walk properties. 

Furthermore, we train four machine learning architectures (LSTM, XGBoost, Multi-Layer Perceptron, and Logistic Regression) over sliding sequence histories; all models collapse to random chance ($\text{ROC-AUC} \in [0.4998, 0.5004]$). Finally, via Doob's Optional Stopping Theorem, we formally prove that progressive betting strategies cannot shift the negative expected value ($\mathbb{E}[X] = -0.03$), with Martingale sequences exhibiting asymptotic certainty of capital ruin ($P(\text{Ruin}) \to 1.00$).

---

## 📊 Key Empirical Benchmarks

### 1. Cryptographic Autocorrelation & Serial Independence ($N = 50,000$)

| Metric / Test | Test Value | Critical Threshold / Bound (95%) | Null Hypothesis $H_0$ | Result |
| :--- | :---: | :---: | :---: | :---: |
| **Lag-1 Autocorrelation ($\rho_1$)** | $-0.00115$ | $\pm 0.00876$ | Zero Serial Dependence | **ACCEPTED** |
| **Lag-2 Autocorrelation ($\rho_2$)** | $-0.00162$ | $\pm 0.00876$ | Zero Serial Dependence | **ACCEPTED** |
| **Lag-5 Autocorrelation ($\rho_5$)** | $-0.00117$ | $\pm 0.00876$ | Zero Serial Dependence | **ACCEPTED** |
| **Ljung-Box $Q(20)$** | $18.42$ | $\chi^2_{20, 0.05} = 31.41$ ($p = 0.56$) | White Noise Sequence | **ACCEPTED** |
| **Wald-Wolfowitz Runs Test** | $Z = 0.42$ | $|Z| < 1.96$ ($p = 0.67$) | Independent Random Walk | **ACCEPTED** |
| **Chi-Square Goodness-of-Fit** | $\chi^2 = 47.12$ | $\chi^2_{49, 0.05} = 66.34$ ($p = 0.55$) | Theoretical PDF Match | **ACCEPTED** |

### 2. Machine Learning Multiplier Predictor Benchmark (Out-of-Sample $M \ge 2.00\times$)

| Model Architecture | Accuracy | ROC-AUC | Log-Loss | Predictive Advantage |
| :--- | :---: | :---: | :---: | :---: |
| **Theoretical Random Walk** | $48.50\%$ | $0.5000$ | $0.6901$ | $0.00\%$ (Baseline) |
| **Logistic Regression** | $48.49\%$ | $0.4998$ | $0.6902$ | **None** |
| **Random Forest (200 Trees)** | $48.54\%$ | $0.5003$ | $0.6907$ | **None** |
| **XGBoost (Depth=4)** | $48.47\%$ | $0.5001$ | $0.6905$ | **None** |
| **LSTM (2-layer Recurrent)** | $48.52\%$ | $0.5004$ | $0.6903$ | **None** |

---

## 💾 Open Datasets

The repository includes open verification datasets in `datasets/`:

- **[`datasets/50k_crash_rounds_sample.csv`](datasets/50k_crash_rounds_sample.csv)**: 10,000 verified sequential crash rounds with exact server seeds, client seeds, nonces, HMAC-SHA256 digests, 52-bit mantissas, and crash multipliers.
- **[`datasets/README.md`](datasets/README.md)**: Full codebook and mathematical schema documentation.

---

## 🔬 Reproducible Verification

Verify every single round in the dataset against the HMAC-SHA256 specification using standard library Python:

```bash
# Run cryptographic audit and autocorrelation verification
python scripts/verify_dataset.py
```

Expected Output:
```text
================================================================================
  CRASHMATH QUANTITATIVE RESEARCH LABS • DATASET VERIFIER v1.0.0
  Target Dataset : .../datasets/50k_crash_rounds_sample.csv
================================================================================

[1] CRYPTOGRAPHIC INTEGRITY AUDIT:
  Total Rounds Verified : 10,000
  Digest Mismatches     : 0
  Hash Chain Integrity  : 100.00%
  Status                : PASSED (100% Deterministic Reproducibility)

[2] EMPIRICAL DISTRIBUTION METRICS:
  Sample Size           : 10,000 rounds
  Instant Crash Rate    : 3.00% - 4.00% (Within statistical error)
  Observed Mean Multiplier: 9.34x
  Median Multiplier     : 1.93x

[3] SERIAL AUTOCORRELATION & INDEPENDENCE TESTS:
  Autocorrelation Lag-1: rho = -0.001155 (Bound 95%: ±0.0196)
  Ljung-Box Q(10) Stat   : 0.1961 (Chi-Square critical df=10, p=0.05: 18.31)
  Null Hypothesis H0    : ACCEPTED (Zero serial dependence / Independent i.i.d.)
```

---

## 📚 Citation (BibTeX)

```bibtex
@techreport{crashmath2026empirical,
  title={Empirical Evaluation of 50,000 Provably Fair Rounds: Autocorrelation, House Edge Invariance, and Resistance to Machine Learning Predictors},
  author={{CrashMath Quantitative Research Labs}},
  institution={CrashMath Quantitative Research Labs},
  number={CRASHMATH-TECH-2026-04},
  year={2026},
  url={https://crashmath.org/papers/provably-fair-empirical-study-2026.pdf}
}
```

---

## ⚖️ License

- **Research Papers, Preprints, LaTeX Sources, and Datasets**: [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- **Software, Scripts, and Algorithms**: [MIT License](LICENSE)

---

## 📬 Contact & Inquiries

For academic inquiries, collaboration, or cryptographic verification requests:
- **Email**: [contact@crashmath.org](mailto:contact@crashmath.org)
- **Web**: [crashmath.org](https://crashmath.org)
- **Organization**: [github.com/crashmath-labs](https://github.com/crashmath-labs)
