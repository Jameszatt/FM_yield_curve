import yfinance as yf
from datetime import datetime
import math

class Share:
    def __init__(self, ticker: str, share_price: float, volatility: float, market_cap: float, dividend_yield: float, sector: str):
        self.ticker = ticker
        self.share_price = share_price
        self.volatility = volatility
        self.market_cap = market_cap
        self.dividend_yield = dividend_yield
        self.sector = sector
 
    def __repr__(self):
        return (f"Share(ticker={self.ticker}, share_price={self.share_price}, "
                f"volatility={self.volatility}, market_cap={self.market_cap}, "
                f"dividend_yield={self.dividend_yield}, sector={self.sector})")

    def calculate_annualized_volatility(self, trading_days: int = 252):
        """
        Calculate the annualized volatility of the share.

        :param trading_days: Number of trading days in a year (default is 252).
        :return: Annualized volatility.
        """
        return self.volatility * (trading_days ** 0.5)

class ShareOption(Share):
    def __init__(self, ticker: str, share_price: float, volatility: float, market_cap: float, dividend_yield: float, sector: str, expiry_date: str):
        super().__init__(ticker, share_price, volatility, market_cap, dividend_yield, sector)
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")

    def calculate_risk_free_rate(self):
        """
        Build a simple yield curve and calculate the risk-free rate.
        For simplicity, this function returns a placeholder value.
        """
        # Placeholder for yield curve and risk-free rate calculation
        return 0.03  # Example: 3% annual risk-free rate

    def calculate_option_value(self, strike_price: float, option_type: str = "call") -> float:
        """
        Calculate the value of the stock option using the Black-Scholes model.

        :param strike_price: The strike price of the option.
        :param option_type: The type of the option ("call" or "put").
        :return: The value of the option.
        """
        from scipy.stats import norm

        # Time to expiry in years
        time_to_expiry = (self.expiry_date - datetime.now()).days / 365.0

        # Risk-free rate
        risk_free_rate = self.calculate_risk_free_rate()

        # Black-Scholes formula components
        d1 = (math.log(self.share_price / strike_price) + (risk_free_rate + 0.5 * self.volatility ** 2) * time_to_expiry) / (self.volatility * math.sqrt(time_to_expiry))
        d2 = d1 - self.volatility * math.sqrt(time_to_expiry)

        if option_type == "call":
            option_value = (self.share_price * norm.cdf(d1)) - (strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2))
        elif option_type == "put":
            option_value = (strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2)) - (self.share_price * norm.cdf(-d1))
        else:
            raise ValueError("Invalid option type. Use 'call' or 'put'.")

        return option_value

    def __repr__(self):
        return (super().__repr__() + f", expiry_date={self.expiry_date.strftime('%Y-%m-%d')}")

# Example usage of the Share class
if __name__ == "__main__":
    # Prompt the user to enter a ticker symbol
    ticker_symbol = input("Enter the ticker symbol: ")
    stock_data = yf.Ticker(ticker_symbol)

    # Extract relevant data using yfinance's history and info
    try:
        share_price = round(stock_data.history(period="1d")["Close"].iloc[-1], 2)
    except (IndexError, KeyError):
        share_price = 0.0

    market_cap = stock_data.info.get("marketCap", 0.0)
    dividend_yield = stock_data.info.get("dividendYield", 0.0)
    sector = stock_data.info.get("sector", "Unknown")

    # Assuming volatility is not directly available, setting a placeholder value
    volatility = 0.2  # Placeholder, replace with actual calculation if available

    # Create an object of the Share class for the entered stock
    stock = Share(
        ticker=ticker_symbol,
        share_price=share_price,
        volatility=volatility,
        market_cap=market_cap,
        dividend_yield=dividend_yield,
        sector=sector
    )

    # Print the stock object
    print(stock)

    # Prompt the user to enter the expiry date for the option
    expiry_date = input("Enter the expiry date (YYYY-MM-DD): ")

    # Create a ShareOption object
    share_option = ShareOption(
        ticker=ticker_symbol,
        share_price=share_price,
        volatility=volatility,
        market_cap=market_cap,
        dividend_yield=dividend_yield,
        sector=sector,
        expiry_date=expiry_date
    )

    # Prompt the user to enter the strike price and option type
    strike_price = float(input("Enter the strike price: "))
    option_type = input("Enter the option type (call/put): ").lower()

    # Calculate the option value
    option_value = share_option.calculate_option_value(strike_price, option_type)

    # Print the ShareOption object and the calculated option value
    print(share_option)
    print(f"The {option_type} option value is: {option_value:.2f}")