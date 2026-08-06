"""Canonical field dictionary package expansion and rendering helpers."""
from __future__ import annotations
import csv, hashlib, json, re
from collections import Counter, defaultdict
from io import StringIO
from pathlib import Path
from typing import Any

FIELD_ID_RE=re.compile(r"^OF_[A-Z0-9_]+$")
TECHNICAL_NAME_RE=re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")
PK_BY_TABLE={"entity":"entity_id","entity_state":"entity_state_id","fund_profile":"fund_profile_id","subfund_profile":"subfund_profile_id","share_class_profile":"share_class_profile_id","entity_event":"event_id","event_participant":"event_participant_id","entity_name":"entity_name_id","entity_identifier":"entity_identifier_id","structure_relationship":"structure_relationship_id"}
TABLE_FILES=("10_tables_identity.json","11_tables_profiles_events.json","12_tables_names_identifiers_structure.json")
SEMANTIC_FILES=("20_column_semantics.json","21_column_semantics.json","22_column_semantics.json")
PACKAGE_FILES=("00_metadata.json",)+TABLE_FILES+SEMANTIC_FILES+("30_allowed_values.json","31_foreign_keys.json")

def load_json(path:Path)->dict[str,Any]:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict): raise ValueError(f"{path} root must be an object")
    return value

def load_package(path:Path)->dict[str,Any]:
    missing=[name for name in PACKAGE_FILES if not (path/name).is_file()]
    if missing: raise ValueError(f"dictionary package files missing: {missing}")
    spec=load_json(path/"00_metadata.json")
    spec["tables"]={}
    for name in TABLE_FILES:
        for key,value in load_json(path/name).items():
            if key in spec["tables"]: raise ValueError(f"duplicate table definition: {key}")
            spec["tables"][key]=value
    spec["column_semantics"]={}
    for name in SEMANTIC_FILES:
        for key,value in load_json(path/name).items():
            if key in spec["column_semantics"]: raise ValueError(f"duplicate semantic definition: {key}")
            spec["column_semantics"][key]=value
    spec["allowed_values"]=load_json(path/"30_allowed_values.json")
    spec["foreign_keys"]=load_json(path/"31_foreign_keys.json")
    return spec

def package_sha256(path:Path)->str:
    h=hashlib.sha256()
    for name in PACKAGE_FILES:
        payload=(path/name).read_bytes(); h.update(name.encode()); h.update(b"\0"); h.update(payload); h.update(b"\0")
    return h.hexdigest()

def expected_columns(spec:dict[str,Any])->dict[str,tuple[str,...]]:
    return {table:tuple(c["name"] for c in value["columns"]) for table,value in spec["tables"].items()}

def data_type(pg_type:str)->str:
    return {"uuid":"UUID","text":"TEXT","date":"DATE","timestamptz":"TIMESTAMPTZ","boolean":"BOOLEAN","jsonb":"JSON_OBJECT"}[pg_type]

def field_format(pg_type:str,column:str)->str:
    if pg_type=="uuid": return "UUID_RFC_4122"
    if pg_type=="date": return "ISO_8601_DATE"
    if pg_type=="timestamptz": return "ISO_8601_TIMESTAMP_WITH_TIMEZONE"
    if pg_type=="boolean": return "TRUE_FALSE"
    if pg_type=="jsonb": return "JSON_OBJECT"
    if column=="language_code": return "BCP_47_OR_UND"
    if column in {"canonical_code","legal_form_code"}: return "UPPERCASE_ASCII_CODE"
    return "UTF_8_TEXT"

def constraints(spec:dict[str,Any],table:str,column:str,nullable:bool)->list[str]:
    values=[]
    if not nullable: values.append("NOT_NULL")
    if PK_BY_TABLE.get(table)==column: values.append("PRIMARY_KEY")
    if fk:=spec.get("foreign_keys",{}).get(f"{table}.{column}"): values.append(fk)
    if column=="canonical_code": values += ["UNIQUE","REGEX ^[A-Z0-9][A-Z0-9_:-]*$"]
    if column=="legal_form_code": values.append("REGEX ^[A-Z0-9][A-Z0-9_:-]*$")
    if column in {"name_text","normalized_name","identifier_value","normalized_value","event_summary"}: values.append("NON_BLANK")
    if table=="event_participant" and column in {"entity_id","organization_id"}: values.append("EXACTLY_ONE_OF_ENTITY_ID_OR_ORGANIZATION_ID")
    if table=="structure_relationship" and column in {"parent_entity_id","child_entity_id"}: values.append("PARENT_AND_CHILD_MUST_DIFFER")
    return list(dict.fromkeys(values))

