from scrapers.city_hive_scraper import CityHiveScraper
from scrapers.lax_scraper import LaxScraper
from scrapers.exotic_scraper import ExoticScraper
from scrapers.nestor_scraper import NestorScraper
WEBSITES_TO_SCAPE = [
    {
        "name": "LiquorBarn",
        "baseURL": "https://liquorbarn.com/",
        "scraper": CityHiveScraper
    },
    {
        "name": "ThirstyWineAndSpirits",
        "baseURL": "https://thirstyswine.com/",
        "scraper": CityHiveScraper
    },
    {
        "name": "GarysWineAndMarketplace",
        "baseURL": "https://garyswine.com/",
        "scraper": CityHiveScraper
    },
    {
        "name": "MikesWineAndSpirits",
        "baseURL": "https://mikeskc.com/",
        "scraper": CityHiveScraper
    },
    {
        "name": "CoasterLiquors",
        "baseURL": "https://coastersliquors.com/",
        "scraper": CityHiveScraper
    },
    {
        "name": "BigRedLiquors",
        "baseURL": "https://bigredliquors.com/",
        "scraper": CityHiveScraper
    },
    {
        "name": "1800Liquors",
        "baseURL": "https://1800liquors.com/",
        "scraper": CityHiveScraper
    },
    {
        "name": "LaxWineAndSpirits",
        "baseURL": "https://www.laxwineandspirits.com/",
        "scraper": LaxScraper
    },
    {
        "name": "ExoticWineAndSpirits",
        "baseURL": "https://www.exoticwinespirits.com/",
        "scraper": ExoticScraper
    },
    {
        "name": "NestorLiquor",
        "baseURL": "https://www.nestorliquor.com/",
        "scraper": NestorScraper
    }
]
