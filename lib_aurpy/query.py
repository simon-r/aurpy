# aurpy : AUR helper in py
#Copyright (C) 2013 Simone Riva
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

from subprocess import check_output
import lib_aurpy.package as pkg

class query( object ):
    def __init__(self):
        pass
    
    def foreign(self):
        cmd = ["pacman" , "-Qm"]
        out = check_output( cmd )
        out = out.decode().splitlines()
        
        pkgs = dict()
        
        for p in out :
            pl = p.split()
            pkgs[pl[0]] = pkg.package()
            pkgs[pl[0]].name = pl[0]
            pkgs[pl[0]].installed_version = pl[1]
            
        return pkgs
        