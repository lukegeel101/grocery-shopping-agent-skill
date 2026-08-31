# Contributing

Thanks for helping make grocery-shopping agents safer, clearer, and easier to reuse.

## Good contributions

- Improve deterministic validation and comparison logic.
- Add fictional examples that exercise delivery fees, coupons, coverage, or substitutions.
- Clarify privacy boundaries and approval gates.
- Improve compatibility with ChatGPT-style and Claude-style skill environments.

Never include real addresses, access codes, retailer credentials, loyalty identifiers, payment data, or personal grocery histories.

## Development workflow

1. Create a focused branch from `main`.
2. Make the smallest coherent change.
3. Add or update tests.
4. Run the complete local verification suite.

```bash
python3 scripts/validate_workspace.py
python3 scripts/evaluate_sample.py --check
python3 -m unittest discover -s tests -v
```

5. Open a pull request using the repository template.

## Pull-request expectations

- Explain the user outcome, safety implications, and verification performed.
- Keep all public examples fictional.
- Preserve the rule that no purchase, payment, login, or account change occurs without explicit user authorization.
- Update `docs/gotchas.md` when a verified issue and fix would help future contributors.

By participating, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
