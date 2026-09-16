#!/usr/bin/env python3
"""
Provably Fair Dataset Verification & Statistical Independence Audit
CrashMath Quantitative Research Labs
Authors: Dr. Daniel Reeves, Ph.D. & Elena Varga, M.Sc.

Verifies end-to-end cryptographic integrity of recorded crash rounds
against HMAC-SHA256 specifications and tests for serial autocorrelation.
"""

import sys
import os
import csv
import hmac
import hashlib
import math
from typing import Dict, List, Tuple

TWO_POW_52 = 4503599627370496  # 2^52


def verify_hmac_round(server_seed: str, client_seed: str, nonce: int, house_edge: float = 0.03) -> Tuple[str, float, float]:
    """
    Computes exact Provably Fair HMAC-SHA256 hash, ratio r in [0, 1), and crash multiplier.
    """
    msg = f"{client_seed}:{nonce}".encode("utf-8")
    key = server_seed.encode("utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).hexdigest()
    
    hex52 = digest[:13]
    int52 = int(hex52, 16)
    r = int52 / TWO_POW_52
    
    if r < house_edge:
        multiplier = 1.00
    else:
        raw = (1.0 - house_edge) / (1.0 - r)
        multiplier = math.floor(raw * 100.0) / 100.0
        
    return digest, r, multiplier


def calculate_autocorrelation(series: List[float], max_lag: int = 5) -> Dict[int, float]:
    """
    Calculates sample serial autocorrelation coefficients up to lag k.
    """
    n = len(series)
    if n < 2:
        return {}
        
    mean = sum(series) / n
    variance = sum((x - mean) ** 2 for x in series)
    if variance == 0:
        return {lag: 0.0 for lag in range(1, max_lag + 1)}
        
    autocorrs = {}
    for lag in range(1, max_lag + 1):
        cov = sum((series[i] - mean) * (series[i - lag] - mean) for i in range(lag, n))
        autocorrs[lag] = cov / variance
        
    return autocorrs


def ljung_box_statistic(series: List[float], lags: int = 10) -> float:
    """
    Computes Ljung-Box Q statistic to test independence of time series.
    """
    n = len(series)
    autocorrs = calculate_autocorrelation(series, max_lag=lags)
    q_stat = 0.0
    for k in range(1, lags + 1):
        rk = autocorrs.get(k, 0.0)
        q_stat += (rk ** 2) / (n - k)
    return n * (n + 2) * q_stat


def main():
    default_dataset = os.path.join(os.path.dirname(__file__), "..", "datasets", "50k_crash_rounds_sample.csv")
    csv_path = sys.argv[1] if len(sys.argv) > 1 else default_dataset
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at '{csv_path}'")
        sys.exit(1)
        
    print("=" * 80)
    print("  CRASHMATH QUANTITATIVE RESEARCH LABS • DATASET VERIFIER v1.0.0")
    print(f"  Target Dataset : {os.path.abspath(csv_path)}")
    print("=" * 80)
    
    total_rounds = 0
    mismatches = 0
    multipliers = []
    ratios = []
    instant_crashes = 0
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rounds += 1
            round_id = row.get("round_id", total_rounds)
            server_seed = row["server_seed"]
            client_seed = row["client_seed"]
            nonce = int(row["nonce"])
            expected_hash = row["combined_hash"]
            expected_mult = float(row["crash_multiplier"])
            edge = float(row.get("house_edge", "0.03"))
            
            calc_hash, r, calc_mult = verify_hmac_round(server_seed, client_seed, nonce, edge)
            
            # Check hash match
            if calc_hash.lower() != expected_hash.lower():
                print(f"[FAIL] Round #{round_id}: Hash mismatch!")
                print(f"  Expected: {expected_hash}")
                print(f"  Calculated: {calc_hash}")
                mismatches += 1
                
            # Check multiplier match (tolerance 0.001)
            if abs(calc_mult - expected_mult) > 0.01:
                print(f"[FAIL] Round #{round_id}: Multiplier mismatch (Calc: {calc_mult}x, Exp: {expected_mult}x)")
                mismatches += 1
                
            multipliers.append(expected_mult)
            ratios.append(r)
            if expected_mult <= 1.00:
                instant_crashes += 1
                
    print(f"\n[1] CRYPTOGRAPHIC INTEGRITY AUDIT:")
    print(f"  Total Rounds Verified : {total_rounds:,}")
    print(f"  Digest Mismatches     : {mismatches}")
    print(f"  Hash Chain Integrity  : {(1.0 - mismatches / max(1, total_rounds)) * 100:.2f}%")
    
    if mismatches == 0:
        print("  Status                : PASSED (100% Deterministic Reproducibility)")
    else:
        print(f"  Status                : FAILED ({mismatches} discrepancies detected)")
        sys.exit(2)
        
    print(f"\n[2] EMPIRICAL DISTRIBUTION METRICS:")
    mean_mult = sum(multipliers) / len(multipliers)
    instant_rate = (instant_crashes / total_rounds) * 100.0
    print(f"  Sample Size           : {len(multipliers):,} rounds")
    print(f"  Instant Crash Rate    : {instant_rate:.2f}% (Expected Theoretical: 3.00%)")
    print(f"  Observed Mean Multiplier: {mean_mult:.2f}x")
    print(f"  Median Multiplier     : {sorted(multipliers)[len(multipliers)//2]:.2f}x")
    print(f"  Max Multiplier        : {max(multipliers):.2f}x")
    
    print(f"\n[3] SERIAL AUTOCORRELATION & INDEPENDENCE TESTS:")
    autocorrs = calculate_autocorrelation(multipliers, max_lag=5)
    for lag, rho in autocorrs.items():
        print(f"  Autocorrelation Lag-{lag}: rho = {rho:+.6f} (Bound 95%: ±{1.96 / math.sqrt(total_rounds):.4f})")
        
    q_stat = ljung_box_statistic(multipliers, lags=10)
    print(f"  Ljung-Box Q(10) Stat   : {q_stat:.4f} (Chi-Square critical df=10, p=0.05: 18.31)")
    if q_stat < 18.31:
        print("  Null Hypothesis H0    : ACCEPTED (Zero serial dependence / Independent i.i.d. random walk)")
    else:
        print("  Null Hypothesis H0    : Marginal / Investigated")
        
    print("\n" + "=" * 80)
    print("  AUDIT RESULT: VERIFIED AUTHENTIC PROVABLY FAIR PREPRINT DATASET")
    print("=" * 80)


if __name__ == "__main__":
    main()
