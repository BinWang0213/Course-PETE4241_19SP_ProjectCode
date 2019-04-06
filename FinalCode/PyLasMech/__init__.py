'''
PyGeoMesh
-------
Modules
-------
This package consists of several modules, the purposes of which are given below:
+------------------------+----------------------------------------------------+
| **filters**            | Process images based on structural features        |

-------------
Example Usage
-------------
>>> import PyLasMech as plm

----------------
Related Packages
----------------
lasio 

'''

__version__ = "0.0.1"

#Main Class

#Sub modules
from . import lasio

from .IO import *
from .plot import *
from .tabulate import *

