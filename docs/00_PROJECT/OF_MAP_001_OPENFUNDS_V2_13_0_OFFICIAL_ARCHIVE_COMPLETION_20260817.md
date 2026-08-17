# OF-MAP-001 — Official Openfunds v2.13.0 Field List archive completion

Date: 2026-08-17
Branch: `architecture/africafunds-country-indicators-v0.1`
Status: `OFFICIAL_ARCHIVE_VERIFIED_COMPLETE_PARSE_PENDING`

## Purpose

Close the binary-source gate of `OF-MAP-001` without reconstructing, normalizing, rewriting or inventing any Openfunds catalogue content.

The archived artifact is the exact official Openfunds Field List v2.13.0 PDF retrieved from the official Openfunds domain.

## Official artifact

```text
Standard: Openfunds
Version: 2.13.0
Document status: FINAL
Document date: 2026-03-23
Media type: application/pdf
PDF version: 1.7
Page count: 745
Byte size: 2,957,096
SHA256: 40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
```

Exact source URL:

```text
https://openfunds.org/wp-content/uploads/2026/03/openfunds_fields_v2.13.0.pdf
```

Archived repository paths:

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf.sha256
data/openfunds/official/v2.13.0/SOURCE_AND_LICENSE.md
data/openfunds/source_manifest_v2.13.0.json
```

The archived PDF is intentionally unaltered. The checksum is a provenance invariant and must be revalidated before any parser consumes the artifact.

## Licence boundary

The repository records the official licence as Creative Commons Attribution-NoDerivatives 4.0 International (`CC BY-ND 4.0`) with attribution to `www.openfunds.org`.

Consequences for the implementation:

1. the official PDF remains byte-identical and is never edited or re-saved;
2. a parser must consume the checksum-locked source rather than produce a replacement “official” document;
3. canonical mappings are separate repository metadata and never overwrite the official source;
4. no official Openfunds identifier, name, definition, type or cardinality may be invented;
5. transformed/derived public redistribution must remain within the verified licence boundary; the safest implementation is to keep the original artifact intact and keep internal mapping metadata separate.

## Governed archive workflow

Workflow:

```text
.github/workflows/of-map-001-archive-openfunds-v2.13.0.yml
```

Four executions were intentionally fail-closed while the gate was hardened.

### Run 1 — environment dependency discovered

```text
32060554996
```

- exact official download: success;
- PDF magic/content type/size: success;
- stopped before provenance write because `pdfinfo` / `pdftotext` were not installed on the runner;
- no archive commit.

### Run 2 — document identity proven, layout assertion too strict

```text
32060627996
```

- `poppler-utils` installed explicitly;
- PDF identity confirmed;
- `Pages: 745` confirmed;
- `File size: 2957096 bytes` confirmed;
- first page extracted successfully and displayed `FINAL`, `Version 2.13.0`, `2026-03-23`;
- stopped only because fixed-string assertions assumed one space after labels while the PDF uses layout padding;
- no archive commit.

### Run 3 — checksum proven, untracked-directory enumeration detected

```text
32060720657
```

- exact download: success;
- official metadata checks: success;
- checksum generated and revalidated successfully;
- observed SHA256:

```text
40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
```

- stopped only because standard `git status --porcelain` compacted the entirely new archive directory into one untracked-directory entry;
- no archive commit.

### Run 4 — final gate

```text
32060831250
Conclusion: SUCCESS
```

All gates passed:

1. archive target absent before run;
2. exact HTTPS official URL downloaded without transformation;
3. `%PDF-` magic verified;
4. `application/pdf` content type verified;
5. size bounds verified;
6. PDF verification tooling installed explicitly;
7. 745 pages verified;
8. first-page status/version/date verified;
9. SHA256 generated;
10. SHA256 revalidated against the binary after provenance generation;
11. exact changed-file scope enumerated with `git status --porcelain=v1 -uall`;
12. only the three new archive/provenance files plus the existing source manifest were staged;
13. commit/push succeeded.

## Manifest state after archive

`data/openfunds/source_manifest_v2.13.0.json` now declares:

```text
status: OFFICIAL_V2_13_0_FIELD_LIST_ARCHIVED_CHECKSUM_LOCKED_PARSE_PENDING
binary_archive.status: ARCHIVED_UNALTERED
```

The archive gate is therefore closed. `OF-MAP-001` itself is **not yet complete**, because deterministic parsing and field inventory validation remain open.

## Next gate — deterministic parser

The parser must be developed against the checksum-locked artifact and must fail closed if the checksum changes.

Required sequence:

```text
VERIFY SHA256
→ EXTRACT DETERMINISTIC TEXT/STRUCTURE
→ DISCOVER ACTUAL PDF RECORD LAYOUT
→ TEST KNOWN FIELD-RECORD BOUNDARIES
→ PARSE OFFICIAL IDS AND ATTRIBUTES
→ CHECK UNIQUENESS / COUNTS / ORDER
→ EMIT SEPARATE MAPPING-INPUT METADATA
```

Before committing a full transformed copy of official definitions to this public repository, licence implications of `NoDerivatives` must remain respected. Parser code and canonical mapping metadata can progress without modifying the archived official artifact.

## Safety conclusion

This completion closes only the official binary archive/hash gate. It does not authorize:

- invented Openfunds fields;
- a claimed complete mapping before deterministic parsing;
- rewriting or modifying the official PDF;
- replacing the canonical model with the Openfunds physical structure;
- production activation;
- merge/retarget of PR #1;
- changes to `main`.
