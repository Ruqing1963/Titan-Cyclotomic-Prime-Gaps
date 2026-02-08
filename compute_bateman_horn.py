#!/usr/bin/env python3
"""
Compute the Bateman-Horn correction factor C_Q for Q(n) = n^47 - (n-1)^47

C_Q = prod_{p prime} (1 - omega_Q(p)/p) / (1 - 1/p)

where omega_Q(p) = 46 if p ≡ 1 (mod 47), and 0 otherwise.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Titan-Cyclotomic-Prime-Gaps
"""

import math


def sieve_primes(n: int) -> list:
    """Sieve of Eratosthenes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def omega_Q(p: int) -> int:
    """
    Compute omega_Q(p): number of solutions to Q(n) ≡ 0 (mod p).

    - p = 47: omega = 0 (ramified; Q(n) ≡ 1 mod 47 always)
    - p ≡ 1 (mod 47): omega = 46 (splitting)
    - otherwise: omega = 0 (inert / shielding)
    """
    if p == 47:
        return 0
    elif (p - 1) % 47 == 0:
        return 46
    else:
        return 0


def compute_CQ(p_max: int = 1_000_000, verbose: bool = True) -> float:
    """Compute C_Q by evaluating the truncated Euler product up to p_max."""
    primes = sieve_primes(p_max)

    C_Q = 1.0
    n_shield = 0
    n_split = 0

    if verbose:
        print(f"Computing C_Q up to p = {p_max:,}")
        print(f"{'p':>8}  {'omega':>5}  {'factor':>12}  {'C_Q':>12}  {'type':>8}")
        print("-" * 55)

    for p in primes:
        w = omega_Q(p)
        factor = (1 - w / p) / (1 - 1 / p)
        C_Q *= factor

        if w == 0:
            n_shield += 1
        else:
            n_split += 1

        if verbose and (p <= 53 or p == 283 or p == 659):
            ptype = "SPLIT" if w == 46 else ("ramif" if p == 47 else "shield")
            print(f"{p:>8}  {w:>5}  {factor:>12.6f}  {C_Q:>12.6f}  {ptype:>8}")

    if verbose:
        print("-" * 55)
        print(f"\nShielding primes (omega=0): {n_shield}")
        print(f"Splitting primes (omega=46): {n_split}")
        print(f"C_Q = {C_Q:.4f}")

        # BH predictions using numerical integration
        # pi_Q(N) ~ C_Q * integral_2^N dt/ln(Q(t))
        # Note: This simple midpoint integration overestimates near t=2
        # where Q(t) is small. The paper uses higher-precision integration
        # yielding rel errors < 0.1%. This script confirms the order of
        # magnitude and convergence trend.
        print("\nBateman-Horn predictions (midpoint integration):")
        for N, actual in [(1e7, 113385), (5e7, 542109), (1e8, 1069872)]:
            steps = 100000
            dt = (N - 2) / steps
            total = 0.0
            for i in range(steps):
                t = 2 + (i + 0.5) * dt
                ln_Qt = math.log(47) + 46 * math.log(t)
                total += dt / ln_Qt
            pred = C_Q * total
            err = (actual - pred) / pred * 100
            print(f"  N={N:.0e}: predicted={pred:,.0f}, actual={actual:,}, "
                  f"rel error={err:+.2f}%")

    return C_Q


def compute_sieve_weight(z: int = 2000) -> float:
    """
    Compute the Selberg sieve weight W = prod_{p<z} (1 - omega(p)/p)
    for Q(n) and for a generic degree-46 polynomial.
    """
    primes = sieve_primes(z)

    W_Q = 1.0
    W_generic = 1.0
    for p in primes:
        w = omega_Q(p)
        W_Q *= (1 - w / p)
        W_generic *= (1 - min(46, p - 1) / p)

    print(f"\nSieve weight comparison (z = {z}):")
    print(f"  Q(n):              W = {W_Q:.6f}")
    print(f"  Generic degree-46: W = {W_generic:.2e}")
    print(f"  Ratio: {W_Q / W_generic:.2e}")
    return W_Q


def main():
    print("=" * 55)
    print("  C_Q for Q(n) = n^47 - (n-1)^47")
    print("=" * 55)
    print()

    C_Q = compute_CQ(1_000_000, verbose=True)
    compute_sieve_weight(2000)

    print(f"\n>>> C_Q = {C_Q:.2f} <<<\n")


if __name__ == "__main__":
    main()
