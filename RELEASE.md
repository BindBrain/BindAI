# BindAI Release Checklist

Use this checklist before publishing a BindAI release or making the repository publicly available.

## Repository and Documentation

* [ ] Review roadmap status
* [ ] Review README
* [ ] Review CHANGELOG
* [ ] Verify LICENSE
* [ ] Verify CONTRIBUTING
* [ ] Verify CODE_OF_CONDUCT
* [ ] Verify SECURITY
* [ ] Build documentation
* [ ] Verify documentation links and navigation

## Framework Validation

* [ ] Run the complete test suite
* [ ] Run `bindai doctor`
* [ ] Run `bindai inspect`
* [ ] Run `bindai init`
* [ ] Run `bindai new my-project`
* [ ] Verify generated project structure
* [ ] Verify a basic agent can be created and executed
* [ ] Verify `Agent.builder()` works from an installed package

## Code Quality

* [ ] Run Ruff checks
* [ ] Check Ruff formatting
* [ ] Run Pyright
* [ ] Run mypy
* [ ] Review warnings and determine whether any are release blockers

## Package Validation

* [ ] Build all workspace packages
* [ ] Build the `bindai` distribution
* [ ] Build affected package distributions
* [ ] Run `twine check` on built distributions
* [ ] Verify package metadata
* [ ] Verify package contents
* [ ] Test installation from built wheels
* [ ] Test installation in a clean environment

## Security and Repository Hygiene

* [ ] Verify no API keys or credentials are tracked
* [ ] Verify no `.env` files are tracked
* [ ] Verify no local databases or development artifacts are tracked
* [ ] Review `.gitignore`
* [ ] Review repository history for accidentally committed secrets
* [ ] Review dependency configuration
* [ ] Review public-facing documentation for accidental private information

## Release

* [ ] Update `CHANGELOG.md`
* [ ] Create or verify the release tag
* [ ] Publish packages to PyPI
* [ ] Verify packages install successfully from PyPI
* [ ] Create GitHub Release
* [ ] Attach or reference release artifacts where appropriate
* [ ] Verify documentation after release
* [ ] Verify website after release

## Public Repository Readiness

Before making the repository public:

* [ ] Complete the repository hygiene audit
* [ ] Complete the security audit
* [ ] Complete the package and build audit
* [ ] Complete the documentation audit
* [ ] Confirm no private or development-only material remains
* [ ] Confirm the public README accurately reflects the current project
* [ ] Confirm the roadmap accurately reflects implemented and remaining work
* [ ] Confirm the repository can be cloned and developed from a clean environment

## Current Progress

* [ ] All tests pass
* [ ] `bindai doctor`
* [ ] `bindai inspect`
* [ ] `bindai init`
* [ ] `bindai new my-project`
* [ ] Build docs
* [ ] Build wheels
* [ ] Publish PyPI
* [ ] GitHub Release
* [x] Update CHANGELOG

The checklist should only be marked complete after the corresponding validation has actually been performed for the release.
