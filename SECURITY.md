# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| main (Public Beta) | Yes |

## Reporting a vulnerability

If you discover a security issue, please **do not** open a public GitHub issue.

Email the maintainer via the [Contact](https://iskonnect.vercel.app/contact) page or report privately through GitHub Security Advisories on this repository.

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We aim to acknowledge reports within 72 hours and provide a status update within 7 days.

## Scope

In scope:

- Authentication and authorization bypass
- SQL injection or data exposure
- Cross-site scripting (XSS) in the web app
- Server-side request forgery (SSRF)
- Insecure direct object references on user data

Out of scope:

- Social engineering
- Denial of service against third-party services (Render, Supabase, Vercel)
- Issues in dependencies without a demonstrable exploit path in this application

## Safe harbor

We appreciate responsible disclosure and will not pursue legal action against researchers who follow this policy.
