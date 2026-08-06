#!/usr/bin/env python3
"""Generate and verify the canonical Fund field dictionary artifacts."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from canonical_field_dictionary import build, load_json, load_package, package_sha256, sha256_text
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_SOURCE=ROOT/"data/dictionary/spec_v1"
DEFAULT_MANIFEST=ROOT/"data/dictionary/CANONICAL_FIELD_DICTIONARY_MANIFEST_V1.json"
DEFAULT_OUTPUT_DIR=ROOT/"build/dictionary"

def write_outputs(output_dir:Path,outputs:dict[str,str])->None:
    output_dir.mkdir(parents=True,exist_ok=True)
    names={"expanded_json":"CANONICAL_FIELD_DICTIONARY_V1.json","csv":"CANONICAL_FIELD_DICTIONARY_V1.csv","markdown":"CANONICAL_FIELD_DICTIONARY_V1.md"}
    for key,name in names.items(): (output_dir/name).write_text(outputs[key],encoding="utf-8")

def check_manifest(manifest:dict,source:Path,outputs:dict[str,str])->None:
    actual={"authoritative_package_sha256":package_sha256(source),"expanded_json_sha256":sha256_text(outputs["expanded_json"]),"csv_sha256":sha256_text(outputs["csv"]),"markdown_sha256":sha256_text(outputs["markdown"])}
    if actual!=manifest["checksums"]: raise ValueError(f"manifest checksum drift: actual={actual} expected={manifest['checksums']}")

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--source",type=Path,default=DEFAULT_SOURCE); parser.add_argument("--manifest",type=Path,default=DEFAULT_MANIFEST); parser.add_argument("--output-dir",type=Path,default=DEFAULT_OUTPUT_DIR); parser.add_argument("--check-manifest",action="store_true"); args=parser.parse_args()
    try:
        spec=load_package(args.source); outputs=build(spec); write_outputs(args.output_dir,outputs)
        if args.check_manifest: check_manifest(load_json(args.manifest),args.source,outputs)
    except (OSError,json.JSONDecodeError,ValueError,KeyError) as exc:
        print(f"ERROR: {exc}",file=sys.stderr); return 1
    print(f"OK: canonical fund dictionary fields=143 package_sha256={package_sha256(args.source)} expanded_sha256={sha256_text(outputs['expanded_json'])} csv_sha256={sha256_text(outputs['csv'])} markdown_sha256={sha256_text(outputs['markdown'])}")
    return 0
if __name__=="__main__": raise SystemExit(main())
