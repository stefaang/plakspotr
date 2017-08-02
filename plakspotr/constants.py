##########################################
#
#  constants used for the bonus system
#
#########################################

import os
import datetime

#
BASE = 10

# spot the same car with at least 24h cooldown
COOLDOWN_PERIOD = datetime.timedelta(60 * 60 * 24 if os.getenv('PLAKSPOTR_CONFIG') != 'devel' else 60)



# lose points when you're not cool
YOU_ARE_BORING = -1