Alignak Example Module
======================

*Alignak example module*

Build status (stable release)
-----------------------------

.. image:: https://travis-ci.org/Alignak-monitoring/alignak-module-example.svg?branch=master
    :target: https://travis-ci.org/Alignak-monitoring/alignak-module-example
    :alt: Unit tests

.. image:: https://coveralls.io/repos/Alignak-monitoring-contrib/alignak-module-example/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/Alignak-monitoring-contrib/alignak-module-example?branch=master
    :alt: Code coverage

Build status (development release)
----------------------------------

.. image:: https://travis-ci.org/Alignak-monitoring/alignak-module-example.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring/alignak-module-example
    :alt: Unit tests

.. image:: https://coveralls.io/repos/Alignak-monitoring-contrib/alignak-module-example/badge.svg?branch=develop&service=github
    :target: https://coveralls.io/github/Alignak-monitoring-contrib/alignak-module-example?branch=master
    :alt: Code coverage

Most recent release
-------------------

.. image:: https://badge.fury.io/py/alignak_module_example.svg
    :target: https://badge.fury.io/py/alignak_module_example


Short description
-----------------

This module is an example skeleton to build Alignak modules ...


Packaging
---------

Features and known issues
~~~~~~~~~~~~~~~~~~~~~~~~~

Modules can be attached to an Alignak daemon thanks to the daemon configuration file. The module
defines, in its own properties which daemon it may be attached to and the module documentation
will informe the user about this.

Rather than Shinken, a module cannot have sub-modules. This feature is not currenlty well tested
and robust :)

Modules types
~~~~~~~~~~~~~

Alignak attributes a type to each module that is installed. The idea behind the module type is
that it is possible to have several existing modules for the same feature. The current modules types:

    * retention, for a module that saves and reloads livestate data between each system restart
    * livestate, for a module that will register the current system state (hosts, services states, ...)
    * configuration, for a module that will provide the monitored objects to the Alignak arbiter
    * passive, for a module that will collect passive checks results (NSCA, ...)
    * logs, for a module that will collect monitoring logs
    * action, for a module that will execute some actions (acknownledge, downtime, ...)
    * poller, for a module that will execute checks in a poller

Old Nagios parameters require that some external modules are installed for the corresponding
features to be available. The Arbiter will alert if some features are activated and the
corresponding modules are not available in the loaded monitoring configuration.

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
        ALIGNAKETC/
            arbiter/
                modules/
                    mod-EXAMPLE.cfg
        __init__.py
        EXAMPLE.py

The content of the directory ``alignak_checks_EXAMPLE/ALIGNAKETC`` (including files and sub
directories) will be copied to */usr/local/var/etc/alignak*.


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

And that's it!

Then, to build and make your module available to the community, you must use the standard Python setuptools:

    * run ``setup.py register`` to register the new package near PyPI
    * run ``setup.py sdist`` to build the package
    * run ``setup.py develop`` to make the package installed locally (development mode)
    * run ``setup.py develop --uninstall`` to remove the development mode
    * run ``setup.py install --dry-run`` to test the package installation (checks which and where the files are installed)

When your package is ready and functional:

    * run ``setup.py sdist upload`` to upload the package to `PyPI repository`_.

**Note**: every time you upload a package to PyPI you will need to change the module version in the ``alignak_module_EXAMPLE2/__init.py__`` file.


Installation
------------

From PyPI
~~~~~~~~~
To install the module from PyPI::

    pip install alignak-module-EXAMPLE


From source files
~~~~~~~~~~~~~~~~~
To install the module from the source files::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-module-EXAMPLE
    cd alignak-module-EXAMPLE
    pip install -r requirements
    python setup.py install


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

Please report any issue using the project `GitHub repository: <https://github.com/Alignak-monitoring/alignak-module-example/issues>`_.

License
-------

Alignak Module EXAMPLE is available under the `GPL version 3 license`_.

.. _GPL version 3 license: http://opensource.org/licenses/GPL-3.0
.. _Alignak monitoring contrib: https://github.com/Alignak-monitoring-contrib
.. _PyPI repository: <https://pypi.python.org/pypi>
