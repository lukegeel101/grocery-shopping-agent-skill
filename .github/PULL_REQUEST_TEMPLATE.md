## What changed

Describe the user-visible outcome.

## Safety and privacy

- [ ] No personal grocery data, address, credential, payment information, or secret was added.
- [ ] Purchase, payment, login, and account-change actions remain approval-gated.
- [ ] New examples use fictional data.

## Verification

- [ ] `python3 scripts/validate_workspace.py`
- [ ] `python3 scripts/evaluate_sample.py --check`
- [ ] `python3 -m unittest discover -s tests -v`

List any additional checks and their results.
