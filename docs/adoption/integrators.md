# Community Adoption: Integrators & Tool Builders

## Building on SemantIQ
We encourage the ecosystem to build tools *around* SemantIQ.

### Types of Integration
- **Leaderboards**: Aggregating results from multiple sources (with strict verification).
- **Visualization Dashboards**: Advanced plotting of SMF/HACS metrics.
- **CI/CD Plugins**: GitHub Actions or Jenkins plugins that wrap the SemantIQ CLI.

### Integration Principles
1.  **Attribution**: You must clearly state "Powered by SemantIQ-M-Benchmarks" and link to the repo.
2.  **Version Pinning**: Your tool must explicitly state which version of the benchmark data it is using.
3.  **No "Black Box" Scoring**: If you modify the scoring logic, you must rename the metric (e.g., "MyTool-Score", not "SemantIQ-Score").

### Technical Integration
- **CLI JSON Output**: Use the `--format json` flag (planned) or parse the standard output structure.
- **Python API**: Import `semantiq` as a library (future SDK stability guarantee pending). currently, calling via subprocess is the most stable method.
