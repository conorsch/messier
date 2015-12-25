===============================
Messier
===============================

.. image:: https://img.shields.io/pypi/v/messier.svg
        :target: https://pypi.python.org/pypi/messier

.. image:: https://img.shields.io/travis/conorsch/messier.svg
        :target: https://travis-ci.org/conorsch/messier

.. image:: https://readthedocs.org/projects/messier/badge/?version=latest
        :target: https://readthedocs.org/projects/messier/?badge=latest
        :alt: Documentation Status


Test Ansible roles with Vagrant. Inspired by Test Kitchen.

* Free software: ISC license
* Documentation: https://messier.readthedocs.org.

Features
--------

* Supports multi-machine roles
* Permits reboots during provisioning
* Use any backend provider available in Vagrant (VirtualBox, AWS, DigitalOcean, etc.)
* Runs Serverspec tests per role
* Integrates with preexisting Serverspec setups

Motivation
----------

Test Kitchen is a wonderful solution for testing system configuration—if you use Chef.
Its support for Ansible is, however, lacking. Similar to Packer, Test Kitchen tries
to run Ansible in "local" mode, which makes it impossible to test multi-machine roles
for service orchestration. Well-meaning projects such as kitchen-ansiblepush (not to
be mistaken with Ansible push mode) enable more traditional Ansible usage patterns,
but still suffer from limitations such as reboots always triggering failure.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
