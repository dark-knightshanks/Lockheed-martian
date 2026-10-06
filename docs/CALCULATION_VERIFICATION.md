# Calculation Verification - Revision C

DRA-VER-C | 6 October 2026

Independent implementation: `src/verify_revised.py`. Units: N, mm, MPa. Production model units: SI. No production analysis functions are imported by the verifier.

- Cases checked: 30.
- Angular samples per case: 12001.
- Maximum absolute utilisation discrepancy: 4.083359095e-09.
- Maximum relative Fourier beam-moment discrepancy: 1.791455873e-12.
- Nominal-grid minima: matched against both saved CSV sweeps.
- All arithmetic checks passed: True.

The unit suite verifies the prescribed properties, co-located stress extrema, pressure-supported energy inequality, positive-semidefinite quadratic composite bound, Euler singularity, zero-load beam limit, gust isolation, elastic-capacity rejection and integer bisection against direct enumeration. Numerical agreement verifies the implementation of DRA-MTH-C; it is not experimental validation of the manufactured shell.

The complete numerical record is [verification.json](../data/guild_assay/verification.json). The historical Revision A audit is [BASELINE_VERIFICATION.md](history/BASELINE_VERIFICATION.md).
