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

## GitHub publishing may require approved network access

Issue: the first GitHub identity check produced no output inside the restricted network environment.

Verified fix: rerun the narrow GitHub command with approved network access, verify the active account, create the repository as private, push `main`, and read back the private visibility setting.

## Inspect ZIP archives one at a time

Issue: `zipinfo` treats a second archive argument as a filename pattern inside the first archive rather than as another archive to inspect.

Verified fix: inspect each archive in a separate command and confirm that neither contains `.git` metadata.

## A technical README can hide the fun part

Issue: the original README led with the repository tree before showing the address-aware delivery comparison, deal search, and smart substitution experience.

Verified fix: lead with user outcomes and visual examples, move implementation details lower, and keep every capability claim tied to the actual approval and privacy boundaries.

## Keep multi-file patches scoped to the correct file

Issue: the first combined redesign patch targeted a gotcha-log sentence inside the workflow reference, so patch verification rejected the entire change before editing any file.

Verified fix: split the work into file-specific hunks, apply the workflow and gotcha changes to their correct paths, and verify the resulting diff before testing.

## Preview SVG artwork through a rendered copy

Issue: the local image viewer does not open SVG files directly, so it could not provide the required visual inspection of the README hero artwork.

Verified fix: validate the source SVG as XML, render a temporary PNG with ImageMagick, visually inspect the PNG, and keep the resolution-independent SVG as the only repository asset.

## Use the supported Ruby YAML interface

Issue: the installed Ruby YAML library does not expose `safe_load_file`, so the first final metadata check failed before parsing the agent manifest.

Verified fix: read the file explicitly and pass its contents to `YAML.safe_load`; the manifest then parsed successfully with aliases disabled.
