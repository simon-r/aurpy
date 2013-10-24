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

from subprocess import check_output, CalledProcessError

import lib_aurpy.config as cfg
import lib_aurpy.glob as glob
import urllib.request
import os

class query( object ):
    def __init__(self):
        pass
    
    def foreign(self):
        """
        Search the foreign installed packages.
        :rtype: return a list containing all the foreign packages  
        """
        cmd = ["pacman" , "-Qm"]
        out = check_output( cmd )
        out = out.decode().splitlines()
        
        return out 
        
        
    def test_installed_package(self , pkg_name ):
        """
        Search an installed package.
        :param pkg_name: The name of the package
        :rtype: a list containing [ name , version ] 
        """
        cmd = "pacman -Q %s"%pkg_name
        try:
            out = check_output( cmd.split() , stderr=open( os.devnull ) ).decode()
        except :
            return None
        return out.split()
    
    def pacman_version(self):
        """
        Return the version message of pacman 
        """
        cmd = "pacman -V"
        try:
            out = check_output( cmd.split() , stderr=open( os.devnull ) ).decode()
        except CalledProcessError as err :
            out = err.output.decode()
        return out    
    
    
    def test_repo_package( self , pkg_name ):
        """
        Search the package in the synchronized repository:
        :param pkg_name: The name of the package
        :rtype: return a list containing [ name , repository , version ]. If the package do non exists it return None 
        """
        cmd = "pacman -Si %s"%pkg_name
        try:
            out = check_output( cmd.split() , stderr=open( os.devnull ) ).decode().splitlines()
        except :
            return None
        
        out = [ out[1].split()[2] , out[0].split()[2] , out[2].split()[2] ]
        
        return out
        
    def test_group_package( self , pkg_name ):
        """
        Search the given group in the synchronized repository:
        :param pkg_name: The name of the package
        :rtype: a list containig all packages of the group. If the package do non exists it return None 
        """
        cmd = "pacman -Sg %s"%pkg_name
        try:
            out = check_output( cmd.split() ).decode().splitlines()
        except :
            return None
        
        return out     
        
    def test_aur_packege( self , pkg_name ):
        """
        Test if a package exists in AUR
        :param pkg_name: The name of the package
        :rtype: True if it exists of False
        """
        config = cfg.aurpy_config()
        
        opener = urllib.request.FancyURLopener({})
        f = opener.open( config.get_pkg_url( glob.AUR , pkg_name ) )
        
        try :
            aur_html = f.read()
        except :
            return False
        
        return True
        
                
        