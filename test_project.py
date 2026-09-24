import pytest
from project import black_scholes, binomial_price, monte_carlo_price, implied_volatility, valid_input, compare_methods

def test_black_scholes():
    assert black_scholes(100, 105, 1, 0.04, 0.20, "call") == pytest.approx(7.5670, abs=0.0001)

def test_binomial_price():
    assert binomial_price(100, 105, 1, 0.04, 0.20, 10, "call") == pytest.approx(7.7278, abs=0.001)
    with pytest.raises(ValueError):
        binomial_price(100, 105, 1, 0.04, 0.20, 5, "call")

def test_monte_carlo_price():
    with pytest.raises(ValueError):
        monte_carlo_price(100, 105, 1, 0.04, 0.20, 500, "call")


def test_implied_volatility():
    market_price = black_scholes(100, 105, 1, 0.04, 0.20, "call")
    assert implied_volatility(100, 105, 1, 0.04, market_price, "call") == pytest.approx(0.20, abs=0.0001)

def test_valid_input():
    with pytest.raises(ValueError):
        valid_input(-100, 105, 1, 0.20, "call")

    with pytest.raises(ValueError):
        valid_input(100, 105, -1, 0.20, "call")

    with pytest.raises(ValueError):
        valid_input(100, 105, 1, 0.20, "banana")

def test_compare_methods():
    assert compare_methods(10, 9.8, 10.3) == pytest.approx((0.2, 0.3))
