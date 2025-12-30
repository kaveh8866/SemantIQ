# GitHub Pages & Public Website

## Overview
SemantIQ uses GitHub Pages to host public documentation and the Web UI (in static mode). This ensures documentation is always available and versioned alongside the code.

## Publishing Strategy

### Source
- **Documentation**: Generated from `docs/` using a static site generator (e.g., MkDocs) or served directly if using simple Markdown rendering.
- **Web UI**: The React app in `webapp/` can be built (`npm run build`) and deployed to a subdirectory or separate domain.

### CI/CD Integration
The `.github/workflows/pages.yml` (to be created) handles deployment.

#### Build Steps
1.  **Checkout**: Get the code.
2.  **Build UI**: Run `npm install && npm run build` in `webapp/`.
3.  **Assemble**: Copy `docs/` and `webapp/dist/` to a publishing directory.
4.  **Deploy**: Use `actions/deploy-pages` to publish.

## Rollback Strategy
GitHub Pages deployments are tied to Git commits. To rollback:
1.  Revert the commit on `main`.
2.  Wait for the CI pipeline to redeploy the previous state.

## Privacy & Security
- **No Private Data**: The public site must NOT contain any internal logs, API keys, or private user data.
- **Static Content Only**: The site is read-only. Dynamic features requiring a backend (like running benchmarks) must be run locally by the user.
