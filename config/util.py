import os


def get_env_read_file(env: str, default=None):
    """Get Environment Variable (read file)

    As this app will mainly be used inside a docker container, it is
    possible that secrets will be passed using a ``_FILE`` suffix
    for environment variables.
    This function check whether the environment variable with ``_FILE``
    suffix exists and falls back to the normal environment variable.

    If both (with and without ``_FILE`` suffix) are set, an exception is
    raised.

    This function is designed to be a drop-in replacement for
    :func:`os.environ.get`.

    :param env: Name of the environment variable WITHOUT the ``_FILE``
        suffix.
    :param default: Default value returned if both environment variables
        are None, i.e. not set.
    """
    file = os.environ.get(f"{env}_FILE", default=None)
    not_file = os.environ.get(env, default=None)
    if not (file is None or not_file is None):
        # Both are set
        raise ValueError(f"Both {env}_FILE and {env} are set. Only one is supported!")
    if file is None and not_file is None:
        # Both are not set
        return default
    if file is not None:
        # Check whether the file actually exists
        if not os.path.isfile(file):
            raise FileNotFoundError(f"{env}_FILE: File not found ({file})!")
        # Open and read the file. Content of the file is returned
        with open(file, "r") as f:
            return f.read()
    else:
        # Return the value of the environment variable without the
        # _FILE suffix
        return not_file
