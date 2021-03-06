from pathlib import Path

from docutils.core import publish_cmdline
from invoke import task
from rellu import Version
from robot.libdoc import libdoc

assert Path.cwd() == Path(__file__).parent



VERSION_PATH = Path('src/SecretsLibrary/version.py')
VERSION_PATTERN = "VERSION = '(.*)'"
RELEASE_NOTES_PATH = Path('docs/MicrosoftDataLibrary-{version}.rst')
RELEASE_NOTES_TITLE = 'SecretsLibrary {version}'
RELEASE_NOTES_INTRO = '''
Write something useful here
'''


@task
def kw_docs(ctx):
    """Generates the library keyword documentation

    Documentation is generated by using the Libdoc tool.
    """
    libdoc(str(Path('src/SecretsLibrary')),
           str(Path('docs/SecretsLibrary.html')))


@task
def project_docs(ctx):
    """Generate project documentation.

     These docs are visible at ?????????????
     """
    args = ['--stylesheet=style.css,extra.css',
            '--link-stylesheet',
            'README.rst',
            'docs/index.html']
    publish_cmdline(writer_name='html5', argv=args)
    print(Path(args[-1]).absolute())


@task
def set_version(ctx, version):
    """Set project version in `src/SSHLibrary/version.py`` file.

    Args:
        version: Project version to set or ``dev`` to set development version.

    Following PEP-440 compatible version numbers are supported:
    - Final version like 3.0 or 3.1.2.
    - Alpha, beta or release candidate with ``a``, ``b`` or ``rc`` postfix,
      respectively, and an incremented number like 3.0a1 or 3.0.1rc1.
    - Development version with ``.dev`` postfix and an incremented number like
      3.0.dev1 or 3.1a1.dev2.

    When the given version is ``dev``, the existing version number is updated
    to the next suitable development version. For example, 3.0 -> 3.0.1.dev1,
    3.1.1 -> 3.1.2.dev1, 3.2a1 -> 3.2a2.dev1, 3.2.dev1 -> 3.2.dev2.
    """
    version = Version(version, VERSION_PATH, VERSION_PATTERN)
    version.write()
    print(version)


@task
def print_version(ctx):
    """Print the current project version."""
    print(Version(path=VERSION_PATH, pattern=VERSION_PATTERN))

