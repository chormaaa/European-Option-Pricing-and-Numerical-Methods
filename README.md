# European Option Pricing and Numerical Methods
#### Video Demo: https://youtu.be/FnCsjhmUFVg
## Description

This project is a European option pricing tool that compares three different approaches to option valuation:

1. Black-Scholes option pricing
2. Cox-Ross-Rubinstein (CRR) binomial tree pricing
3. Monte Carlo simulation

The program prices both European call and put options, estimates implied volatility using the bisection method and analyses how the CRR and Monte Carlo methods converge towards the Black-Scholes price.

The main aim of the project was not just to build an option price calculator, but also to compare analytical and numerical pricing methods and see how their accuracy changes when the number of binomial steps or Monte Carlo simulations is increased.

## Features

- Black-Scholes pricing for European calls and puts
- CRR binomial tree pricing
- Monte Carlo option pricing
- Monte Carlo standard error
- 95% confidence interval
- Implied volatility using bisection
- Numerical error comparison against Black-Scholes
- Binomial convergence analysis
- Monte Carlo convergence analysis
- Generates convergence graphs

## Files

### project.py
The main Python program containing all pricing models, convergence analysis, plotting functions, input validation, and the main user interface.

### test_project.py

Contains pytest tests for the main pricing and validation functions.

### requirements.txt

Lists the external Python libraries required to run the project.

## Black-Scholes Model
The `black_scholes()` function implements the Black-Scholes pricing formula for European call and put options. It uses Python's `math` module for logarithmic, exponential, and square-root calculations, and `NormalDist` from the `statistics` module to evaluate the cumulative standard normal distribution.

The function takes the stock price, strike price, time to maturity, continuously compounded risk-free interest rate, volatility, and option type as inputs. Depending on whether the user selects a call or put option, it applies the corresponding Black-Scholes formula and returns the theoretical option price.

## CRR Binomial Model
The `binomial_price()` function implements the Cox-Ross-Rubinstein (CRR) binomial option pricing model. The time to maturity is divided into a chosen number of smaller time steps, where the stock price can either move up or down at each step.

The model calculates the up factor, down factor, and risk-neutral probability using the volatility, interest rate, and length of each time step. It then calculates all possible stock prices at maturity and determines the corresponding call or put payoff.

After obtaining the option payoffs at maturity, the function works backwards through the binomial tree. At each node, the discounted risk-neutral expected value of the two possible future option values is calculated. This process continues until only one value remains, representing the estimated option price at the present time.

## Monte Carlo Simulation
The `monte_carlo_price()` function estimates the value of a European option by simulating many possible stock prices at maturity.

For each simulation, the function generates a random value from the standard normal distribution and uses the risk-neutral geometric Brownian motion model to calculate a possible future stock price. The corresponding call or put payoff is then calculated.

After all simulations are completed, the average payoff is calculated and discounted back to the present using the continuously compounded risk-free interest rate. This gives the Monte Carlo estimate of the option price.

The function also calculates the standard error of the estimate and an approximate 95% confidence interval. The standard error measures the uncertainty caused by using a finite number of random simulations. As the number of simulations increases, the standard error generally decreases.

## Implied Volatility
The `implied_volatility()` function calculates the volatility implied by an observed market option price. Instead of using volatility to calculate an option price, this reverses the Black-Scholes problem by finding the volatility that makes the Black-Scholes price approximately equal to the given market price.

The function uses the bisection method. It begins with a lower and upper volatility bound and repeatedly tests the midpoint. Depending on whether the calculated Black-Scholes price is above or below the market price, the search interval is reduced. This continues until the difference between the calculated price and market price is within a specified tolerance.
## Convergence Analysis
The project also investigates how the numerical methods converge towards the Black-Scholes analytical price.

For the CRR model, `binomial_convergence()` increases the number of time steps and records the absolute difference between the binomial price and the Black-Scholes price. This shows how the binomial approximation generally becomes more accurate as the number of steps increases, although the error can oscillate between different step counts.

The `plot_binomial_convergence()` function uses `matplotlib` to generate `binomial_convergence.png`, which displays this convergence behaviour.

For the Monte Carlo method, `monte_carlo_convergence()` increases the number of simulations and records both the absolute pricing error and the standard error. Since Monte Carlo simulation uses random sampling, the actual pricing error does not necessarily decrease smoothly. However, the standard error generally decreases as the number of simulations increases.

The functions `plot_mc_convergence()` and `plot_mc_price()` use `matplotlib` to generate `monte_carlo_convergence.png` and `monte_carlo_price_convergence.png`.

## Design Decisions
I chose Black-Scholes as the benchmark because it gives an analytical solution for European options, which makes it possible to compare the numerical methods against a known reference value. The CRR binomial model and Monte Carlo simulation were chosen as the two numerical approaches.

I also decided to use a continuously compounded risk-free interest rate throughout the project so that the same interest-rate convention is used in all three pricing methods.

Instead of relying on an existing financial library to calculate the option prices, I implemented the main methods directly. This made it possible to explore how the models actually work, particularly the backward induction used in the binomial tree and the random simulation process used in Monte Carlo.

For implied volatility, I chose the bisection method because it is simple and stable, and does not require calculating additional derivatives such as Vega.

The project focuses only on European options, which can only be exercised at maturity. This keeps the models directly comparable and keeps the project focused on the numerical methods. More advanced features, such as American option pricing and early exercise, are outside the scope of this project.

