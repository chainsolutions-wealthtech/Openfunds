# OF-MAP-001 — Deterministic Openfunds v2.13.0 parse completion

Date: 2026-08-17
Branch: `architecture/africafunds-country-indicators-v0.1`
Status: `VERIFIED_COMPLETE`

## Result

`OF-MAP-001` is complete at the governed source/inventory layer.

The repository now has all required prerequisites for field-by-field mapping:

```text
OFFICIAL VERSION                2.13.0
OFFICIAL RELEASE DATE           2026-03-23
OFFICIAL DOCUMENT STATUS        FINAL
OFFICIAL PDF ARCHIVED           YES — byte-identical
OFFICIAL PDF PAGES              745
OFFICIAL PDF BYTES              2,957,096
SHA256 LOCKED                   40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
DETERMINISTIC PARSER            VERIFIED
PYTHON 3.11                     GREEN
PYTHON 3.12                     GREEN
OFFICIAL FIELD RECORDS          1,869
UNIQUE OF-IDS                   1,869
CONCRETE OF-IDS                 1,849
PARAMETERIZED XX TEMPLATES      20
FULL DERIVED CATALOGUE COMMIT   NO
NEXT TASK                       OF-MAP-002
```

## Immutable source

The parser is bound to:

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf.sha256
```

Expected SHA256:

```text
40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
```

Any checksum drift is a hard failure. The parser does not silently consume a different standard release.

## Layout discovery

Read-only workflow:

```text
.github/workflows/of-map-001-audit-fieldlist-layout.yml
```

The first layout audit established the scale of the deterministic extraction:

```text
pdftotext mode: -layout
TEXT_BYTES: 1,881,634
TEXT_LINES: 34,360
```

A broad token scan was deliberately not treated as a field count because OF-IDs also occur in descriptions, ranges and examples.

The refined field-record audit then identified actual record headers of the form:

```text
OF-ID <OF-ID> Field Name <official field name>
```

Verified structure:

```text
ACTUAL FIELD RECORD HEADERS: 1,869
CONCRETE GRAMMAR RECORDS:    1,849
COUNTRY-TEMPLATE RECORDS:       20
DUPLICATE OF-IDS:                0
```

One additional `OF-ID Range Field Tags` line belongs to document/table furniture and is not a field record.

## Verified OF-ID grammar

The official v2.13.0 inventory uses two structural forms:

```text
OF[A-Z]{2}\d{6}
OF[A-Z]{2}\d{4}XX
```

Combined governed parser grammar:

```text
OF[A-Z]{2}(?:\d{6}|\d{4}XX)
```

The `XX` suffix is official parameterization and is preserved exactly. It must never be replaced with an invented country code in the source inventory.

The 20 parameterized templates consist of one `OFNW` template and nineteen `OFST` templates.

## TDD parser evidence

Contract:

```text
tests/test_parse_openfunds_v2_13_0.py
```

RED run:

```text
GitHub Actions run: 32061734854
```

The RED was exact on Python 3.11 and 3.12:

```text
ModuleNotFoundError: No module named 'scripts.parse_openfunds_v2_13_0'
```

No implementation existed before the contract.

GREEN implementation:

```text
scripts/parse_openfunds_v2_13_0.py
.github/workflows/of-map-001-parser.yml
```

GREEN run:

```text
GitHub Actions run: 32061806859
Conclusion: SUCCESS
```

All three jobs passed:

```text
parser-unit (3.11)                    SUCCESS
parser-unit (3.12)                    SUCCESS
checksum-locked official inventory    SUCCESS
```

The integration job verified the official checksum before extraction, installed Poppler explicitly, parsed the actual 745-page PDF, checked the exact inventory and confirmed that the repository remained clean after runtime parsing.

## Exact official structural inventory

```text
field_records: 1869
concrete_ids: 1849
parameterized_country_templates: 20
unique_ids: 1869
first_id: OFST001000
last_id: OFIN000410
```

Prefix counts:

```text
OFCA   44
OFDC   21
OFDY   67
OFEE  617
OFEF   29
OFEM  122
OFEP  143
OFFV    7
OFIN   11
OFNW   14
OFPH   92
OFPM    8
OFRE   42
OFST  652
```

Total: `1,869`.

## Parser behaviour

The parser:

1. verifies the PDF SHA256 against the sidecar and governed expected checksum;
2. invokes `pdftotext -layout` into an ephemeral directory;
3. recognizes only governed OF-ID forms;
4. preserves `XX` country templates unchanged;
5. detects duplicate OF-IDs;
6. rejects malformed lines that present themselves as field headers;
7. preserves field-name continuations before `Field Tags`;
8. emits a structural summary JSON only in CI;
9. does not modify the archived PDF or repository.

## Licence boundary

The official Field List is licensed `CC BY-ND 4.0`. The architecture therefore deliberately avoids committing a rewritten public copy of the full official definitions.

The repository keeps:

- the unaltered official source;
- the checksum;
- parser code;
- structural verification metrics;
- separate canonical mapping metadata.

`OF-MAP-002` must reference verified OF-IDs and add the project's own canonical mapping semantics without presenting a modified derivative of the official Field List as an official document.

## Closure decision

The acceptance criteria of `OF-MAP-001` are now met:

```text
official version/source/date        VERIFIED
official archive                    VERIFIED
license/provenance                  VERIFIED
official identifiers inventoried    VERIFIED
deterministic parsing               VERIFIED
field count/uniqueness              VERIFIED
no invented official field          PRESERVED
```

Therefore:

```text
OF-MAP-001 = TERMINE
OF-MAP-002 = READY / EN_COURS
```

This closure does not imply that the 1,869 fields are already mapped to the canonical model. That is the independent `OF-MAP-002` task.
