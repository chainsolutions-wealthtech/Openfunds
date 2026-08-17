import unittest


class OpenfundsV2130ParserContractTests(unittest.TestCase):
    def setUp(self):
        from scripts.parse_openfunds_v2_13_0 import parse_records_from_layout_text
        self.parse_records_from_layout_text = parse_records_from_layout_text

    def test_parses_concrete_and_country_template_ids_without_mutation(self):
        fixture = """
OF-ID         OFST001000      Field Name    Fund Group Name
Field Tags    Essential
Field Level   Company                                                     Link Reference
Data Type     string                                               Introduced / Revoked     0.86 /    --
Description Overall brand name of the fund company.
Values
Example       UBS

OF-ID         OFST6010XX      Field Name     Country Registration Date
Field Tags    Full
Field Level   Share Class                                                 Link Reference
Data Type     date                                                 Introduced / Revoked     1.00 /    --
Description Registration date in the country represented by XX.
Values
Example       2026-01-01

OF-ID         OFNW6000XX         Field Name   News Publication Country
Field Tags    Additional
Field Level   Fund                                                        Link Reference
Data Type     string                                               Introduced / Revoked     2.00 /    --
Description Country parameter template.
Values        ISO country code
Example       CH
""".strip()

        records = self.parse_records_from_layout_text(fixture)
        self.assertEqual(3, len(records))
        self.assertEqual(
            ["OFST001000", "OFST6010XX", "OFNW6000XX"],
            [record["of_id"] for record in records],
        )
        self.assertEqual("Fund Group Name", records[0]["field_name"])
        self.assertEqual("Country Registration Date", records[1]["field_name"])
        self.assertEqual("News Publication Country", records[2]["field_name"])
        self.assertTrue(records[1]["is_parameterized_country_template"])
        self.assertTrue(records[2]["is_parameterized_country_template"])
        self.assertFalse(records[0]["is_parameterized_country_template"])

    def test_preserves_wrapped_field_name_before_field_tags(self):
        fixture = """
OF-ID         OFCA010230      Field Name     Corporate Action Securities Proceeds Applied Price or
                                      Conversion Factor
Field Tags    Full
Field Level   Share Class                                                 Link Reference
Data Type     number                                               Introduced / Revoked     2.10 /    --
Description Example wrapped field name.
Values
Example
""".strip()
        records = self.parse_records_from_layout_text(fixture)
        self.assertEqual(1, len(records))
        self.assertEqual(
            "Corporate Action Securities Proceeds Applied Price or Conversion Factor",
            records[0]["field_name"],
        )

    def test_rejects_duplicate_ids(self):
        fixture = """
OF-ID         OFST001000      Field Name    Fund Group Name
Field Tags    Essential
Field Level   Company
Data Type     string
Description A
Values
Example A
OF-ID         OFST001000      Field Name    Duplicate
Field Tags    Essential
Field Level   Company
Data Type     string
Description B
Values
Example B
""".strip()
        with self.assertRaisesRegex(ValueError, "duplicate Openfunds OF-ID"):
            self.parse_records_from_layout_text(fixture)

    def test_rejects_malformed_field_record_header(self):
        fixture = """
OF-ID         OFST6010XY      Field Name    Invalid Country Template
Field Tags    Full
Field Level   Share Class
Data Type     date
Description Invalid template suffix.
Values
Example
""".strip()
        with self.assertRaisesRegex(ValueError, "malformed Openfunds field header"):
            self.parse_records_from_layout_text(fixture)


if __name__ == "__main__":
    unittest.main()
