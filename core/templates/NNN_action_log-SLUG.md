# Project NNN — Action Log

Serial, append-only postcard timeline. One line per action, appended to the END.
Format: `ISO8601-UTC,<postcard>`. Append with:
`echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),<postcard>" >> <this file>`
Do not rewrite history; only append. This is a `log` doc — no YAML frontmatter by convention.

[YYYY-MM-DDThh:mm:ssZ],project scaffold created (six files + index); planning-only session, no product code
