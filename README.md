# Resilient Info Kit

> An open-source, offline-first toolkit that helps people preserve, store, and later re-synchronize critical public-interest information during periods of severe internet disruption.
>
> Public-interest infrastructure for connectivity resilience. Privacy by design. Minimal data. Transparent and auditable.

---

## Why This Exists

Internet disruptions are not only a technical problem — they are a **public health, civic safety, and human dignity problem**. When connectivity drops, people lose access to health information, emergency guidance, and the ability to document their circumstances.

In January 2026, during one of Iran's most intense nationwide internet shutdowns, independent researcher Maziyar Moradi conducted a 30-day study titled *"Anatomy of a Silent Collapse: Digital Isolation, Violence Exposure, and Self-Medication in Iran's Online Ecosystem."* Using only a mobile phone and intermittent connectivity, approximately 3,000 public Persian-language posts were collected and analyzed across X (Twitter), Instagram, Telegram channels, LinkedIn, and satellite TV subtitles. The study documented measurable increases in language around benzodiazepine use, suicidal ideation, digital isolation, economic paralysis, and exposure to violence.

This project focuses on **information resilience**, not network evasion.

---

## What This Project Provides

- **Offline-first storage** of locally authored notes and curated content
- **Encrypted local-only data** by default
- **Store-and-forward sync** that completes safely when connectivity returns
- **Low-bandwidth, mobile-first design**
- **Bilingual documentation** (English and Persian / Farsi)
- **Transparent, auditable architecture**

## What This is NOT

- Not a VPN or censorship-circumvention tool
- Does not bypass network controls
- Does not collect, transmit, or store user credentials
- Does not exploit third-party systems
- Does not perform network-level evasion of controls

## Design Principles

| Principle | Description |
|-----------|-------------|
| User Consent | No hidden data collection, ever |
| Minimal Data | Only what is strictly necessary for function |
| Privacy by Design | Privacy is structural, not an afterthought |
| Transparent Documentation | Every component documented in English and Persian |
| No Credential Theft | Zero tolerance |
| No Exploitation | Built on legitimate, auditable infrastructure |
| Security Review | Independent audit before public release |
| Free Availability | For people who cannot pay |

---

## Repository Structure

```
resilient-info-kit/
├── README.md
├── LICENSE                      # MIT
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
├── THREAT_MODEL.md
├── DATA_MINIMIZATION.md
├── ROADMAP.md
├── docs/
│   ├── architecture.md          # System architecture (EN)
│   ├── architecture.fa.md       # System architecture (FA)
│   ├── user-guide.md            # User guide (EN)
│   └── user-guide.fa.md         # User guide (FA)
├── src/
│   ├── core/
│   │   ├── storage.ts           # Local encrypted store
│   │   ├── sync.ts              # Store-and-forward sync queue
│   │   └── content.ts           # Offline content bundles
│   └── mobile/
│       └── README.md            # Mobile UI specs
├── data/
│   └── schema/
│       └── content-bundle.schema.json
└── .github/
    └── workflows/
        └── ci.yml               # Continuous integration
```

---

## The Problem This Project Addresses

| Layer | Problem |
|-------|---------||
| **Technical** | Commercial tools are expensive, blocked, or require unavailable payment methods |
| **Health** | Shutdown-induced isolation pushes vulnerable populations toward self-medication and suicide |
| **Civic** | Journalists, NGOs, civil society workers lose coordination ability |
| **Educational** | Students lose access to coursework during critical periods |
| **Documented** | Research shows shutdowns trigger measurable increases in despair-language, sedative mentions, suicidal ideation |

---

## Status

**Pre-release.** Public release planned after independent security review.

This repository currently contains:
- Project documentation and policy files
- Threat model and data minimization framework
- Architecture specifications (EN/FA)
- Roadmap
- Placeholder source files for core modules

---

## License

MIT License

---

## About This Project

This project grew directly from field research conducted during active internet blackouts. The researcher, living in Iran, experienced firsthand the connectivity challenges documented in this work:

- **Lost communication channels**: During a blackout, a Linux system crash caused permanent loss of all active Telegram sessions. Recovery was impossible due to the virtual number being expired.
- **Research under fire**: A 30-day study was conducted using only a mobile phone with intermittent connectivity, collecting ~3,000 public posts across social platforms during an active nationwide shutdown.
- **Infrastructure fragility**: Three websites hosted on Iranian infrastructure returned 403 errors and were deindexed by Google during the shutdown, requiring urgent transfer to international hosting.
- **Community engagement**: Active participation in Net4People (net4people/bbs) contributing to discussions on shutdown bypass and tunneling solutions.
- **Tool testing**: Direct experience with circumvention tools (Psiphon, NordVPN, Hotspot Shield) and their limitations under blackout conditions.

## Project Author

**Maziyar Moradi**
- Independent volunteer researcher and mental health activist
- Student, University of the People (S547076 / C110394972)
- Living in Tehran, Iran
- Works under conditions of active internet shutdowns, economic collapse, and constant disconnection threat
- No affiliation with any government or political organization

### Related Work

- *Anatomy of a Silent Collapse: Digital Isolation, Violence Exposure, and Self-Medication in Iran's Online Ecosystem* (Jan 2026)
- 30-day mixed-methods study during nationwide internet shutdown
- ~3,000 Persian-language posts analyzed across X, Instagram, Telegram, LinkedIn, satellite TV subtitles
- Findings shared with NGOs, human rights organizations, and media

### Links

- **Website**: [maziyar.link](https://maziyar.link)
- **GitHub**: [github.com/maziyarid](https://github.com/maziyarid)
- **Additional sites**: [maziyarid.com](https://maziyarid.com), [teznevisan3.com](http://teznevisan3.com), [bluethesis.ir](https://bluethesis.ir)

---

## Repository Metadata

| Field | Value |
|-------|-------||
| **Owner** | [maziyarid](https://github.com/maziyarid) |
| **Visibility** | Public |
| **License** | MIT |
| **Primary Language** | TypeScript |
| **Documentation** | English & Persian (Farsi) |
| **Status** | Pre-release (public after security review) |
| **Created** | June 2026 |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Security

See [SECURITY.md](SECURITY.md) for instructions on reporting security vulnerabilities.

## Code of Conduct

We are committed to fostering an inclusive community. Please see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Acknowledgments

This project was conceived during active internet shutdowns in Iran (2025-2026). The research and development were made possible through intermittent connectivity, community support, and the resilience of people who continue to share information despite systematic attempts to silence them.

---

*Last updated: June 2026*
---
