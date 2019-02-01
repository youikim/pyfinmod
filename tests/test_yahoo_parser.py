from datetime import datetime
import pytest
import pandas as pd
from pyfinmod.yahoo_finance import YahooFinanceParser, YahooParserError


def test_int_parser():
    assert YahooFinanceParser._int_parse('-48,995,000') == -48995000000


def test_date_parser():
    assert YahooFinanceParser._date_parse('9/29/2018') == datetime(2018, 9, 29, 0, 0)


def test_get_balance_sheet():
    with open('./raw_data/aapl_balance_sheet.txt', 'r') as f:
        html = f.read()

    parser = YahooFinanceParser('AAPL', 'balance-sheet')
    df = parser.get_dataframe(html)
    assert not df.empty
    df_test = pd.read_hdf('./raw_data/aapl_balance_sheet.hd5', key='aapl_balance_sheet')
    assert df.equals(df_test)


def test_wrong_ticker():
    with open('./raw_data/empty_html.txt', 'w+') as f:
        html = f.read()
    parser = YahooFinanceParser('123123123', 'balance-sheet')
    with pytest.raises(YahooParserError):
        df = parser.get_dataframe(html)
        assert not df


def test_get_income_statement():
    with open('./raw_data/aapl_income_statement.txt', 'r') as f:
        html = f.read()

    parser = YahooFinanceParser('AAPL', 'income-statement')
    df = parser.get_dataframe()
    assert not df.empty

    df_test = pd.read_hdf('./raw_data/aapl_income_statement.hd5', key='aapl_income_statement')
    assert df.equals(df_test)


def test_get_cash_flow():
    with open('./raw_data/aapl_cash_flow.txt', 'r') as f:
        html = f.read()

    parser = YahooFinanceParser('AAPL', 'cash-flow')
    df = parser.get_dataframe(html)
    assert not df.empty

    df_test = pd.read_hdf('./raw_data/aapl_cash_flow.hd5', key='aapl_cash_flow')
    assert df.equals(df_test)