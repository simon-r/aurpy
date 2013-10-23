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

import lib_aurpy.config as cfg
import lib_aurpy.glob as glob
import urllib.request

class query( object ):
    def __init__(self):
        pass
    
    def foreign(self):
        cmd = ["pacman" , "-Qm"]
        out = check_output( cmd )
        out = out.decode().splitlines()
        
        return out 
        
        
    def test_installed_package(self , pkg_name ):
        cmd = "pacman -Q %s"%pkg_name
        try:
            out = check_output( cmd.split() ).decode()
        except :
            return None
        return out.split()
    
    
    def test_repo_package( self , pkg_name ):
        cmd = "pacman -Si %s"%pkg_name
        try:
            out = check_output( cmd.split() ).decode().splitlines()
        except :
            return None
        
        out = [ out[1].split()[2] , out[0].split()[2] , out[2].split()[2] ]
        
        return out
        
    def test_group_package( self , pkg_name ):
        cmd = "pacman -Sg %s"%pkg_name
        try:
            out = check_output( cmd.split() ).decode().splitlines()
        except :
            return None
        
        return out     
        
    def test_aur_packege( self , pkg_name ):
        config = cfg.aurpy_config()
        
        opener = urllib.request.FancyURLopener({})
        f = opener.open( config.get_pkg_url( glob.AUR , pkg_name ) )
        
        try :
            aur_html = f.read()
        except :
            return False
        
        return True
        
                
        