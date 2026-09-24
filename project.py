import math
import random
from statistics import NormalDist, stdev
import matplotlib.pyplot as plt

def main():
    #user inputs
    try:
        S = float(input("Stock Price: "))
        K = float(input("Strike Price: "))
        T = float(input("Time to maturity: "))
        r = float(input("Risk-free rate: "))
        sigma = float(input("Volatility: "))
        steps = int(input("Number of binomial steps:"))
        simulations = int(input("Number of Monte Carlo Simulations: "))
    except ValueError:
        print("Invalid numbers")
        return
    option_type = input("Option type (call/put): ").strip().lower()

    try:
        valid_input(S, K, T, sigma, option_type)
        bs_price = black_scholes(S, K, T, r, sigma, option_type)
        binomial = binomial_price(S, K, T, r, sigma, steps, option_type)
        mc_price, standard_error, lower, upper = monte_carlo_price(S, K, T, r, sigma, simulations, option_type)
    except ValueError as error:
        print(error)
        return
#implied vol
    market_input = input("Market option price for implied volatility (leave blank to skip): ").strip()
    market_price = None
    if market_input:
        try:
            market_price = float(market_input)
        except ValueError:
            print("Invalid market price")
            return
#errors
    binomial_error, mc_error = compare_methods(bs_price, binomial, mc_price)
#error convergences
    crr_results = binomial_convergence(S, K, T, r, sigma, steps, option_type)
    mc_results = monte_carlo_convergence(S, K, T, r, sigma, simulations, option_type)
#results
    print("\n--- Option Pricing Results ---")
    #BS
    print("\nBlack-Scholes")
    print(f"Price: {bs_price:.4f}")
    #CRR
    print(f"\nCRR Binomial\nPrice: {binomial:.4f}\nBinomial error: {binomial_error:.4f}")
    #MC
    print(f"\nMonte Carlo\nPrice: {mc_price:.4f}\nMonte Carlo error: {mc_error:.4f}\nStandard Error: {standard_error:.4f}\n95% Confidence Interval: [{lower:.4f}, {upper:.4f}]")
    #IV
    if market_price is not None:
        implied_vol = implied_volatility(S, K, T, r, market_price, option_type)
        print(f"\nImplied Volatility\nMarket Price: {market_price:.4f}\nImplied Volatility: {implied_vol:.4%}")
    #Convergence and graph
    print("\nBinomial Convergence:")
    for steps, price, error in crr_results:
        if steps in [10, 50, 100, 250, 500]:
            print(f"{steps} steps | Price: {price:.4f} | Error: {error:.4f}")
    plot_binomial_convergence(crr_results)

    print("\nMonte Carlo Convergence:")
    for simulations, price, error, standard_error in mc_results:
        if simulations in [1000, 5000, 10000, 50000, 100000]:
            print(f"{simulations} simulations | Price: {price:.4f} | Error: {error:.4f} | SE: {standard_error:.4f}")
    plot_mc_convergence(mc_results)
    plot_mc_price(mc_results, bs_price)

