#!/usr/bin/env python3
"""Generate the governed BCEAO/BEAC FX reference synchronization migration."""
from __future__ import annotations
import argparse, csv, io, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv"
DEFAULT_OUTPUT = ROOT / "schemas/reference/012_validated_fx_reference_registry.sql"
NS = uuid.UUID("d4f88e04-7384-4d50-8e3d-65f4d67894c8")
FIXED = {
"org:BCEAO":"302dbf2d-4a75-5e9f-84eb-d6b5368cf4ab","org:BEAC":"af6d3e9d-95fd-50ca-8880-6f58f564bdd4",
"endpoint:BCEAO_FX_DAILY":"857a19f9-8c29-5dff-a84c-c0c93a540bf8","endpoint:BEAC_FX_DAILY":"cb5518cd-236c-5ded-8941-56f09eb74bdc",
"map:UEMOA_D09_FX_EUR":"5c9d24db-71cb-5ef6-a229-4cd490afdf9e","map:UEMOA_D09_FX_USD":"0c1fb34d-b686-5e16-a7e6-1075b47b7d8b",
"map:CEMAC_D09_FX_EUR":"ed45fa2d-6cca-5d7b-9f8f-370f49b441a9","map:CEMAC_D09_FX_USD":"16d59b96-a6ed-5fa6-9997-3e9c74ddb94e",
"series:PS_UEMOA_BCEAO_FX_SNAPSHOT":"41b0ddb2-a1ed-5733-b3e1-a07e249b9753","series:PS_UEMOA_FX_XOF_EUR":"352810a4-a95f-581b-8065-26c6840e5674","series:PS_UEMOA_FX_XOF_USD":"f9393b91-98dc-5f8d-96cf-a510345dbcf2",
"series:PS_CEMAC_BEAC_FX_SNAPSHOT":"60058d6f-608e-5221-abd3-86585386a4bb","series:PS_CEMAC_FX_XAF_EUR":"b1da9ec4-7672-5214-a117-37726a7c40f6","series:PS_CEMAC_FX_XAF_USD":"29740f5e-fbd7-53f6-873c-8ca5a223ab39",
"spec:CS_UEMOA_BCEAO_FX_SNAPSHOT":"11464493-a058-5ff6-98ad-4f0a3ba8d82b","spec:CS_CEMAC_BEAC_FX_SNAPSHOT":"128bb2f4-ff2d-5633-8e13-b5e1cb72c88d"}
REQUIRED = tuple("PILOT_CODE ORGANIZATION_CODE SCOPE_CODE CURRENCY_CODE ENDPOINT_CODE SOURCE_URL RETRIEVED_AT EVIDENCE_ID WORKFLOW_RUN_ID RAW_SHA256 VALUE_DATE PARSER_VERSION OBSERVATION_COUNT RAW_MAPPING_CODE RAW_SERIES_CODE RAW_SPEC_CODE EUR_MAPPING_CODE EUR_SERIES_CODE EUR_SPEC_CODE USD_MAPPING_CODE USD_SERIES_CODE USD_SPEC_CODE SELECTOR QUALITY_PROFILE".split())

def sid(kind: str, code: str) -> str: return FIXED.get(f"{kind}:{code}", str(uuid.uuid5(NS, f"{kind}:{code}")))
def q(v: str) -> str: return "'" + v.replace("'", "''") + "'"
def load(path: Path) -> list[dict[str,str]]:
    raw=path.read_text(encoding="utf-8")
    if "\r" in raw: raise ValueError("CR characters are forbidden")
    reader=csv.DictReader(io.StringIO(raw), delimiter=";")
    if tuple(reader.fieldnames or ()) != REQUIRED: raise ValueError("unexpected registry header")
    rows=list(reader)
    if {r["PILOT_CODE"] for r in rows}!={"BCEAO_XOF","BEAC_XAF"}: raise ValueError("exactly BCEAO_XOF and BEAC_XAF are required")
    for r in rows:
        if None in r or any(not r[k] for k in REQUIRED): raise ValueError(f"incomplete row {r.get('PILOT_CODE')}")
        if r["PARSER_VERSION"]!="0.2.0" or len(r["RAW_SHA256"])!=64: raise ValueError("invalid governed evidence")
    return rows

