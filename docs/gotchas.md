# Gotchas

## Historical artifacts can disagree

Issue: multiple shopping artifacts may contain different item counts, totals, or update times.

Verified fix: designate one canonical state file, treat other artifacts as historical evidence, and compare timestamps before applying changes.

## A low item price can produce a worse basket

Issue: delivery fees, service fees, minimum-order charges, and incomplete coverage can erase item-level savings.

Verified fix: compare normalized unit cost and the complete delivered basket, then show any split order separately.

## Checkout claims are not public evidence

Issue: exact eligibility, account-only coupons, taxes, tips, and member pricing may not be visible without authentication.

Verified fix: keep those fields unknown or estimated until verified and never present them as confirmed public facts.

## Package changes can hide a bad substitution

Issue: a cheaper-looking replacement may use a smaller package or cover fewer days.

Verified fix: normalize units and state the package and horizon differences in every substitution proposal.

## The bundled skill checker may lack its YAML dependency

Issue: the local `quick_validate.py` entrypoint could not start because PyYAML was not installed in its Python environment, and the installed Ruby YAML version did not expose `safe_load_file` for the first fallback attempt.

Verified fix: the repository's dependency-free validator passed, the YAML frontmatter and `agents/openai.yaml` were parsed with `safe_load` over explicit file contents, and no scaffold placeholders remained.

## Packaging checks depend on the current directory

Issue: one final metadata command was launched from the `outputs` directory while still prefixing repository paths with `outputs/`, so the files were not found.

Verified fix: rerun the checks with repository paths relative to the actual current directory, then rebuild and test the archive.
