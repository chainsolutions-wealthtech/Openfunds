import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "dictionary" / "extensions" / "entity_lifecycle_phase_v1"


class EntityLifecyclePhaseDictionaryExtensionTests(unittest.TestCase):
    def test_extension_contains_one_additive_field(self):
        metadata = json.loads((EXT / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(1, metadata["field_count"])
        self.assertEqual(1, len(fields))
        field = fields[0]
        self.assertEqual("OF_FUND_FUND_ENTITY_STATE_LIFECYCLE_PHASE", field["field_id"])
        self.assertEqual("fund", field["physical_schema"])
        self.assertEqual("entity_state", field["physical_table"])
        self.assertEqual("lifecycle_phase", field["physical_column"])
        self.assertIn("DORMANT", field["allowed_values"])
        self.assertIn("IN_LIQUIDATION", field["allowed_values"])


if __name__ == "__main__":
    unittest.main()
