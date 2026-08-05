from pathlib import Path
import unittest

from collectors.beac_fx import parse_beac_fx_html, rows_to_observations


FIXTURE = Path(__file__).parent / "fixtures" / "beac_fx_sample.html"


class BeacFxParserTests(unittest.TestCase):
    def test_parse_expected_pairs_and_value_date(self) -> None:
        observations, warnings = parse_beac_fx_html(FIXTURE.read_bytes())
        by_code = {item.canonical_currency_code: item for item in observations}

        self.assertEqual([], warnings)
        self.assertEqual("2026-07-14", by_code["EUR"].value_date)
        self.assertEqual("EUR/XAF", by_code["EUR"].provider_currency_label)
        self.assertEqual("655.957", by_code["EUR"].provider_buy_rate)
        self.assertEqual("655.957", by_code["EUR"].provider_sell_rate)
        self.assertEqual("571.0072", by_code["USD"].provider_buy_rate)
        self.assertEqual("575.9103", by_code["USD"].provider_sell_rate)
        self.assertEqual("XAF_PER_1_FOREIGN_CURRENCY", by_code["USD"].quote_convention_source)

    def test_pair_label_whitespace_is_normalized(self) -> None:
        observations = rows_to_observations(
            [[" EUR / XAF ", "655.957", "655.957"]],
            "2026-07-14",
        )
        self.assertEqual(1, len(observations))
        self.assertEqual("EUR", observations[0].canonical_currency_code)

    def test_reverse_or_unknown_pair_is_not_silently_accepted(self) -> None:
        observations = rows_to_observations(
            [
                ["XAF/EUR", "0.0015", "0.0016"],
                ["ABC/XAF", "10", "11"],
            ],
            "2026-07-14",
        )
        self.assertEqual([], observations)


if __name__ == "__main__":
    unittest.main()
