from __future__ import annotations
import csv, importlib.util, json, subprocess, sys, tempfile, unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/dictionary/spec_v1"
MANIFEST=ROOT/"data/dictionary/CANONICAL_FIELD_DICTIONARY_MANIFEST_V1.json"
SCHEMA=ROOT/"data/dictionary/canonical-field-dictionary-v1.schema.json"
MIGRATION=ROOT/"schemas/fund/015_fund_subfund_shareclass_core.sql"
CORE=ROOT/"scripts/canonical_field_dictionary.py"
GENERATOR=ROOT/"scripts/generate_canonical_field_dictionary.py"

def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError(f"cannot load {path}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def extract_table_columns(sql:str,table:str)->tuple[str,...]:
    marker=f"create table if not exists fund.{table} ("; start=sql.find(marker)
    if start<0: raise AssertionError(f"missing table declaration: fund.{table}")
    fragment=sql[start+len(marker):]; columns=[]; depth=1
    for raw_line in fragment.splitlines():
        stripped=raw_line.strip()
        if depth==1 and raw_line.startswith("    ") and stripped:
            token=stripped.split(None,1)[0].rstrip(",")
            if token not in {"check","foreign","unique","constraint","primary"} and token.replace("_","").isalnum() and token[0].isalpha(): columns.append(token)
        depth += raw_line.count("(")-raw_line.count(")")
        if depth<=0: break
    return tuple(columns)

class CanonicalFieldDictionaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core=load_module(CORE,"canonical_field_dictionary")
        cls.spec=cls.core.load_package(SOURCE); cls.fields=cls.core.expand(cls.spec)
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_authoritative_package_is_complete(self):
        self.assertEqual(set(self.core.PACKAGE_FILES),{p.name for p in SOURCE.glob("*.json")})
        self.assertEqual("JSON_PACKAGE",self.spec["authoring_format"])
        self.assertEqual(";",self.spec["governance"]["csv_delimiter"])
        self.assertEqual("NO_IDENTIFIER_INVENTED",self.spec["governance"]["openfunds_mapping_policy"])
        self.assertEqual(10,len(self.spec["tables"])); self.assertEqual(36,len(self.spec["required_attributes"]))
        self.assertEqual(143,sum(len(v["columns"]) for v in self.spec["tables"].values()))

    def test_logical_json_schema_matches_the_governed_package(self):
        schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual("JSON_PACKAGE",schema["properties"]["authoring_format"]["const"])
        self.assertEqual("data/dictionary/spec_v1/",schema["properties"]["authoritative_path"]["const"])
        self.assertEqual("VALIDATED_FUND_CORE_SCOPE",schema["properties"]["status"]["const"])
        self.assertTrue(set(schema["required"]).issubset(self.spec))
        self.assertEqual(10,schema["properties"]["tables"]["minProperties"])
        self.assertEqual(10,schema["properties"]["tables"]["maxProperties"])

    def test_expansion_has_complete_unique_contract(self):
        self.assertEqual(143,len(self.fields)); required=set(self.spec["required_attributes"])
        self.assertTrue(all(set(field)==required for field in self.fields))
        self.assertTrue(all(n==1 for n in Counter(f["FIELD_ID"] for f in self.fields).values()))
        self.assertTrue(all(n==1 for n in Counter(f["TECHNICAL_NAME"] for f in self.fields).values()))

    def test_dictionary_matches_migration_015_exactly(self):
        sql=MIGRATION.read_text(encoding="utf-8"); expected=self.core.expected_columns(self.spec)
        for table,columns in expected.items():
            self.assertEqual(columns,extract_table_columns(sql,table),table)
            self.assertEqual(set(columns),{f["PHYSICAL_COLUMN"] for f in self.fields if f["PHYSICAL_TABLE"]==table},table)

    def test_no_official_openfunds_identifier_is_invented(self):
        self.assertTrue(all(f["OPENFUNDS_FIELD_ID"] is None for f in self.fields))
        self.assertTrue(all(f["EXTERNAL_MAPPINGS"]["openfunds_mapping_status"]=="NOT_MAPPED_OFFICIAL_CATALOGUE_UNAVAILABLE" for f in self.fields))

    def test_manifest_and_generated_artifacts_are_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            completed=subprocess.run([sys.executable,str(GENERATOR),"--output-dir",temp,"--check-manifest"],cwd=ROOT,text=True,capture_output=True,check=False)
            self.assertEqual(0,completed.returncode,completed.stdout+completed.stderr); self.assertIn("fields=143",completed.stdout)
            output=Path(temp); expanded=json.loads((output/"CANONICAL_FIELD_DICTIONARY_V1.json").read_text(encoding="utf-8"))
            self.assertEqual(143,expanded["field_count"]); self.assertEqual(self.fields,expanded["fields"])
            with (output/"CANONICAL_FIELD_DICTIONARY_V1.csv").open(encoding="utf-8",newline="") as handle:
                reader=csv.DictReader(handle,delimiter=";"); rows=list(reader)
            self.assertEqual(self.spec["required_attributes"],reader.fieldnames); self.assertEqual(143,len(rows))
            markdown=(output/"CANONICAL_FIELD_DICTIONARY_V1.md").read_text(encoding="utf-8")
            self.assertIn("FIELD_COUNT: 143",markdown); self.assertIn("ne prétend pas encore couvrir",markdown)

    def test_package_hash_matches_manifest(self):
        self.assertEqual(self.manifest["checksums"]["authoritative_package_sha256"],self.core.package_sha256(SOURCE))

if __name__=="__main__": unittest.main()