def validation_rule(table:str,column:str)->str:
    if column in {"effective_from","effective_to","effective_date"}: return "DATE_VALUE_MUST_MATCH_KNOWLEDGE_STATUS"
    if column in {"effective_from_status","effective_to_status","effective_date_status"}: return "ENUM_AND_DATE_COUPLING_CHECK"
    if column=="is_current": return "CURRENT_REQUIRES_SUPERSEDED_AT_NULL"
    if column=="superseded_at": return "NON_CURRENT_REQUIRES_SUPERSEDED_AT_NOT_NULL"
    if column=="validation_status": return "ENUM_CHECK_AND_CURRENT_VIEW_FILTER"
    if column=="canonical_code": return "UNIQUE_UPPERCASE_TECHNICAL_CODE"
    if column=="normalized_name": return "NON_BLANK_NORMALIZED_MATCHING_FORM"
    if column=="normalized_value": return "NON_BLANK_AND_CURRENT_SCHEME_UNIQUENESS"
    if column=="relationship_type": return "TYPE_PAIR_AND_STRUCTURE_TRIGGER_CHECK"
    if table=="event_participant" and column in {"entity_id","organization_id"}: return "EXACTLY_ONE_PARTICIPANT_TARGET"
    return "POSTGRESQL_CONSTRAINTS_AND_DOMAIN_REVIEW"

def normalization_rule(pg_type:str,column:str)->str:
    if column in {"canonical_code","legal_form_code"}: return "TRIM;UPPERCASE;REMOVE_ACCENTS;NORMALIZE_SEPARATORS_TO_UNDERSCORE"
    if column=="normalized_name": return "TRIM;UNICODE_NORMALIZE;UPPERCASE;REMOVE_ACCENTS;COLLAPSE_WHITESPACE"
    if column=="normalized_value": return "TRIM;UPPERCASE;REMOVE_SCHEME_FORMATTING"
    if column=="language_code": return "LOWERCASE_BCP47_OR_UND"
    if pg_type=="text": return "TRIM;PRESERVE_SOURCE_TEXT_UNLESS_EXPLICITLY_NORMALIZED"
    if pg_type=="jsonb": return "VALID_JSON_OBJECT;PRESERVE_SOURCE_COORDINATES"
    return "NO_LOSSY_NORMALIZATION"

def example_value(column:str,pg_type:str)->str:
    examples={"entity_id":"10000000-0000-0000-0000-000000000001","entity_type":"FUND","canonical_code":"MA_FUND_EXAMPLE_001","created_at":"2026-08-06T12:00:00Z","retired_at":"2028-12-31T23:59:59Z","lifecycle_status":"ACTIVE","domicile_country_id":"20000000-0000-0000-0000-000000000504","effective_from":"2020-01-15","effective_from_status":"KNOWN","effective_to":"2026-12-31","effective_to_status":"NOT_APPLICABLE","recorded_at":"2026-08-06T12:00:00Z","superseded_at":"2026-08-07T08:00:00Z","is_current":"true","validation_status":"VALIDATED","source_artifact_id":"30000000-0000-0000-0000-000000000001","source_locator":'{"page":12,"section":"Identification"}',"source_note":"Prospectus officiel vérifié","structure_type":"STANDALONE","legal_form_code":"SICAV","has_legal_personality":"true","base_currency_id":"4000000-0000-0000-00000-000000000504","compartment_type":"COMPARTMENT","currency_id":"40000000-0000-0000-0000-000000000566","distribution_policy":"ACCUMULATING","hedging_policy":"UNHEDGED","nav_frequency":"DAILY","is_representative":"true","event_type":"RENAME","effective_date":"2024-03-01","effective_date_status":"KNOWN","publication_date":"2024-02-20","event_summary":"Changement de dénomination approuvé","participant_role":"SUBJECT","note":"Entité concernée","name_role":"LEGAL_NAME","name_text":"Exemple Fonds Monétaire","normalized_name":"EXEMPLE FONDS MONETAIRE","language_code":"fr","identifier_scheme":"ISIN","identifier_value":"CI0000000001","normalized_value":"CI0000000001","relationship_type":"FUND_HAS_SHARE_CLASS","parent_entity_type":"FUND","child_entity_type":"SHARE_CLASS"}
    if column in examples: return examples[column]
    if pg_type=="uuid": return "50000000-0000-0000-0000-000000000001"
    if pg_type=="boolean": return "false"
    if pg_type=="jsonb": return "{}"
    if pg_type=="date": return "2026-08-06"
    if pg_type=="timestamptz": return "2026-08-06T12:00:00Z"
    return f"EXAMPLE_{column.upper()}"

