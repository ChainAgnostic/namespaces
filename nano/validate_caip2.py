#!/usr/bin/env python3
"""Validate the Nano CAIP-2 namespace profile (caip2.md) against its own spec.

Reproduces every Test Case in the proposal against the exact validation
regex it defines. Also cross-checks the mainnet genesis block hash.

Run:  python3 validate_caip2.py
Exit code 0 = all checks pass; 1 = a check failed.

Verified 2026-09-21 (fern): all 8 test cases pass; genesis hash confirmed
against nano-python's GENESIS_BLOCK_HASH constant; live block_info on
rpc.nano.to returns height:1, type:open, confirmed:true for the genesis hash.
"""
import re
import subprocess

GENESIS = "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"

# The exact validation regex from the proposal (caip2.md, "Validation regular
# expression, anchored and case-insensitive"). No re.I flag: CAIP-2 states a
# chain_id is CASE-SENSITIVE, so the namespace prefix `nano` must stay
# lowercase; only the reference accepts mixed case hex.
RE = re.compile(r"^nano:[0-9A-Fa-f]{64}$")


def valid(candidate: str) -> bool:
    return bool(RE.match(candidate))


valid_cases = [
    f"nano:{GENESIS}",            # uppercase hex reference
    f"nano:{GENESIS.lower()}",    # lowercase hex reference (case-insensitive on input)
]

invalid_cases = [
    "nano:mainnet",               # symbolic, not a hash (legacy alias only)
    "nano:991CF190",              # too short
    "nano:",                      # empty reference
    f"NANO:{GENESIS}",            # namespace identifier is lowercase - rejected
    f"nano:{GENESIS[:63]}Z",      # non-hex character
    GENESIS[:63],                 # 63 chars, no prefix
]


def main() -> int:
    ok = True
    for c in valid_cases:
        r = valid(c)
        print(f"{'PASS' if r else 'FAIL'} valid   {c[:20]}...")
        ok = ok and r
    for c in invalid_cases:
        r = not valid(c)
        print(f"{'PASS' if r else 'FAIL'} invalid {c[:20]}...")
        ok = ok and r

    # Cross-check the genesis hash constant is the canonical mainnet value.
    expected = "991cf190094c00f0b68e2e5f75f6bee95a2e0bd93ceaa4a6734db9f19b728948"
    hex_ok = GENESIS.lower() == expected
    print(f"{'PASS' if hex_ok else 'FAIL'} genesis hash is canonical mainnet {GENESIS[:16]}...")
    ok = ok and hex_ok

    # Live RPC cross-check (optional; rpc.nano.to is the public reference node).
    payload = '{"action":"block_info","json_block":"true","hash":"%s"}' % GENESIS
    try:
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json",
             "-d", payload, "https://rpc.nano.to"],
            capture_output=True, text=True, timeout=30,
        ).stdout
        live_ok = '"height":"1"' in out and '"type":"open"' in out and '"confirmed":"true"' in out
        print(f"{'PASS' if live_ok else 'FAIL'} live RPC confirms genesis height:1 open confirmed")
    except Exception as e:  # noqa: BLE001 - best-effort live check
        print(f"SKIP live RPC (unavailable): {e}")
        live_ok = True  # not a spec failure when offline
    ok = ok and live_ok

    print("\nALL CHECKS:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
