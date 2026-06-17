# Threat Model

**Project**: Resilient Info Kit
**Version**: 0.1 (Pre-release)
**Last Updated**: June 2026
**Status**: Draft — pending independent security review

---

## 1. Overview

This document describes the threat model for the Resilient Info Kit — an offline-first toolkit for preserving and distributing critical public-interest information during internet shutdowns.

The primary deployment context is **Iran during active internet shutdowns** (2025-2026), though the system is designed for any similar environment.

---

## 2. Assets to Protect

| Asset | Sensitivity | Why It Matters |
|-------|-------------|----------------|
| User identity | Critical | Users may face arrest or harm if identified |
| User location | Critical | Physical safety risk |
| Usage patterns | High | Can reveal political affiliation |
| Content bundles | Medium | Some content may be illegal to possess |
| Sync peer relationships | High | Graph of associations is sensitive |
| Device metadata | Medium | Can be used to fingerprint |

---

## 3. Adversary Profiles

### 3.1 State-Level Adversary (Primary)

**Capability**: Nation-state with full network visibility
- Deep packet inspection (DPI) at ISP level
- Physical device seizure and forensic analysis
- Legal compulsion of service providers
- Social network analysis
- Infiltration of activist communities

**Motivation**: Identify dissidents; suppress information sharing

**Resources**: Unlimited (state budget)

### 3.2 Network Passive Observer

**Capability**: Traffic analysis on local/regional networks
- Packet capture
- Timing analysis
- Volume analysis

**Motivation**: Identify users of circumvention tools

### 3.3 Malicious Peer

**Capability**: Another device in the sync network
- Can observe sync traffic
- May attempt to poison content bundles
- May attempt to de-anonymize peers

**Motivation**: Intelligence gathering; sabotage

### 3.4 Physical Adversary

**Capability**: Access to seized device
- Full filesystem access if unencrypted
- Memory forensics if device is running
- Rubber-hose cryptanalysis

**Motivation**: Evidence gathering; identification of associates

---

## 4. Threat Scenarios

### T-1: Device Seizure
**Threat**: Device is seized by authorities; data extracted
**Mitigation**: Full encryption of local storage; plausible deniability features (planned); minimal data retention
**Residual Risk**: Strong passphrase required by user; not enforced by software

### T-2: Network Traffic Analysis
**Threat**: Sync traffic identified as suspicious; user flagged
**Mitigation**: Traffic obfuscation (planned); minimize sync frequency; use common protocols
**Residual Risk**: Volume anomalies may still be detectable

### T-3: Content Bundle Poisoning
**Threat**: Malicious peer injects false or harmful content
**Mitigation**: Cryptographic signing of content bundles; provenance chain
**Residual Risk**: Social engineering of legitimate signers

### T-4: Metadata Leakage
**Threat**: App logs, timestamps, or file metadata reveals user behavior
**Mitigation**: Strip metadata on ingest; no persistent logs; randomize timestamps
**Residual Risk**: OS-level metadata outside app control

### T-5: Supply Chain Attack
**Threat**: Compromised build or dependency
**Mitigation**: Reproducible builds (planned); dependency pinning; minimal dependencies; CI with hash verification
**Residual Risk**: Trust in build infrastructure

### T-6: Malicious App Version
**Threat**: Attacker distributes trojanized version of app
**Mitigation**: Code signing; checksum verification; open source for community review
**Residual Risk**: Users downloading from unofficial sources

---

## 5. Trust Boundaries

```
[User Device] <-- encrypted --> [Local Storage]
     |
     | (optional, when connectivity exists)
     v
[Sync Network] <-- authenticated --> [Peer Devices]
     |
     v
[Content Providers] (trusted signers only)
```

**Untrusted**: Network, peers, content providers without valid signatures
**Partially Trusted**: Peer devices with valid credentials
**Trusted**: Local device (after unlock), verified content signers

---

## 6. Security Properties

| Property | Status | Notes |
|----------|--------|-------|
| Encryption at rest | Planned | AES-256-GCM |
| Forward secrecy | Planned | For sync sessions |
| Content signing | Planned | Ed25519 |
| Plausible deniability | Research | Hidden volumes |
| Network anonymity | Out of scope | Recommend Tor separately |
| Metadata minimization | Planned | See DATA_MINIMIZATION.md |

---

## 7. Out of Scope

- Network-level anonymity (recommend using Tor or similar separately)
- Protection against device owner being coerced
- OS-level vulnerabilities
- Physical security of the device itself

---

## 8. Review Schedule

This threat model will be reviewed:
- Before each major release
- After any significant security incident
- After independent security audit
- Annually at minimum

---

*This threat model is a living document. Real-world deployment will reveal gaps that must be addressed.*
