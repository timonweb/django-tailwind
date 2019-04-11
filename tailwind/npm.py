import subprocess


class NPMException(Exception):
    pass


class NPM:
    cwd = None
    path = None

    def __init__(self, path=None, cwd=None):
        self.path = path
        self.cwd = cwd

    def command(self, *args):
        try:
            subprocess.run(["npm"] + list(args), cwd=self.cwd)
            return True
        except OSError:
            raise NPMException(
                'npm is not installed or cannot be found at path "{path}"'.format(
                    path=self.path
                )
            )
