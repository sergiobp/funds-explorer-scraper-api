import tomli
import os
import typing


class ScraperXPathSettings(typing.TypedDict):
    code: str
    description: str
    price: str
    variation: str
    daily_liquidity: str
    last_yield: str
    dividend_yield: str
    net_worth: str
    equity_value: str
    month_profitability: str
    pvp: str


class ScraperSettings(typing.TypedDict):
    default_user_agent: str
    fii_data_endpoint: str
    xpath: ScraperXPathSettings


class Settings(typing.TypedDict):
    scraper: ScraperSettings


SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.toml")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 80))


with open(SETTINGS_PATH, mode="rb") as file:
    settings: Settings = tomli.load(file)
