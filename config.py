
# config.py

# Paramètres du marché cible
BARRIER_EPIC = "IX.D.DAX.OPTCALL.IP"
EXPIRY_DATE = "FEB-27"
DEFAULT_BARRIER_LEVEL = 25750.0

# Paramètres de trading
DIRECTION = "BUY"
ORDER_SIZE = 1.2
ORDER_TYPE = "MARKET"

# Sécurité
DEMO_MODE = True
DRY_RUN = True  # True = aucun ordre transmis
FORCE_OPEN = True

# Devise : à confirmer dans les caractéristiques IG
CURRENCY_CODE = "EUR"

# Gestion du risque
GUARANTEED_STOP = False
STOP_DISTANCE = None
LIMIT_DISTANCE = None

# Délai de confirmation
CONFIRMATION_TIMEOUT = 15
