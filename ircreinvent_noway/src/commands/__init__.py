from .api import commands, registeredEvents, EventType, getPrivateMessage, getBroadcast

# this is only done to trigger the registering of the commands, but not to actually import them.
# python will not run the file if the file isn't referenced, so they're referenced here
# but since the functions are not actually being used directly, we can delete the import afterwards.
import ircreinvent_noway.src.commands.builtin as cmdBuiltin
del cmdBuiltin