def render(path: Path=DEFAULT_SOURCE) -> str:
    out=["-- GENERATED FILE: DO NOT EDIT.","-- Authoring source: data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv","-- PostgreSQL remains the runtime source of truth after application.",""]
    for r in load(path):
        org=r["ORGANIZATION_CODE"]; scope=r["SCOPE_CODE"]; cur=r["CURRENCY_CODE"]
        evidence=f"EVIDENCE_{r['EVIDENCE_ID']}_RUN_{r['WORKFLOW_RUN_ID']}_SHA256_{r['RAW_SHA256']}_VALUE_DATE_{r['VALUE_DATE'].replace('-','_')}"
        out += [f"update ref.organization set official_website={q(r['SOURCE_URL'].split('/fr')[0] if org=='BCEAO' else 'https://www.beac.int/')}, data_portal_url={q(r['SOURCE_URL'])}, validation_status='VALIDATED', source_note={q(evidence)}, updated_at=now() where organization_code={q(org)};",""]
        out += [f"insert into source.endpoint(endpoint_id,endpoint_code,organization_id,scope_type,scope_code,endpoint_type,url,official_url,access_method,auth_required,file_formats,expected_frequency,last_verified_at,validation_status,source_note) select {q(sid('endpoint',r['ENDPOINT_CODE']))}::uuid,{q(r['ENDPOINT_CODE'])},organization_id,'ZONE',{q(scope)},'WEB_PAGE',{q(r['SOURCE_URL'])},{q(r['SOURCE_URL'])},'PUBLIC_WEB',false,array['HTML']::text[],'DAILY',{q(r['RETRIEVED_AT'])}::timestamptz,'VALIDATED',{q(evidence)} from ref.organization where organization_code={q(org)} on conflict(endpoint_code) do update set organization_id=excluded.organization_id,scope_type=excluded.scope_type,scope_code=excluded.scope_code,endpoint_type=excluded.endpoint_type,url=excluded.url,official_url=excluded.official_url,access_method=excluded.access_method,auth_required=excluded.auth_required,file_formats=excluded.file_formats,expected_frequency=excluded.expected_frequency,last_verified_at=excluded.last_verified_at,validation_status=excluded.validation_status,source_note=excluded.source_note,updated_at=now();",""]
        maps=[(r["RAW_MAPPING_CODE"],f"FX_{cur}_EUR_USD_RAW",r["RAW_SERIES_CODE"],"RAW_FX_SNAPSHOT"),(r["EUR_MAPPING_CODE"],f"FX_{cur}_EUR",r["EUR_SERIES_CODE"],"LOCAL_EUR_CONVERSION"),(r["USD_MAPPING_CODE"],f"FX_{cur}_USD",r["USD_SERIES_CODE"],"LOCAL_USD_CONVERSION")]
        for code,indicator,series,usage in maps:
            out += [f"insert into source.indicator_source_mapping(mapping_id,mapping_code,scope_type,scope_code,domain_code,indicator_code,organization_id,organization_role_code,endpoint_id,provider_series_code,frequency_native,unit_code,currency_code,is_primary_source,source_priority,collection_status,validation_status,usage_target,source_note) select {q(sid('map',code))}::uuid,{q(code)},'ZONE',{q(scope)},'D09',{q(indicator)},o.organization_id,'FX_REFERENCE_RATE_PROVIDER',e.endpoint_id,{q(series)},'DAILY','FX_RATE',{q(cur)},true,1,'COLLECTION_TESTED','VALIDATED',array[{q(usage)}]::text[],{q(evidence)} from ref.organization o join source.endpoint e on e.endpoint_code={q(r['ENDPOINT_CODE'])} where o.organization_code={q(org)} on conflict(mapping_code) do update set endpoint_id=excluded.endpoint_id,provider_series_code=excluded.provider_series_code,collection_status='COLLECTION_TESTED',validation_status='VALIDATED',source_note=excluded.source_note,updated_at=now();",""]
        series=[(r["RAW_SERIES_CODE"],r["RAW_MAPPING_CODE"],f"FX_{cur}_EUR_USD_RAW",r["SOURCE_URL"]),(r["EUR_SERIES_CODE"],r["EUR_MAPPING_CODE"],f"FX_{cur}_EUR","") ,(r["USD_SERIES_CODE"],r["USD_MAPPING_CODE"],f"FX_{cur}_USD","")]
        for code,mapping,indicator,url in series:
            out += [f"insert into source.provider_series(provider_series_id,provider_series_code,mapping_code,organization_id,endpoint_id,canonical_indicator_code,native_series_url,native_frequency,native_unit,native_currency_code,revision_policy,history_status,validation_status) select {q(sid('series',code))}::uuid,{q(code)},{q(mapping)},o.organization_id,e.endpoint_id,{q(indicator)},{q(url) if url else 'null'},'DAILY','FX_RATE',{q(cur)},'KEEP_ALL_REVISIONS','COLLECTION_TESTED','VALIDATED' from ref.organization o join source.endpoint e on e.endpoint_code={q(r['ENDPOINT_CODE'])} where o.organization_code={q(org)} on conflict(provider_series_code) do update set mapping_code=excluded.mapping_code,organization_id=excluded.organization_id,endpoint_id=excluded.endpoint_id,canonical_indicator_code=excluded.canonical_indicator_code,native_series_url=excluded.native_series_url,history_status='COLLECTION_TESTED',validation_status='VALIDATED',updated_at=now();",""]
        specs=[(r["RAW_SPEC_CODE"],r["RAW_SERIES_CODE"],"HTML_SNAPSHOT",r["SELECTOR"],r["QUALITY_PROFILE"]),(r["EUR_SPEC_CODE"],r["EUR_SERIES_CODE"],"DERIVED_FROM_VALIDATED_SNAPSHOT","PROVIDER_BUY_SELL_FROM_SHARED_SNAPSHOT","FX_BUY_SELL_DATE_SHA256_AND_LINEAGE_CHECKS"),(r["USD_SPEC_CODE"],r["USD_SERIES_CODE"],"DERIVED_FROM_VALIDATED_SNAPSHOT","PROVIDER_BUY_SELL_FROM_SHARED_SNAPSHOT","FX_BUY_SELL_DATE_SHA256_AND_LINEAGE_CHECKS")]
        for code,series_code,method,selector,quality in specs:
            out += [f"insert into source.collection_specification(collection_specification_id,collection_specification_code,provider_series_id,collection_method,request_method,discovery_rule,table_or_selector,date_extraction_rule,value_extraction_rule,number_parsing_rule,currency_rule,frequency_check,deduplication_key,revision_handling,raw_artifact_required,hash_required,parser_version,retry_policy,quality_check_profile,implementation_status,validation_status) select {q(sid('spec',code))}::uuid,{q(code)},provider_series_id,{q(method)},'GET','USE_GOVERNED_VALIDATED_FX_REGISTRY',{q(selector)},'SOURCE_VALUE_DATE','PRESERVE_BUY_SELL_AND_INVERT_MIDPOINT','LOCALE_AWARE_DECIMAL',{q(cur+'_TO_EUR_USD_WITH_LINEAGE')},'DAILY_BUSINESS_DAY_CHECK','RAW_SHA256|VALUE_DATE|SERIES','KEEP_ALL_REVISIONS',true,true,{q(r['PARSER_VERSION'])},'STANDARD_BACKOFF',{q(quality)},'COLLECTION_TESTED','VALIDATED' from source.provider_series where provider_series_code={q(series_code)} on conflict(collection_specification_code) do update set provider_series_id=excluded.provider_series_id,collection_method=excluded.collection_method,table_or_selector=excluded.table_or_selector,parser_version=excluded.parser_version,quality_check_profile=excluded.quality_check_profile,implementation_status='COLLECTION_TESTED',validation_status='VALIDATED',updated_at=now();",""]
    out += ["-- Snapshot pilots only: no PARTIAL_HISTORY_LOADED or COMPLETE_HISTORY_LOADED claim.",""]
    return "\n".join(out)

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--source",type=Path,default=DEFAULT_SOURCE); p.add_argument("--output",type=Path,default=DEFAULT_OUTPUT); p.add_argument("--check",action="store_true"); a=p.parse_args(); generated=render(a.source)
    if a.check:
        if not a.output.exists() or a.output.read_text(encoding="utf-8")!=generated: raise SystemExit("generated SQL differs from governed registry")
        print(f"OK: {a.output} is synchronized"); return 0
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(generated,encoding="utf-8",newline="\n"); print(a.output); return 0
if __name__=="__main__": raise SystemExit(main())
