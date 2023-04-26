from typing import TypedDict
from httpx import AsyncClient
from lxml import etree
import re
from .settings import settings


class FII(TypedDict):
    code: str
    description: str
    price: float
    variation: str
    daily_liquidity: float
    last_yield: float
    dividend_yield: float
    net_worth: float
    equity_value: float
    month_profitability: float
    pvp: float


def parse(fii: FII) -> FII:
    def _try_number(value: str) -> float | str:
        try:
            return float(value)
        except Exception:
            try:
                result: str = re.findall("\d+\,\d+", value)[0]
                return float(result.replace(",", "."))
            except Exception:
                return value

    return {
        **fii,
        "daily_liquidity": _try_number(fii.get("daily_liquidity", 0)),
        "dividend_yield": _try_number(fii.get("dividend_yield", 0)),
        "equity_value": _try_number(fii.get("equity_value", 0)),
        "last_yield": _try_number(fii.get("last_yield", 0)),
        "month_profitability": _try_number(fii.get("month_profitability", 0)),
        "price": _try_number(fii.get("price", 0)),
        "pvp": _try_number(fii.get("pvp", 0)),
        "variation": _try_number(fii.get("variation", 0)),
    }


async def fetch_from_url(url: str, mapping: dict) -> dict | None:
    async with AsyncClient() as http:
        response = await http.get(
            url, headers={"User-Agent": settings["scraper"]["default_user_agent"]}
        )

    if response.status_code == 404:
        return None

    dom = etree.HTML(response.text)

    def _xpath(path: str):
        try:
            return dom.xpath(path)[0].text.strip()
        except Exception:
            return ""

    return parse({k: _xpath(xpath) for k, xpath in mapping.items()})


async def fetch_fii_data(code: str) -> FII:
    if not (
        fii := await fetch_from_url(
            settings["scraper"]["fii_data_endpoint"].format(code=code),
            settings["scraper"]["xpath"],
        )
    ):
        raise Exception("Could not find the requested FII.")

    return fii
