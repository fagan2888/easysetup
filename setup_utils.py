#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009-2015 Joao Carlos Roseta Matos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Setup utils library."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import datetime as dt
import glob
import os
##import pprint as pp
import sys
##import sysconfig
import time
import zipfile as zip

import appinfo


def check_copyright():
    """Check copyright on files that have to be updated manually."""
    files = ['setup_utils.py', 'build.cmd', 'appinfo.py']
    update_required = 0
    for filename in files:
        if os.path.isfile(filename):
            with codecs.open(filename, encoding='utf8') as file_:
                text = file_.readlines()
            for line in text:
                if appinfo.COPYRIGHT in line:
                    break
                if 'Copyright 2009-' in line:
                    print('Copyright in ' + filename + ' is not updated.')
                    update_required += 1
                    break
    if update_required:
        sys.exit(1)


def update_copyright():
    """Update copyright on source and license files."""
    files = glob.glob('*.py')
    files = [file_ for file_ in files if file_ not in ['appinfo.py',
                                                       'setup_utils.py']]
    files += glob.glob(appinfo.APP_NAME + '/*.py')
    for filename in files:
        with codecs.open(filename, encoding='utf8') as file_:
            text = file_.readlines()
        new_text = ''
        changed = False
        for line in text:
            if ((not changed) and (appinfo.COPYRIGHT not in line) and
                 ('Copyright 2009-' in line)):
                new_text += '# ' + appinfo.COPYRIGHT + os.linesep
                changed = True
            else:
                new_text += line
        if changed:
            with codecs.open(filename, 'w', encoding='utf8') as file_:
                file_.writelines(new_text)

    filename = 'doc/conf.py'
    if os.path.isfile(filename):
        with codecs.open(filename, encoding='utf8') as file_:
            text = file_.readlines()
        new_text = ''
        changed = False
        doc_copyright = ("copyright = u'2009-" + str(dt.date.today().year) +
                         ', '  + appinfo.AUTHOR + "'")
        for line in text:
            if ((not changed) and ("copyright = u'2009-" in line) and
                 (doc_copyright not in line)):
                new_text += doc_copyright + os.linesep
                changed = True
            else:
                new_text += line
        if changed:
            with codecs.open(filename, 'w', encoding='utf8') as file_:
                file_.writelines(new_text)

    filename = 'LICENSE.rst'
    with codecs.open(filename, encoding='utf8') as file_:
        text = file_.readlines()
    new_text = ''
    changed = False
    for line in text:
        if ((not changed) and (appinfo.COPYRIGHT not in line) and
             ('Copyright ' + '2009-' in line)):
            new_text += '        ' + appinfo.COPYRIGHT + os.linesep
            changed = True
        else:
            new_text += line
    if changed:
        with codecs.open(filename, 'w', encoding='utf8') as file_:
            file_.writelines(new_text)


def sleep(seconds=5):
    """Pause for specified time."""
    time.sleep(seconds)


def app_name():
    """Write application name to text file."""
    with open('app_name.txt', 'w') as file_:
        file_.write(appinfo.APP_NAME)


def app_ver():
    """Write application version to text file if equal to ChangeLog.rst."""
    with open('ChangeLog.rst') as file_:
        changelog_app_ver = file_.readline().split()[0]
    if changelog_app_ver == appinfo.APP_VERSION:
        with open('app_ver.txt', 'w') as file_:
            file_.write(appinfo.APP_VERSION)
    else:
        print('ChangeLog.rst and appinfo.py are not in sync.')


def app_type():
    """Write application type (application or module) to text file."""
    with open('app_type.txt', 'w') as file_:
        file_.write(appinfo.APP_TYPE)


def py_ver():
    """Write Python version to text file."""
    with open('py_ver.txt', 'w') as file_:
        file_.write(str(sys.version_info.major) + '.' +
                    str(sys.version_info.minor))


def remove_copyright():
    """Remove Copyright from README.rst."""
    with open('../README.rst') as file_:
        text = file_.readlines()

    new_text = ''

    for line in text:
        if 'Copyright ' in line:
            pass
        else:
            new_text += line

    with open('../README.rst', 'w') as file_:
        file_.writelines(new_text)


def prep_rst2pdf():
    """Remove parts of rST to create a better pdf."""
    with open('index.ori') as file_:
        text = file_.readlines()

    new_text = ''

    for line in text:
        if 'Contents:' in line:
            pass
        elif 'Indices and tables' in line:
            break
        else:
            new_text += line

    with open('index.rst', 'w') as file_:
        file_.writelines(new_text)

    with open('../README.rst') as file_:
        text = file_.readlines()

    new_text = ''

    for line in text:
        if '.. image:: ' in line or '    :target: ' in line:
            pass
        else:
            new_text += line

    with open('../README.rst', 'w') as file_:
        file_.writelines(new_text)


def create_doc_zip():
    """Create doc.zip to publish in PyPI."""
    doc_path = appinfo.APP_NAME + '/doc'
    with zip.ZipFile('pythonhosted.org/doc.zip', 'w') as archive:
        for root, dirs, files in os.walk(doc_path):
            for file_ in files:
                if not '.pdf' in file_:
                    pathname = os.path.join(root, file_)
                    filename = pathname.replace(doc_path + os.sep, '')
                    archive.write(pathname, filename)


##def std_lib_modules():
##    """List all (not complete) Standard library modules."""
##    std_lib_dir = sysconfig.get_config_vars('LIBDEST')[0]
##    modules_lst = []
##    for top, dirs, files in os.walk(std_lib_dir):
##        for nm in files:
##            if nm != '__init__.py' and nm[-3:] == '.py':
##                module = os.path.join(top, nm)[len(std_lib_dir)+1:-3].replace('\\','.')
##                if 'site-packages.' not in module:
##                    modules_lst.append(os.path.join(top, nm)[len(std_lib_dir)+1:-3].replace('\\','.'))
##    pp.pprint(modules_lst)


##def non_std_lib_modules():
##    """List all non Standard library modules."""
##    site_lib_dir = sysconfig.get_config_vars('LIBDEST')[0]
##    site_lib_dir += '/site-packages'
##    modules_lst = []
##    for top, dirs, files in os.walk(site_lib_dir):
##        for nm in files:
##            if nm != '__init__.py' and nm[-3:] == '.py':
##                modules_lst.append(os.path.join(top, nm)[len(site_lib_dir)+1:-3].replace('\\','.'))
##    pp.pprint(modules_lst)


##def docstr2readme():
##    """Copy main module docstring to README.rst."""
##    with codecs.open(appinfo.APP_NAME + '/' + appinfo.APP_NAME + '.py',
##                     encoding='utf8') as file_:
##        text = file_.readlines()
##
##    text2copy = appinfo.APP_NAME + '\n' + '=' * len(appinfo.APP_NAME) + '\n\n'
##
##    start_copy = False
##
##    for line in text:
##        if '"""' in line:
##            if start_copy:
##                break
##            else:
##                start_copy = True
##        elif start_copy:
##            text2copy += line
##
##    text2copy += '\n'
##
##    with codecs.open(appinfo.APP_NAME + '/README.rst',
##                     encoding='cp1252') as file_:
##        text = file_.readlines()
##
##    until_eof = False
##
##    for line in text:
##        if 'Resources' in line or until_eof:
##            text2copy += line
##            until_eof = True
##
##    with codecs.open(appinfo.APP_NAME + '/README.rst', 'wb',
##                     encoding='cp1252') as file_:
##        file_.writelines(text2copy)


if __name__ == '__main__':
    eval(sys.argv[1])