def expand(spec:dict[str,Any])->list[dict[str,Any]]:
    errors=[]; fields=[]; required=spec["required_attributes"]; defaults=spec["defaults"]
    if len(spec["tables"])!=10: errors.append(f"expected 10 tables, got {len(spec['tables'])}")
    for table,table_spec in spec["tables"].items():
        entity_code=table_spec["ENTITY_CODE"]
        for definition in table_spec["columns"]:
            column,pg_type,nullable=definition["name"],definition["pg_type"],definition["nullable"]
            semantic=spec["column_semantics"].get(column)
            if not semantic: errors.append(f"semantic definition missing: {column}"); continue
            external={"openfunds_mapping_status":"NOT_MAPPED_OFFICIAL_CATALOGUE_UNAVAILABLE"}
            if column in {"domicile_country_id"}: external["reference"]="ISO_3166_1_ALPHA_2_VIA_REF_GEOGRAPHY"
            if column in {"base_currency_id","currency_id"}: external["reference"]="ISO_4217_VIA_REF_CURRENCY"
            if column=="identifier_scheme": external["standards"]=["ISO_6166_ISIN","ISO_17442_LEI","LOCAL_REGULATOR_SCHEMES"]
            source_role="CANONICAL_SYSTEM" if table=="entity" else "OFFICIAL_REGULATOR_OR_FUND_DOCUMENT"
            field=dict(defaults); field.update(semantic); field.update({"FIELD_ID":f"OF_FUND_{entity_code}_{column.upper()}","TECHNICAL_NAME":f"fund.{table}.{column}","DOMAIN_CODE":"FUND","ENTITY_CODE":entity_code,"DATA_TYPE":data_type(pg_type),"FORMAT":field_format(pg_type,column),"CURRENCY_RULE":"REFERENCE_TO_REF_CURRENCY" if column in {"base_currency_id","currency_id"} else "NOT_APPLICABLE","NULLABILITY":"OPTIONAL" if nullable else "REQUIRED","CARDINALITY":"0..1" if nullable else "1","ALLOWED_VALUES":spec.get("allowed_values",{}).get(f"{table}.{column}",[]),"CONSTRAINTS":constraints(spec,table,column,nullable),"VALIDATION_RULE":validation_rule(table,column),"NORMALIZATION_RULE":normalization_rule(pg_type,column),"SOURCE_ROLE":source_role,"SOURCE_PRIORITY_RULE":"CANONICAL_SYSTEM_ASSIGNMENT" if source_role=="CANONICAL_SYSTEM" else "OFFICIAL_REGULATOR > OFFICIAL_FUND_DOCUMENT > MANAGEMENT_COMPANY > OTHER_VERIFIED_SOURCE","HISTORY_METHOD":table_spec["HISTORY_METHOD"],"EXTERNAL_MAPPINGS":external,"EXAMPLE_VALUE":example_value(column,pg_type),"PHYSICAL_TABLE":table,"PHYSICAL_COLUMN":column})
            missing=[name for name in required if name not in field]
            if missing: errors.append(f"{table}.{column}: missing {missing}")
            fields.append(field)
    ids=Counter(r["FIELD_ID"] for r in fields); names=Counter(r["TECHNICAL_NAME"] for r in fields)
    if dup:=[v for v,n in ids.items() if n>1]: errors.append(f"duplicate FIELD_ID: {dup}")
    if dup:=[v for v,n in names.items() if n>1]: errors.append(f"duplicate TECHNICAL_NAME: {dup}")
    if len(fields)!=143: errors.append(f"expected 143 fields, got {len(fields)}")
    for field in fields:
        if not FIELD_ID_RE.fullmatch(str(field["FIELD_ID"])): errors.append(f"invalid FIELD_ID: {field['FIELD_ID']}")
        if not TECHNICAL_NAME_RE.fullmatch(str(field["TECHNICAL_NAME"])): errors.append(f"invalid TECHNICAL_NAME: {field['TECHNICAL_NAME']}")
        if field.get("OPENFUNDS_FIELD_ID") is not None: errors.append(f"{field['FIELD_ID']}: Openfunds ID must remain null")
        if field.get("EXTERNAL_MAPPINGS",{}).get("openfunds_mapping_status")!="NOT_MAPPED_OFFICIAL_CATALOGUE_UNAVAILABLE": errors.append(f"{field['FIELD_ID']}: explicit Openfunds non-mapping status missing")
    if errors: raise ValueError("\n".join(errors))
    return sorted(fields,key=lambda r:(r["PHYSICAL_TABLE"],r["PHYSICAL_COLUMN"]))