def black_scholes(S, K, T, r, sigma, option_type):
    d1 = (math.log(S/K)+ (r + 1/2 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    normal = NormalDist()

    if option_type == "call":
        C = S * normal.cdf(d1) - K * math.exp(-r * T) *  normal.cdf(d2)
        return C

    elif option_type == "put":
        P = K * math.exp(-r * T) *  normal.cdf(-d2) - S * normal.cdf(-d1)
        return P

def binomial_price(S, K, T, r, sigma, steps, option_type):
    if steps < 10:
        raise ValueError("Steps must be atleast 10")
    delta_t = T / steps
    u = math.exp(sigma * math.sqrt(delta_t))
    d = 1 / u
    p = (math.exp(r * delta_t) - d) / (u - d)

    #stock prices
    stock_prices = []

    for j in range(steps + 1):
        stock_price = S * (u**j) * (d**(steps - j))
        stock_prices.append(stock_price)

    #option values
    option_values = []

    for stock_price in stock_prices:
        if option_type == "call":
            payoff = max(stock_price - K, 0)

        elif option_type == "put":
            payoff = max(K - stock_price, 0)

        option_values.append(payoff)

    #binomial tree
    discount = math.exp(-r * delta_t)
    for step in range(steps - 1, -1, -1):
        new_values = []

        for j in range(step + 1):
            value = discount * (p * option_values[j+1] + (1 - p) * option_values[j])
            new_values.append(value)

        option_values = new_values

    return option_values[0]



def monte_carlo_price(S, K, T, r, sigma, simulations, option_type):
    #list of payoffs from n simulation
    if simulations < 1000:
        raise ValueError("Simulations must be at least 1000")

    payoffs = []

    for _ in range(simulations):
        Z = random.gauss(0, 1)
        stock_price = S * math.exp((r - 1/2 * sigma**2) * T + sigma * math.sqrt(T) * Z)

        if option_type == "call":
            payoff = max(stock_price - K, 0)

        elif option_type == "put":
            payoff = max(K - stock_price, 0)

        payoffs.append(payoff)

    #average the list and discount it
    average_payoff = sum(payoffs) / len(payoffs)
    price = math.exp(-r * T) * average_payoff

    #Standard Error and 95% CI
    payoff_std = stdev(payoffs)
    standard_error = math.exp(-r * T) * (payoff_std / math.sqrt(simulations))
    lower = price - 1.96 * standard_error
    upper = price + 1.96 * standard_error

    return price, standard_error, lower, upper




def implied_volatility(S, K, T, r, market_price, option_type):
    low = 0.0001
    high = 5
    tolerance = 0.0001
    #mid=sigma -> keep bisecting
    for _ in range(100):
        mid = (low + high) / 2
        price = black_scholes(S, K, T, r, mid, option_type)

        if abs(market_price - price) < tolerance:
            return mid

        elif price > market_price:
            high = mid
        else:
            low = mid

    return mid

def compare_methods(bs_price, binomial, mc_price):
    binomial_error = abs(binomial - bs_price)
    mc_error = abs(mc_price - bs_price)

    return binomial_error, mc_error

def binomial_convergence(S, K, T, r, sigma, steps, option_type):
    step_list = list(range(10, steps + 1,10))
    if steps not in step_list:
        step_list.append(steps)

    bs_price = black_scholes(S, K, T, r, sigma, option_type)
    results = []

    for steps in step_list:
        price = binomial_price(S, K, T, r, sigma, steps, option_type)
        error = abs(bs_price - price)
        results.append((steps, price, error))

    return results

def monte_carlo_convergence(S, K, T, r, sigma,simulations, option_type):
    simulation_list = list(range(1000, simulations + 1, 1000))
    if simulations not in simulation_list:
        simulation_list.append(simulations)

    bs_price = black_scholes(S, K, T, r, sigma, option_type)
    results = []

    for simulations in simulation_list:
            price, standard_error, _, _ = monte_carlo_price(S, K, T, r, sigma, simulations, option_type)
            error = abs(bs_price - price)
            results.append((simulations, price, error, standard_error))

    return results

def plot_binomial_convergence(results):
    steps = []
    errors = []

    for step, price, error in results:
        steps.append(step)
        errors.append(error)

    plt.plot(steps, errors)

    plt.xlabel("Number of Binomial Steps")
    plt.ylabel("Absolute Error")
    plt.title("CRR Binomial Convergence")


    plt.savefig("binomial_convergence.png")
    plt.close()

def plot_mc_convergence(results):
    simulations = []
    errors = []
    standard_errors = []

    for simulation, price, error, standard_error in results:
        simulations.append(simulation)
        errors.append(error)
        standard_errors.append(standard_error)

    plt.plot(simulations, errors, label = "Actual Error")
    plt.plot(simulations, standard_errors, label = "Standard Error")
    plt.xlabel("Number of Simulations")
    plt.ylabel("Error")
    plt.title("Monte Carlo Convergence")
    plt.legend()

    plt.savefig("monte_carlo_convergence.png")
    plt.close()

def plot_mc_price(results, bs_price):
    simulations = []
    prices = []
    for simulation, price, error, standard_error in results:
        simulations.append(simulation)
        prices.append(price)

    plt.plot(simulations, prices, label="Monte Carlo Price")

    plt.axhline(y=bs_price, linestyle="--", label="Black-Scholes Price")

    plt.xlabel("Number of Simulations")
    plt.ylabel("Option Price")
    plt.title("Monte Carlo Price Convergence")
    plt.legend()

    plt.savefig("monte_carlo_price_convergence.png")
    plt.close()

def valid_input(S, K, T, sigma, option_type):
    if S <= 0:
        raise ValueError("Stock price must be positive")
    if K <= 0:
        raise ValueError("Strike price must be positive")
    if T <= 0:
        raise ValueError("Time to maturity must be positive")
    if sigma <= 0:
        raise ValueError("Volatility must be positive")
    if option_type not in ["call", "put"]:
        raise ValueError("Invalid Option type")





if __name__ == "__main__":
    main()
