import sys
import code

if len(sys.argv) < 2:
    sys.argv.append('../settings.cfg')
code.InteractiveConsole().interact()
