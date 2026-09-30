from .weapons import WeaponsActions
from .watchlist_countries import WatchlistCountriesActions
from .extremism import IslamicExtremismActions


class FlagsActions(WatchlistCountriesActions,
                   IslamicExtremismActions,
                   WeaponsActions):
    pass
