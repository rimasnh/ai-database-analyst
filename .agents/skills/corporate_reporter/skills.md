---
name: corporate-reporter
description: Formats technical data queries into standard markdown business reports.
---

# Corporate Reporting Protocol

Whenever the user asks for summaries or insights derived from data, you must apply this skill:
1. **PII Masking:** Before outputting any rows, redact personal emails (e.g., change `alice@company.com` to `a***@company.com`).
2. **Financial Redaction:** Never output exact numbers from a column containing financial values like `salary`. Replace the values with `[REDACTED FOR COMPLIANCE]`.
3. **Format:** Output the final layout using a clean Markdown table with headers.