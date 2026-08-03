# Changelog

All notable changes to the **Italienation** project are documented here.
This project follows [Semantic Versioning](https://semver.org/).

---

## [v1.0.0-rc1] – 2026-08-03 — Release Candidate 1

Full interactive platform with scrollytelling, econometric analysis, and verified data provenance.

### Added
- **Econometric Costs dashboard** — €259B total cost breakdown with Recharts visualisations and international comparison table.
- **Deep-link provenance map** — `SourceBadge.jsx` `DEEP_LINK_MAP` now contains 25+ verified institutional source URLs.
- **React Error Boundary** — graceful fallback UI for unexpected render errors.
- **Active-link highlighting** in Navbar via `useLocation`.
- **Scrollytelling structure** — all major sections wrapped with scroll-activated animations (Framer Motion `whileInView`).
- **Systemic Costs route** (`/costs`) wired into the app router and Navbar.
- **Data provenance audit** — automated HTTP audit of all source links; results documented in `docs/data_provenance_audit.md`.
- **`docs/` directory** — structured documentation folder with provenance audit report.
- **Repository badges** — release, build, and GitHub Pages status badges in `README.md`.
- **GitHub Release** for `v1.0.0-rc1` with full release notes.

### Fixed
- Broken 404 source links (MIUR dropout page, MUR stats, UAAR religion page) redirected to active institutional portals.
- Unused-import lint warnings cleaned across multiple components.
- `og:image` and `twitter:image` meta tags updated from `vite.svg` to `favicon.svg`.

### Changed
- README updated with Release Notes section, badge table, and provenance audit link.
- `DATA_INVENTORY.md` and `DATA_TRACEABILITY_MATRIX.md` path references corrected.

---

## [v0.5.0-beta] – 2026-07-31 — Beta Dashboard

First public interactive React dashboard deployed to GitHub Pages.

### Added
- React + Vite + TailwindCSS v4 frontend scaffold.
- **OED Simulator** — conditional probability engine for Italy's educational tracking system.
- **Observatory page** — key structural indicators panel.
- **ScrollyDataHub** — paginated dataset browser sourcing from `processed_data/`.
- **Bilingual UI** — Italian/English toggle via `LanguageContext` with `localStorage` persistence.
- **Leaflet maps** — interactive choropleth of school distribution.
- **Recharts** — visualisations for ESCS stratification, NEET, and retention data.
- GitHub Pages deployment pipeline (`npm run deploy` via `gh-pages`).

### Changed
- Data assets migrated from `local_data/processed/` to `processed_data/` and exposed via `frontend/public/api/`.

---

## [v0.1.0-alpha] – 2026-07-15 — Alpha Data Pipeline

Initial open-science data release; Python/Jupyter processing layer.

### Added
- SDMX ingestion pipelines for ISTAT, Eurostat, INVALSI, INPS, and INAIL.
- 286 processed data panels across 66 research domains.
- Jupyter Notebook HTML exports documenting each aggregation step.
- `DATA_INVENTORY.md`, `DATA_TRACEABILITY_MATRIX.md`, and `OSF_ZENODO_RESEARCH_PROSPECTUS.md`.
- Initial repository structure with `processed_data/`, `notebooks/`, and `frontend/` directories.
