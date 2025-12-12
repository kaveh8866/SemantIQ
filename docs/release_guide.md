# Release Guide

## Versioning
- Semantic Versioning: `MAJOR.MINOR.PATCH`
- Current release: `v0.1.0`

## Steps
1. Update `src/semantiq/__init__.py` version and `CHANGELOG.md`
2. Ensure tests pass: `pytest -q`
3. Build package: `python -m build` or `hatch build`
4. Upload to TestPyPI: `python -m twine upload --repository testpypi dist/*`
5. Create a Git tag: `git tag v0.1.0 && git push origin v0.1.0`
6. Publish to PyPI (after validation): `twine upload dist/*`

## Automation (GitHub Actions)
- See `.github/workflows/publish.yml` for a template that builds and uploads on release tags.
