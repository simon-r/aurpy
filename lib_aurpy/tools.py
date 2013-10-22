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


import lib_aurpy.glob as glob
import urllib.request
import re
import os
from subprocess import call

def progress_bar( pc ):
    
    len = 100
    pcc = int(pc/100*len)
    
    print( "[" + "#" * pcc + " " * (len-pcc) + "]" + chr(27) + "[A" )
    
def get_pkg_url( origin , pkg_name ):
    
    if origin == glob.AUR :
        return glob.AUR_URL + "/" + pkg_name
    elif origin == glob.PACKAGES :
        return ""

def get_pkgbuild_url( origin , pkg_name ):
    if origin == glob.AUR :
        return glob.AUR_URL + "/" + pkg_name[:2] + "/" + pkg_name + "/" + "PKGBUILD"
    
    return ""


def get_pkgbuild( origin , pkg_name ):
    opener = urllib.request.FancyURLopener({})
    f = opener.open( get_pkgbuild_url( origin , pkg_name ) )
    
    try :
        pkgbuild = f.read()
        pkgbuild = pkgbuild.decode()
    except :
        return NameError( "Error: PKGBUILD not found!" )
    
    return pkgbuild 

def download_pkg( origin , pkg_name ):
    # wget https://aur.archlinux.org/packages/in/intel-parallel-studio-xe/intel-parallel-studio-xe.tar.gz  --directory-prefix=/tmp/aurpy/pkg

    cmd = [ "wget" ]
    cmd.append( glob.AUR_URL + "/" + pkg_name[:2] + "/" + pkg_name + "/" + pkg_name + ".tar.gz" )
    cmd.append( "--directory-prefix=" + "%s/pkg/"%(glob.COMPILE_DIR) )
    
    call( cmd )
    
    
def compile_pkg( pkg_name ):

    os.chdir( "%s/pkg"%(glob.COMPILE_DIR) )

    cmd = [ "tar" , "xvzf" , pkg_name + ".tar.gz"  ]
    call( cmd )
    
    os.chdir( pkg_name )
    
    cmd = [ "makepkg" ]    
    call( cmd )

def parse_pkgbuild( pkgbuild ):
    pkg_data = dict()
    
    pkgbuild = re.sub( "\#.*\n" , "\n" , aur_html , flags=re.M )
    pkgbuild = re.sub( "[\n\r]" , " " , pkgbuild )
    pkgbuild = re.sub( "\s+" , " " , pkgbuild )
    
    m = re.search( '\s+depends\s*\=\s*(\(.+\))' , pkgbuild )
    
    if m :
        ss = m.group(1).strip()

        ss = re.sub( r"\s+" , " " , ss )
        ss = re.sub( r"[\(\)]" , "" , ss )
        ss = re.sub( r"[\'\"]\s[\'\"]" , "|" , ss )
        ss = re.sub( r"[\'\"]" , "" , ss )
        ss = re.sub( r"\s+" , "" , ss )
        pkg_data["depends"] = ss.split("|")
    else :
        pkg_data["depends"] = []
    
    
    m = re.search( 's+makedepends\s*\=\s*(\(.+\))' , pkgbuild )
    
    if m :
        ss = m.group(1).strip()

        ss = re.sub( r"\s+" , " " , ss )
        ss = re.sub( r"[\(\)]" , "" , ss )
        ss = re.sub( r"[\'\"]\s[\'\"]" , "|" , ss )
        ss = re.sub( r"[\'\"]" , "" , ss )
        ss = re.sub( r"\s+" , "" , ss )
        pkg_data["makedepends"] = ss.split("|")
    else :
        pkg_data["makedepends"] = []
        
    return pkg_data
        
    
    
    
    
    
    
    
    