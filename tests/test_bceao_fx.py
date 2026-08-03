from pathlib import Path
import unittest

from collectors.bceao_fx import normalize_decimal, parse_bceao_fx_html


FIXTURE = Path(__file__).parent / "fixtures" / "bceao_fx_sample.html"


class BceaoFxParserTests(unittest.TestCase):
    def test_parse_expected_currencies_and_value_date(self) -> None:
        observations, warnings = parse_bceao_fx_html(FIXTURE.read_bytes())
        by_code = {item.canonical_currency_code: item for item in observations}

        self.assertEqual([], warnings)
        self.assertEqual("2026-08-03", by_code["EUR"].value_date)
        self.assertEqual("655.957", by_code["EUR"].provider_buy_rate)
        self.assertEqual("655.957", by_code["EUR"].provider_sell_rate)
        self.assertEqual("570.125", by_code["USD"].provider_buy_rate)
        self.assertEqual("575.875", by_code["USD"].provider_sell_rate)
        self.assertEqual("XOF_PER_1_FOREIGN_CURRENCY", by_code["USD"].quote_convention_source)

    def test_numeric_parser_handles_localized_formats(self) -> None:
        self.assertEqual("1234.56", normalize_decimal("1 234,56"))
        self.assertEqual("1234.56", normalize_decimal("1,234.56"))
        self.assertEqual("1234.56", normalize_decimal("1.234,56"))

    def test_numeric_parser_rejects_zero_and_missing(self) -> None:
        with self.assertRaises(ValueError):
            normalize_decimal("")
        with self.assertRaises(ValueError):
            normalize_decimal("0")


if __name__ == "__main__":
    unittest.main()