def render_expanded_json(spec:dict[str,Any],fields:list[dict[str,Any]])->str:
    return json.dumps({"dictionary_id":spec["dictionary_id"],"dictionary_version":spec["dictionary_version"],"status":spec["status"],"generated_from":spec["authoritative_path"],"field_count":len(fields),"fields":fields},ensure_ascii=False,indent=2)+"\n"

def render_csv(required:list[str],fields:list[dict[str,Any]])->str:
    output=StringIO(); writer=csv.DictWriter(output,fieldnames=required,delimiter=";",lineterminator="\n"); writer.writeheader()
    for field in fields:
        row={}
        for name in required:
            value=field[name]
            if isinstance(value,(list,dict)): value=json.dumps(value,ensure_ascii=False,separators=(",",":"),sort_keys=True)
            elif value is None: value=""
            row[name]=str(value)
        writer.writerow(row)
    return output.getvalue()

def render_markdown(spec:dict[str,Any],fields:list[dict[str,Any]])->str:
    lines=["# Dictionnaire canonique des champs — Fund / SubFund / ShareClass v1","","> Vue humaine générée depuis le paquet `data/dictionary/spec_v1/`. Ne pas modifier un artefact de build directement.","","## Statut","","```text","TASK: OF-DATA-002","SCOPE: CANONICAL_FUND_CORE",f"STATUS: {spec['status']}",f"DICTIONARY_VERSION: {spec['dictionary_version']}",f"FIELD_COUNT: {len(fields)}","OPENFUNDS_MAPPING: NOT_MAPPED_OFFICIAL_CATALOGUE_UNAVAILABLE","```","","## Principes","","- Chaque champ physique de `fund.*` introduit par la migration gouvernée `015` possède une définition complète et un identifiant stable.","- `NULL`, `UNKNOWN` et `NOT_APPLICABLE` restent distincts.","- Les noms publiés, noms normalisés, identifiants, profils, relations et événements restent séparés.","- Aucun identifiant Openfunds n’est inventé.","- Le CSV généré utilise le séparateur `;`.",""]
    by_table=defaultdict(list)
    for field in fields: by_table[field["PHYSICAL_TABLE"]].append(field)
    for table,table_spec in spec["tables"].items():
        lines += [f"## {table_spec['ENTITY_CODE']} — `fund.{table}`","",f"{table_spec['DESCRIPTION_FR']} Historisation : `{table_spec['HISTORY_METHOD']}`.","","| FIELD_ID | Colonne | Type | Nullabilité | Définition | Valeurs autorisées |","|---|---|---|---|---|---|"]
        for field in by_table[table]:
            allowed=", ".join(field["ALLOWED_VALUES"]) if field["ALLOWED_VALUES"] else "—"; definition=str(field["DEFINITION"]).replace("|","\\|")
            lines.append(f"| `{field['FIELD_ID']}` | `{field['PHYSICAL_COLUMN']}` | `{field['DATA_TYPE']}` | `{field['NULLABILITY']}` | {definition} | {allowed} |")
        lines.append("")
    lines += ["## Limites explicites","","Ce catalogue est complet pour le schéma canonique `fund.*` courant. Il ne prétend pas encore couvrir les colonnes physiques `ref.*`, `source.*`, `market.*`, le catalogue D00–D17, ni un mapping officiel Openfunds.",""]
    return "\n".join(lines)

def build(spec:dict[str,Any])->dict[str,str]:
    fields=expand(spec); return {"expanded_json":render_expanded_json(spec,fields),"csv":render_csv(spec["required_attributes"],fields),"markdown":render_markdown(spec,fields)}

def sha256_text(value:str)->str: return hashlib.sha256(value.encode("utf-8")).hexdigest()
