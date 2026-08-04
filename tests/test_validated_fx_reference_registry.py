from __future__ import annotations
import csv, importlib.util, shutil, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('fx_registry',ROOT/'scripts/generate_validated_fx_reference_sql.py')
assert SPEC and SPEC.loader
mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)
class Tests(unittest.TestCase):
    def test_render_is_deterministic(self):
        self.assertEqual(mod.render(),mod.render())
    def test_two_snapshot_pilots_only(self):
        rows=mod.load(ROOT/'data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv')
        self.assertEqual({r['PILOT_CODE'] for r in rows},{'BCEAO_XOF','BEAC_XAF'})
        sql=mod.render(); self.assertNotIn("'PARTIAL_HISTORY_LOADED'",sql); self.assertNotIn("'COMPLETE_HISTORY_LOADED'",sql)
        self.assertIn('30777722357',sql); self.assertIn('30779605759',sql)
    def test_corrupt_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'registry.csv'; shutil.copy(ROOT/'data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv',p)
            with p.open(encoding='utf-8',newline='') as h:
                rows=list(csv.DictReader(h,delimiter=';'))
            fields=list(rows[0]); rows[0]['RAW_SHA256']='BAD'
            with p.open('w',encoding='utf-8',newline='') as h:
                w=csv.DictWriter(h,fieldnames=fields,delimiter=';',lineterminator='\n'); w.writeheader(); w.writerows(rows)
            with self.assertRaises(ValueError): mod.load(p)
if __name__=='__main__': unittest.main()
