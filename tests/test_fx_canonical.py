import unittest

from collectors.fx_canonical import transform_xof_manifest


class CanonicalFxTransformationTests(unittest.TestCase):
    def _manifest(self) -> dict:
        return {
            "parser_version": "0.2.0",
            "raw_artifact": {
                "sha256": "ABC123",
                "source_url": "https://www.bceao.int/fr",
            },
            "observations": [
                {
                    "canonical_currency_code": "EUR",
                    "provider_currency_label": "Euro",
                    "provider_buy_rate": "655.957",
                    "provider_sell_rate": "655.957",
                    "quote_convention_source": "XOF_PER_1_FOREIGN_CURRENCY",
                    "value_date": "2026-07-31",
                },
                {
                    "canonical_currency_code": "USD",
                    "provider_currency_label": "Dollar us",
                    "provider_buy_rate": "566.250",
                    "provider_sell_rate": "573.250",
                    "quote_convention_source": "XOF_PER_1_FOREIGN_CURRENCY",
                    "value_date": "2026-07-31",
                },
                {
                    "canonical_currency_code": "GBP",
                    "provider_currency_label": "Livre sterling",
                    "provider_buy_rate": "762.750",
                    "provider_sell_rate": "769.750",
                    "quote_convention_source": "XOF_PER_1_FOREIGN_CURRENCY",
                    "value_date": "2026-07-31",
                },
            ],
        }

    def test_transforms_required_pairs_with_lineage(self) -> None:
        observations = transform_xof_manifest(self._manifest())
        by_pair = {item.canonical_pair_code: item for item in observations}

        self.assertEqual({"XOF_EUR", "XOF_USD"}, set(by_pair))
        self.assertEqual("0.001524490172374104", by_pair["XOF_EUR"].canonical_rate)
        self.assertEqual("655.957000000000000000", by_pair["XOF_EUR"].source_midpoint)
        self.assertEqual("0.001755155770074594", by_pair["XOF_USD"].canonical_rate)
        self.assertEqual("569.750000000000000000", by_pair["XOF_USD"].source_midpoint)
        self.assertEqual("2026-07-31", by_pair["XOF_USD"].value_date)
        self.assertEqual("ABC123", by_pair["XOF_USD"].source_raw_sha256)
        self.assertEqual("0.2.0", by_pair["XOF_USD"].source_parser_version)
        self.assertEqual(
            "1 / ((PROVIDER_BUY_RATE + PROVIDER_SELL_RATE) / 2)",
            by_pair["XOF_USD"].transformation_formula,
        )

    def test_rejects_missing_value_date(self) -> None:
        manifest = self._manifest()
        manifest["observations"][0]["value_date"] = None
        with self.assertRaisesRegex(ValueError, "missing value_date"):
            transform_xof_manifest(manifest)

    def test_rejects_wrong_quote_direction(self) -> None:
        manifest = self._manifest()
        manifest["observations"][0]["quote_convention_source"] = "FOREIGN_PER_1_XOF"
        with self.assertRaisesRegex(ValueError, "unexpected quote convention"):
            transform_xof_manifest(manifest)

    def test_rejects_duplicate_required_pair(self) -> None:
        manifest = self._manifest()
        manifest["observations"].append(dict(manifest["observations"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate provider row"):
            transform_xof_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
