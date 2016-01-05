class VagrantfileNotFound(Exception):
    """
    Error when no Vagrantfile is found for a given project.
    Messier assumes that a Vagrantfile in the CWD or in a parent directory
    (same as vagrant itself). If it is not found, this exception will be raised.
    """
    pass
