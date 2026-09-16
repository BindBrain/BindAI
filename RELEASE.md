# BindAI Release Checklist

Use this checklist before publishing a BindAI release or making the repository publicly available.

## Repository and Documentation

* [x] Review roadmap status
* [ ] Review README
* [x] Review CHANGELOG
* [ ] Verify LICENSE
* [ ] Verify CONTRIBUTING
* [ ] Verify CODE_OF_CONDUCT
* [ ] Verify SECURITY
* [ ] Build documentation
* [ ] Verify documentation links and navigation

## Framework Validation

* [x] Run the complete test suite
* [ ] Run `bindai doctor`
* [ ] Run `bindai inspect`
* [ ] Run `bindai init`
* [ ] Run `bindai new my-project`
* [ ] Verify generated project structure
* [ ] Verify a basic agent can be created and executed
* [ ] Verify `Agent.builder()` works from an installed package

## Code Quality

* [x] Run Ruff checks
* [ ] Check Ruff formatting
* [ ] Run Pyright
* [ ] Run mypy
* [x] Review warnings and determine whether any are release blockers

## Package Validation

* [x] Build all workspace packages
* [x] Build the `bindai` distribution
* [x] Build affected package distributions
* [x] Run `twine check` on built distributions
* [x] Verify package metadata
* [x] Verify package contents
* [x] Test installation from built wheels
* [x] Test installation in a clean environment

## Security and Repository Hygiene

* [ ] Verify no API keys or credentials are tracked
* [ ] Verify no `.env` files are tracked
* [ ] Verify no local databases or development artifacts are tracked
* [ ] Review `.gitignore`
* [ ] Review repository history for accidentally committed secrets
* [ ] Review dependency configuration
* [ ] Review public-facing documentation for accidental private information

## Release

* [x] Update `CHANGELOG.md`
* [ ] Create or verify the release tag
* [x] Publish packages to PyPI
* [x] Verify packages install successfully from PyPI
* [ ] Create GitHub Release
* [ ] Attach or reference release artifacts where appropriate
* [ ] Verify documentation after release
* [ ] Verify website after release

## Public Repository Readiness

Before making the repository public:

* [ ] Complete the repository hygiene audit
* [ ] Complete the security audit
* [x] Complete the package and build audit
* [ ] Complete the documentation audit
* [ ] Confirm no private or development-only material remains
* [ ] Confirm the public README accurately reflects the current project
* [x] Confirm the roadmap accurately reflects implemented and remaining work
* [ ] Confirm the repository can be cloned and developed from a clean environment

## Current Progress

* [x] All tests pass
* [ ] `bindai doctor`
* [ ] `bindai inspect`
* [ ] `bindai init`
* [ ] `bindai new my-project`
* [ ] Build docs
* [x] Build wheels
* [x] Publish PyPI
* [ ] GitHub Release
* [x] Update CHANGELOG

The checklist should only be marked complete after the corresponding validation has actually been performed for the release.