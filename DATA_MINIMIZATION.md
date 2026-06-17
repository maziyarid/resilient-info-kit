# Data Minimization Framework

**Project**: Resilient Info Kit
**Version**: 0.1
**Last Updated**: June 2026

---

## Principle

> Collect nothing you don't need. Store nothing you don't use. Delete everything you can.

Data minimization is not just a privacy feature — in environments with active state surveillance, unnecessary data collection can endanger lives.

---

## 1. Data Inventory

### 1.1 Data We Collect

| Data Type | Purpose | Retention | Encrypted | Required |
|-----------|---------|-----------|-----------|----------|
| Content bundles | Core functionality | Until deleted by user | Yes | Yes |
| Sync timestamps | Conflict resolution | 30 days max | Yes | No* |
| Error logs | Debugging | Session only | N/A | No |
| User preferences | UX | Local only | Yes | No |

*Can be disabled; reduces sync accuracy

### 1.2 Data We Never Collect

- User identity or name
- Location data (GPS, IP, cell tower)
- Device identifiers (IMEI, MAC address, advertising ID)
- Contact lists or social graph
- Usage analytics or telemetry
- Crash reports sent to external servers
- Any biometric data

---

## 2. Storage Rules

### 2.1 Local Storage

- All data stored locally MUST be encrypted at rest (AES-256-GCM)
- Encryption key derived from user passphrase via Argon2id
- No plaintext fallback
- Temporary files deleted immediately after use

### 2.2 Sync Storage

- Only content bundles are synced between peers
- No user metadata is transmitted during sync
- Sync sessions use forward-secret session keys
- Peer identifiers are ephemeral and rotated each session

### 2.3 Memory

- Sensitive data cleared from memory after use
- No sensitive data written to disk swap if avoidable
- Passphrase material zeroed after key derivation

---

## 3. Retention Policy

| Data | Retention | Trigger |
|------|-----------|--------|
| Content bundles | Until user deletes | User action |
| Sync session keys | Session duration only | Session end |
| Error logs | Current session only | App close |
| Temporary files | Immediate | Operation complete |
| User preferences | Until app uninstall | User action |

**Default**: When in doubt, do not retain.

---

## 4. Third-Party Data Sharing

**We share no data with any third party. Ever.**

- No analytics services
- No crash reporting services
- No CDN or content delivery
- No push notification services (use pull instead)
- No authentication providers

---

## 5. Metadata Minimization

Metadata can be as dangerous as content. We minimize:

- **File timestamps**: Normalized or randomized on ingest
- **EXIF data**: Stripped from all media in content bundles
- **Network metadata**: Minimize sync frequency; randomize timing
- **App usage patterns**: No internal analytics
- **Bundle provenance**: Only trusted signer identity, no user path

---

## 6. User Rights

Users have the right to:

- **Access**: View all data stored by the app
- **Delete**: Remove any or all data at any time
- **Export**: Export their content bundles in open formats
- **Audit**: Inspect what the app does with their data (open source)

---

## 7. Implementation Checklist

- [ ] Encryption at rest for all local data
- [ ] No external network calls without explicit user action
- [ ] No device identifier collection
- [ ] Session-only error logging
- [ ] Metadata stripping on content ingest
- [ ] User data deletion feature
- [ ] Memory zeroing for sensitive data
- [ ] Sync anonymization
- [ ] Dependency audit for data collection
- [ ] Privacy audit before public release

---

## 8. Audit

This framework will be audited:
- By independent security researchers before public release
- Annually during active development
- After any significant architecture change

---

*Data minimization is an act of respect for users who trust us with their safety.*
