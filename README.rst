Alignak Example Module
======================

*Alignak example module*

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-example.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-example
    :alt: Develop branch build status

.. image:: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-example/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-example/develop
    :alt: Development code static analysis

.. image:: https://coveralls.io/repos/Alignak-monitoring-contrib/alignak-module-example/badge.svg?branch=develop
    :target: https://coveralls.io/r/Alignak-monitoring-contrib/alignak-module-example
    :alt: Development code tests coverage

.. image:: https://badge.fury.io/py/alignak_module_example.svg
    :target: https://badge.fury.io/py/alignak-module-example
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

Short description
-----------------

This module is an example skeleton to build Alignak modules ...


Packaging
---------

Features and known issues
~~~~~~~~~~~~~~~~~~~~~~~~~

Modules can be attached to an Alignak daemon thanks to the daemon configuration file. The module defines, in its own properties which daemon it may be attached to and the module documentation will informe the user about this.

Rather than Shinken, a module cannot have sub-modules. This feature is not currently well tested and robust enough :) If you really need this feature get in touch with us to discuss the matter.

Modules types
~~~~~~~~~~~~~

Alignak attributes a type to each module that is installed. The idea behind the module type is that it is possible to have several existing modules for the same feature. The current modules types:

* retention, for a module that saves and reloads livestate data between each system restart
* livestate, for a module that will register the current system state (hosts, services states, ...)
* configuration, for a module that will provide the monitored objects to the Alignak arbiter
* passive, for a module that will collect passive checks results (NSCA, ...)
* logs, for a module that will collect monitoring logs
* action, for a module that will execute some actions (acknownledge, downtime, ...)
* poller, for a module that will execute checks in a poller

Old Nagios parameters require that some external modules are installed for the corresponding features to be available. The Arbiter will alert if some features are activated and the corresponding modules are not available in the loaded monitoring configuration.

Repositories
~~~~~~~~~~~~

All Alignak modules are stored in their own repository in the `Alignak monitoring contrib`_ Github organization.


Repository example
~~~~~~~~~~~~~~~~~~
Repository directories and files example::

    README.rst
    LICENCE
    AUTHORS
    requirements.txt
    setup.py
    version.py

    alignak_module_EXAMPLE/
        etc/
            arbiter/
                modules/
                    mod-EXAMPLE.cfg
        __init__.py
        EXAMPLE.py

The content of the directory ``alignak_checks_EXAMPLE/etc`` (including files and sub directories) will be copied to */usr/local/var/etc/alignak*.


Building
~~~~~~~~

To build a new module EXAMPLE2:

    * create a new ``alignak-module-EXAMPLE2`` repository which is a copy of this repository

        * rename the ``alignak_module_EXAMPLE`` directory to ``alignak_module_EXAMPLE2``

    * update the ``version.py`` file

        * edit the ``__pkg_name__`` and the ``module_type`` variables

    * update the ``MANIFEST.in`` file

        * rename the ``alignak_module_EXAMPLE`` directory to ``alignak_module_EXAMPLE2``

    * update the ``README.rst`` file

        * remove this section **Packaging**
        * search and replace ``EXAMPLE`` with ``EXAMPLE2``
        * complete the **Documentation** chapter

    * update the ``version.py`` file with all the package information

        * ``__module_type__`` will be used to complete the keywords in PyPI and as the sub-directory to store the pack's files
        * the file docstring will be used as the package description in PyPI

    * update the ``setup.py`` file (**not recommended**)

        * ``setup.py`` should not be modified for most of the modules ... if necessary, do it with much care!

The ``example.py`` contains all the possible methods that are to be used in the different daemon types. Remove unuseful functions and adapt the remaining ones to your needs. And that's it!

.. note: If you create an external broker module, do not forget to uncomment the 'main' function :)

Then, to build and make your module available to the community, you must use the standard Python setuptools:

    * run ``setup.py register -r pypi`` to register the new package near PyPI
    * run ``setup.py sdist -r pypi`` to build the package
    * run ``sudo pip install . -e`` to make the package installed locally (development mode)
    * run ``sudo pip uninstall -v . -e`` to remove the development mode
    * run ``sudo pip install . -v`` to make the package installed locally
    * run ``sudo pip uninstall -v alignak_module_EXAMPLE`` to uninstall the package

When your package is ready and functional:

    * run ``python setup.py sdist upload -r pypi`` to upload the package to `PyPI repository`_.

**Note**: every time you upload a package to PyPI you will need to change the module version in the ``version.py`` file.




Under this line, keep the content for the new built package. Remove the former *Packaging* section of this document.
-----




Installation
------------

The installation of this module will copy some configuration files in the Alignak default configuration directory (eg. */usr/local/etc/alignak*). The copied files are located in the default sub-directory used for the modules (eg. *arbiter/modules*).

From PyPI
~~~~~~~~~
To install the module from PyPI:
::

   sudo pip install alignak-module-example


From source files
~~~~~~~~~~~~~~~~~
To install the module from the source files (for developing purpose):
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-module-example
   cd alignak-module-example
   sudo pip install . -e

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*


Configuration
-------------

Once installed, this module has its own configuration file in the */usr/local/etc/alignak/arbiter/modules* directory.
The default configuration file is *mod-example.cfg*. This file is commented to help configure all the parameters.

To configure an Alignak daemon to use this module:

- edit your daemon configuration file
- add your module alias value (`example`) to the `modules` parameter of the daemon

To set up several instances of the same module:

- copy the default configuration to another file,
- update the module alias parameter (`example_bis`)
- edit your daemon configuration file
- add the new `module_alias` parameter value (`example_bis`) to the `modules` parameter of the daemon


Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-module-example/issues>`_ are the common way to raise an information.
