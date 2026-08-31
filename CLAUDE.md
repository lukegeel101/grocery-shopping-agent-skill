# Claude project instructions

Read and follow `SKILL.md` for every grocery-list, price-check, coupon, delivery-service, or substitution task in this repository.

Use `config/grocery.example.json` and `data/sample-grocery-list.json` only as fictional examples.
Real user state belongs in ignored private files outside the public repository.

Run `python3 scripts/validate_workspace.py` after changing public examples or schemas.
Run `python3 -m unittest discover -s tests -v` after changing validation behavior.

Never place an order, submit payment, sign in to a retailer, or change an external account as part of the default workflow.

