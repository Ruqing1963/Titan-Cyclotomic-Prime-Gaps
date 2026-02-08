#!/usr/bin/env python3
"""
Verify the Complete Local Obstruction Theorem (Theorem 3.1)

For Q(n) = n^47 - (n-1)^47:
  1. omega(p) = 0 for all primes p ≢ 1 (mod 47) (including p = 47)
  2. omega(p) = 46 for all primes p ≡ 1 (mod 47)
  3. Q(n) ≡ 1 (mod 47) for all n
  4. No prime p < 283 ever divides Q(n)

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Titan-Cyclotomic-Prime-Gaps
"""


def sieve_primes(n: int) -> list:
    """Sieve of Eratosthenes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def omega_brute_force(p: int) -> int:
    """Brute-force: count n in [0, p-1] with Q(n) ≡ 0 (mod p)."""
    count = 0
    for n in range(p):
        q = (pow(n, 47, p) - pow((n - 1) % p, 47, p)) % p
        if q == 0:
            count += 1
    return count


def omega_theory(p: int) -> int:
    """Theoretical omega from Theorem 3.1."""
    if p == 47:
        return 0
    elif (p - 1) % 47 == 0:
        return 46
    else:
        return 0


def verify_omega(p_max: int = 6299):
    """Verify omega(p) by brute force for all primes up to p_max."""
    primes = sieve_primes(p_max)
    print(f"Verifying omega(p) for all {len(primes)} primes up to {p_max}...")
    print(f"{'p':>6}  {'theory':>7}  {'brute':>6}  {'type':>8}  {'match':>6}")
    print("-" * 42)

    all_ok = True
    for p in primes:
        brute = omega_brute_force(p)
        theory = omega_theory(p)
        match = "OK" if brute == theory else "FAIL"
        ptype = "SPLIT" if (p - 1) % 47 == 0 and p != 47 else (
            "ramif" if p == 47 else "shield")

        if brute != theory:
            all_ok = False
            print(f"{p:>6}  {theory:>7}  {brute:>6}  {ptype:>8}  {match:>6}")
        elif p <= 53 or (p - 1) % 47 == 0:
            print(f"{p:>6}  {theory:>7}  {brute:>6}  {ptype:>8}  {match:>6}")

    print("-" * 42)
    status = "PASS" if all_ok else "FAIL"
    print(f"  [{status}] omega verified for all primes up to {p_max}")
    return all_ok


def verify_mod47(n_max: int = 100_000):
    """Verify Q(n) ≡ 1 (mod 47) for all n in [0, n_max]."""
    print(f"\nVerifying Q(n) ≡ 1 (mod 47) for n in [0, {n_max:,}]...")
    for n in range(n_max + 1):
        q_mod = (pow(n, 47, 47) - pow((n - 1) % 47, 47, 47)) % 47
        if q_mod != 1:
            print(f"  FAIL at n = {n}: Q(n) ≡ {q_mod} (mod 47)")
            return False
    print(f"  [PASS] Q(n) ≡ 1 (mod 47) for all n in [0, {n_max:,}]")
    return True


def verify_no_small_divisors(n_max: int = 10_000):
    """Verify no prime < 283 divides Q(n) for n in [2, n_max]."""
    small_primes = sieve_primes(282)
    print(f"\nVerifying no prime < 283 divides Q(n) for n in [2, {n_max:,}]...")
    print(f"  Testing against {len(small_primes)} primes: {small_primes[:10]}...")

    for n in range(2, n_max + 1):
        for p in small_primes:
            q_mod = (pow(n, 47, p) - pow((n - 1) % p, 47, p)) % p
            if q_mod == 0:
                print(f"  FAIL: p={p} divides Q({n})")
                return False

    print(f"  [PASS] No prime < 283 divides Q(n) for n in [2, {n_max:,}]")
    return True


def verify_smallest_bad_prime():
    """Verify that 283 = 6*47+1 is the smallest bad prime."""
    primes = sieve_primes(300)
    print(f"\nVerifying 283 is the smallest prime ≡ 1 (mod 47)...")
    for p in primes:
        if (p - 1) % 47 == 0:
            print(f"  First prime ≡ 1 (mod 47): p = {p}")
            if p == 283:
                print(f"  [PASS] 283 = 6 × 47 + 1 confirmed")
                return True
            else:
                print(f"  [FAIL] Expected 283, got {p}")
                return False
    return False


def count_bad_moduli(q_max: int = 50_000):
    """Count bad moduli (all prime factors ≡ 1 mod 47) up to q_max."""
    primes = sieve_primes(q_max)
    bad_primes_set = set(p for p in primes if (p - 1) % 47 == 0)

    bad_count = 0
    for q in range(2, q_max + 1):
        temp = q
        all_bad = True
        for p in primes:
            if p * p > temp:
                break
            while temp % p == 0:
                if p not in bad_primes_set:
                    all_bad = False
                    break
                temp //= p
            if not all_bad:
                break
        if temp > 1 and temp not in bad_primes_set:
            all_bad = False
        if all_bad:
            bad_count += 1

    pct = bad_count / q_max * 100
    null_pct = 100 - pct
    print(f"\nBad moduli count (q ≤ {q_max:,}):")
    print(f"  Bad (all factors ≡ 1 mod 47): {bad_count} ({pct:.1f}%)")
    print(f"  Null (at least one factor ≢ 1 mod 47): {q_max - bad_count} ({null_pct:.1f}%)")
    print(f"  Paper claims ~97.8% null: {'CONSISTENT' if null_pct > 97 else 'MISMATCH'}")


def main():
    print("=" * 55)
    print("  Local Obstruction Verification")
    print("  Q(n) = n^47 - (n-1)^47")
    print("=" * 55)
    print()

    ok1 = verify_omega(6299)
    ok2 = verify_mod47(100_000)
    ok3 = verify_no_small_divisors(10_000)
    ok4 = verify_smallest_bad_prime()
    count_bad_moduli(50_000)

    print("\n" + "=" * 55)
    all_ok = ok1 and ok2 and ok3 and ok4
    print(f"  OVERALL: {'ALL PASS' if all_ok else 'SOME FAILED'}")
    print("=" * 55)


if __name__ == "__main__":
    main()
