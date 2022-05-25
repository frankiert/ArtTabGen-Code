from pytest_mock import MockerFixture

from arttabgen import row_builder


class TestRowBuilder:
    def test_build_1_col_kuv(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure npa 259"]

        returned = row_builder.build_1_col_kuv(key, value, unit)

        assert expected == returned

    def test_build_1_col_kvu(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure 259 npa"]

        returned = row_builder.build_1_col_kvu(key, value, unit)

        assert expected == returned

    def test_build_2_cols_square_brackets(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure, [npa]", "259"]

        returned = row_builder.build_2_cols_square_brackets(key, value, unit)

        assert expected == returned

    def test_build_2_cols_round_brackets(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure (npa)", "259"]

        returned = row_builder.build_2_cols_round_brackets(key, value, unit)

        assert expected == returned

    def test_build_2_cols_comma(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure, npa", "259"]

        returned = row_builder.build_2_cols_comma(key, value, unit)

        assert expected == returned

    def test_build_2_cols_space(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure", "259 npa"]

        returned = row_builder.build_2_cols_space(key, value, unit)

        assert expected == returned

    def test_build_3_cols_kuv(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure", "npa", "259"]

        returned = row_builder.build_3_cols_kuv(key, value, unit)

        assert expected == returned

    def test_build_3_cols_kvu(self):
        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure", "259", "npa"]

        returned = row_builder.build_3_cols_kvu(key, value, unit)

        assert expected == returned

    def test_get_random_row_by_col_no_2(self, mocker: MockerFixture):
        returned = row_builder._get_random_row_method_by_col_no(2)

        assert 2 <= returned <= 5

    def test_build_row_no_4(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.row_builder._get_random_row_method_by_col_no", return_value=4
        )

        key = "burst pressure"
        unit = "npa"
        value = "259"

        expected = ["burst pressure, npa", "259"]

        returned = row_builder.build_random_row(2, key, value, unit)

        assert returned == expected
