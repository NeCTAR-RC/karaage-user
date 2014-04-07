# Copyright 2014 The University of Melbourne
#
# This file is part of Karaage-User.
#
# Karaage-User is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage-User is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage-User If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import ast

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


tests_require = open('test-requirements.txt').readlines()
install_requires = map(lambda r: r.rsplit('#egg=', 1)[-1].strip(),
                       open('requirements.txt').readlines())


setup(
    name="karaage-user",
    version=version,
    url='https://github.com/NeCTAR-RC/karaage-user',
    author='Russell Sim',
    author_email='russell.sim@unimelb.edu.au',
    description='Registration interface to karaage',
    packages=find_packages(),
    license="GPL3+",
    scripts=['sbin/kg-manage-user'],
    data_files=[
        ('/etc/karaage', [
            'conf/user_settings.py',
            'conf/user_urls.py',
            'conf/karaage-user.wsgi',
            'conf/kguser-apache.conf'])],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
)
