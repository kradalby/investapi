from absl.testing import absltest, parameterized

import morningstar


class MorningstarTests(parameterized.TestCase):
    @parameterized.parameters(
        dict(
            isin="",
            country_code="no",
            expected_morningstar_id=None,
        ),
        dict(
            # DNB Global Indeks A
            isin="NO0010582984",
            country_code="no",
            expected_morningstar_id="F00000JORS",
        ),
        dict(
            # DNB Teknologi A
            isin="no0010337678",
            country_code="no",
            expected_morningstar_id="F0GBR04NGU",
        ),
        dict(
            # Odin Eiendom C
            isin="NO0010062953",
            country_code="no",
            expected_morningstar_id="F0GBR04UQX",
        ),
        dict(
            # Fidelity China Consumer Fund W-Accumulation
            isin="GB00B82ZSC67",
            country_code="no",
            expected_morningstar_id=None,
        ),
        dict(
            isin="",
            country_code="uk",
            expected_morningstar_id=None,
        ),
        dict(
            # DNB Global Indeks A
            isin="NO0010582984",
            country_code="uk",
            expected_morningstar_id=None,
        ),
        dict(
            # Fidelity China Consumer Fund W-Accumulation
            isin="GB00B82ZSC67",
            country_code="uk",
            expected_morningstar_id="F00000OPX3",
        ),
    )
    def test_morningstar_id(
        self, isin: str, country_code: str, expected_morningstar_id: str
    ):
        id = morningstar.get_morningstar_id(isin, country_code)

        self.assertEqual(id, expected_morningstar_id)

    @parameterized.parameters(
        dict(
            isin="",
            expected=False,
        ),
        dict(
            # DNB Global Indeks A
            isin="NO0010582984",
            expected=True,
        ),
        dict(
            # DNB Teknologi A
            isin="no0010337678",
            expected=True,
        ),
        dict(
            # Odin Eiendom C
            isin="NO0010062953",
            expected=True,
        ),
        dict(
            # Fidelity China Consumer Fund W-Accumulation
            isin="GB00B82ZSC67",
            expected=False,
        ),
    )
    def test_get_fund_nor(self, isin: str, expected: bool):
        fund = morningstar.get_fund_nor(isin)

        if expected:
            self.assertEqual(fund.isin, isin)
        else:
            self.assertIsNone(fund)

    @parameterized.parameters(
        dict(
            isin="",
            expected=False,
        ),
        dict(
            # DNB Global Indeks A
            isin="NO0010582984",
            expected=False,
        ),
        dict(
            # DNB Teknologi A
            isin="no0010337678",
            expected=False,
        ),
        dict(
            # Odin Eiendom C
            isin="NO0010062953",
            expected=False,
        ),
        dict(
            # Fidelity China Consumer Fund W-Accumulation
            isin="GB00B82ZSC67",
            expected=True,
        ),
        dict(
            # Vanguard Pacific ex-Japan Stock Index Fund GBP Acc
            isin="IE00B523l313",
            expected=True,
        ),
    )
    def test_get_fund_uk(self, isin: str, expected: bool):
        fund = morningstar.get_fund_uk(isin)

        if expected:
            self.assertEqual(fund.isin, isin)
        else:
            self.assertIsNone(fund)


if __name__ == "__main__":
    absltest.main()
