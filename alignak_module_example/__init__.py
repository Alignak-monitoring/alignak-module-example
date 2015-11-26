

from .version import VERSION as __version__

# the properties and get_instance must be available from the top-level:
from .example import properties, get_instance
# so that alignak can do:
#   mod = importlib.import_module(mod_name)
# where mod_name would be "alignak_module_%s" % $mod_type$
# where $mod_type$ would be taken from the module config file
# and then alignak can do:
#   mod.properties   # to check the module properties attribute, or:
#   mod.get_instance(..)  # to instantiate the module
