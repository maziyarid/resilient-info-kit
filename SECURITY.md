# Security Policy

## Supported Versions

This project is currently in pre-release. Security fixes will be applied to the latest version on the `main` branch.

| Version | Supported |
|---------|----------|
| main (pre-release) | ✅ |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

This project serves users in high-risk environments. A publicly disclosed vulnerability could put real people in danger.

### How to Report

1. **Email**: Send a detailed report to the maintainer privately
   - GitHub profile: [maziyarid](https://github.com/maziyarid)
   - Use encrypted communication if possible (PGP preferred)

2. **GitHub Private Vulnerability Reporting**: Use GitHub's built-in security advisory feature:
   - Go to the Security tab of this repository
   - Click "Report a vulnerability"

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Suggested fix (if any)
- Your contact information (optional)

**Do NOT include**:
- Any real user data
- Information that could identify users in high-risk regions

## Response Timeline

| Action | Timeline |
|--------|----------|
| Acknowledgment | Within 72 hours |
| Initial assessment | Within 7 days |
| Fix timeline estimate | Within 14 days |
| Fix release | Depends on severity |

## Security Considerations for This Project

Given that this tool is designed for use in environments with active surveillance and censorship, we treat the following as critical security concerns:

### Critical (Immediate response)
- Any vulnerability that could expose user identity or location
- Encryption failures in local storage
- Network traffic leaking identifying information
- Backdoors or intentional data exfiltration

### High (Response within 48 hours)
- Vulnerabilities allowing data corruption
- Authentication/authorization bypasses
- Denial of service affecting offline functionality

### Medium (Response within 7 days)
- Information disclosure not tied to user identity
- Non-critical cryptographic weaknesses

### Low (Response within 30 days)
- Minor information leaks
- Best-practice deviations

## Threat Model

See [THREAT_MODEL.md](THREAT_MODEL.md) for the full threat model, including adversary profiles relevant to this project.

## Security Audit Status

**Current status**: Pre-release, awaiting independent security audit before public release.

We are actively seeking security researchers and organizations willing to conduct a pro-bono security audit of this project, given its humanitarian purpose.

---

*Security is not a feature — it is the foundation of this project.*
