# Contributing to Resilient Info Kit

Thank you for your interest in contributing to this project. This toolkit serves communities under internet shutdowns and censorship — your contributions can have real impact on people's lives.

## Before You Begin

Please read:
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community standards
- [SECURITY.md](SECURITY.md) — Security reporting procedures
- [THREAT_MODEL.md](THREAT_MODEL.md) — Understand the threat landscape

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Device and OS information
   - Steps to reproduce
   - Expected vs actual behavior
   - **Do not include** any personally identifying information

### Suggesting Features

Open a feature request issue. Consider:
- Does this help users during internet shutdowns?
- Does this minimize data collection?
- Does this work offline?
- Is this safe for users in high-risk environments?

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Write tests for your changes
4. Ensure all tests pass: `npm test`
5. Run linting: `npm run lint`
6. Commit with a descriptive message
7. Open a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/resilient-info-kit.git
cd resilient-info-kit

# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build
```

## Code Standards

- **Language**: TypeScript (strict mode)
- **Style**: ESLint + Prettier (config included)
- **Tests**: Jest for unit tests
- **Commits**: Conventional Commits format

## Privacy & Security Requirements for Contributors

All contributions must:

- **Minimize data collection** — Collect only what is strictly necessary
- **Encrypt at rest** — All stored data must be encrypted
- **Work offline** — Core functionality must not require connectivity
- **Be auditable** — No obfuscated code; clear, reviewable logic
- **Not fingerprint users** — Avoid device or behavior fingerprinting
- **Protect metadata** — Consider what metadata is leaked

## Documentation Contributions

Documentation is needed in both English and Persian (Farsi). If you can contribute translations:

- English files: `docs/*.md`
- Persian files: `docs/*.fa.md`

## Priority Areas

We especially need help with:

1. **Security review** — Audit encryption and storage implementations
2. **Persian (Farsi) translations** — Docs and UI strings
3. **Mobile UI** — React Native components (see `src/mobile/`)
4. **Offline sync** — Store-and-forward queue improvements
5. **Content bundles** — Schema and validation tooling

## Questions?

Open a discussion in the GitHub Discussions tab. For security-sensitive topics, see [SECURITY.md](SECURITY.md).

---

*Every contribution to this project supports access to information as a human right.*
