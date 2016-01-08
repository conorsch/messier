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

Features
--------

* Supports multi-machine roles
* Permits reboots during provisioning
* Use any backend provider available in Vagrant (VirtualBox, AWS, DigitalOcean, etc.)
* Runs Serverspec tests per role via `ansible_spec`_
* Integrates with preexisting Serverspec setups

Motivation
----------

`Test Kitchen`_ is a wonderful solution for testing system configuration—if you use Chef.
Its support for Ansible is, however, lacking. Similar `Packer`_, `Test Kitchen`_ tries
to run Ansible in "local" mode, which makes it impossible to test multi-machine roles
for service orchestration. Well-meaning projects such as `kitchen-ansiblepush`_ (not to
be mistaken with Ansible pull mode) enable more traditional Ansible usage patterns,
but still suffer from limitations such as `reboots always triggering failure`_.

In order to simplify setup, Test Kitchen makes the concession that testing VMs are
polluted with additional software in order to accommodate test running. Serverspec
has an SSH transport built into it, and Test Kitchen ignores that functionality completely.

Name
----

`Messier`_ was a comet hunter, and didn't much care for galaxies or nebula. He
only kept track of non-comet objects so he wouldn't bother inspecting them
further. Similarly, the ``messier`` tool, particularly the ``messier ci``
subcommand, considers working configurations forgettable, and flag only
failures for follow-up work. The name is also brutally honest, in that the
heavy Vagrant dependency will make your configuration projects messier. :wink:


TODO
----

* Add ``init`` command for bootstrapping Messier config


License
-------
GPLv3 (would like to use MIT, but if `import ansible` appears, then it must be GPLv3).

.. _Packer: https://packer.io/docs/provisioners/ansible-local.html
.. _Test Kitchen: http://kitchen.ci/
.. _kitchen-ansiblepush: https://github.com/ahelal/kitchen-ansiblepush
.. _Ansible pull mode: http://docs.ansible.com/ansible/playbooks_intro.html?#ansible-pull
.. _reboots always triggering failure: https://github.com/ahelal/kitchen-ansiblepush/issues/10
.. _ansible_spec: https://github.com/volanja/ansible_spec
.. _Messier: https://en.wikipedia.org/wiki/Charles_Messier
