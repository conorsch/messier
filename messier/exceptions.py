class VagrantfileNotFound(Exception):
    """
    Error when no Vagrantfile is found for a given project.
    Messier assumes that a Vagrantfile in the CWD or in a parent directory
    (same as vagrant itself). If it is not found, this exception will be raised.
    """
    pass


class ServerspecGemfileNotFound(Exception):
    """
    Error when no Gemfile is found within the Serverspec directory.
    """
    pass


class AnsiblePlaybookNotFound(Exception):
    """
    Error when Ansible playbook for running Serverspec tests is not found.
    """
    pass
