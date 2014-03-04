from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os
import sys
import ast

class osx_install_data(install_data):
    # On MacOS, the platform-specific lib dir is /System/Library/Framework/Python/.../
    # which is wrong. Python 2.5 supplied with MacOS 10.5 has an Apple-specific fix
    # for this in distutils.command.install_data#306. It fixes install_lib but not
    # install_data, which is why we roll our own install_data class.

    def finalize_options(self):
        # By the time finalize_options is called, install.install_lib is set to the
        # fixed directory, so we set the installdir to install_lib. The
        # install_data class uses ('install_data', 'install_dir') instead.
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
code_dir = 'kguser'

for dirpath, dirnames, filenames in os.walk(code_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Small hack for working with bdist_wininst.
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

path = "kguser/__init__.py"
with open(path, 'rU') as file:
    t = compile(file.read(), path, 'exec', ast.PyCF_ONLY_AST)
    for node in (n for n in t.body if isinstance(n, ast.Assign)):
        if len(node.targets) == 1:
            name = node.targets[0]
            if isinstance(name, ast.Name) and \
                    name.id in ('__version__', '__version_info__', 'VERSION'):
                v = node.value
                if isinstance(v, ast.Str):
                    version = v.s
                    break
                if isinstance(v, ast.Tuple):
                    r = []
                    for e in v.elts:
                        if isinstance(e, ast.Str):
                            r.append(e.s)
                        elif isinstance(e, ast.Num):
                            r.append(str(e.n))
                    version = '.'.join(r)
                    break

media_files = []
for dirpath, dirnames, filenames in os.walk('media'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        media_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

for dirpath, dirnames, filenames in os.walk('templates'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        media_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


for i in media_files:
    d = i[0]
    i[0] = '/usr/share/kguser/%s' % d


data_files =  media_files
data_files.append(('/usr/sbin', ['sbin/kg-manage-user']))
data_files.append(
    ('/etc/karaage', [
        'conf/user_settings.py',
        'conf/user_urls.py',
        'conf/karaage-user.wsgi',
        'conf/kguser-apache.conf'])
)

setup(
    name = "karaage-user",
    version = version,
    url = 'https://github.com/Karaage-Cluster/karaage',
    author = 'Russell Sim',
    author_email = 'russell.sim@unimelb.edu.au',
    description = 'Registration interface to karaage',
    packages = packages,
    cmdclass = cmdclasses,
    data_files = data_files,
)
