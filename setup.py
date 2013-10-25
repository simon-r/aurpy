
# Copyright (C) 2013  Simone Riva
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


import os
import shutil
import subprocess
import sys
import re


from distutils.core import setup
from distutils.command.install import install
import lib_aurpy.glob as glob

class aurpy_install(install):
    user_options = install.user_options
 
    def run(self):
        
        install.run(self)
        
#         man_dir = os.path.abspath("./man/")
# 
#         #print ( "root:   " + self.root )
#         #print ( "prefix: " + self.prefix )
# 
#         prefix = re.sub( r'^/' , '' , self.prefix )
# 
#         output = subprocess.Popen([os.path.join(man_dir, "install.sh")],
#                 stdout=subprocess.PIPE,
#                 cwd=man_dir,
#                 env=dict({"PREFIX": os.path.join( self.root , prefix ) }, **dict(os.environ))).communicate()[0]
#         print( output )




setup(name = "aurpy",
    version = "%s" % glob.get_version() ,
    description = "Another AUR helper",
    author = "Simone Riva",
    author_email = "simone.rva [at] gmail.com",
    url = "https://github.com/simon-r/aurpy",
    packages = ['lib_aurpy'],
    scripts = ["aurpy"],
    long_description = "Another AUR helper" ,
    classifiers=[
        'Development Status :: %s Beta' % dr14_version() ,
        'Environment :: Console',
        'Intended Audience :: Users',
        'License :: OSI Approved :: GPL-3.0+',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Topic :: System'] ,
    cmdclass={"install": aurpy_install }
) 
