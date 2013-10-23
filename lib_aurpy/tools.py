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
import lib_aurpy.config as cfg 

import urllib.request
import re
import os
from subprocess import call, check_output

def progress_bar( pc ):
    
    len = 100
    pcc = int(pc/100*len)
    
    print( "[" + "#" * pcc + " " * (len-pcc) + "]" + chr(27) + "[A" )

    
def get_pkgbuild( origin , pkg_name ):
    
    config = cfg.aurpy_config()
    
    opener = urllib.request.FancyURLopener({})
    f = opener.open( config.get_pkgbuild_url( origin , pkg_name ) )
    
    try :
        pkgbuild = f.read()
        pkgbuild = pkgbuild.decode()
    except :
        return NameError( "Error: PKGBUILD not found!" )
    
    return pkgbuild 

def download_pkg( origin , pkg_name ):
    
    config = cfg.aurpy_config()
    
    cmd = [ "wget" ]
    cmd.append( config.get_aur_dw_pkg_url( pkg_name ) )
    cmd.append( "--directory-prefix=" + "%s/pkg/"%(glob.COMPILE_DIR) )
    
    call( cmd )
    
    
def compile_pkg( pkg_name ):

    os.chdir( "%s/pkg"%(glob.COMPILE_DIR) )

    cmd = [ "tar" , "xvzf" , pkg_name + ".tar.gz"  ]
    call( cmd )
    
    os.chdir( pkg_name )
    
    cmd = [ "makepkg" ]    
    call( cmd )


def _get_pkgbuild_variable( var_name , pb_out ):
    m = re.search( "\s+%s=\|\|\|\|(.*)\|\|\|\|"%var_name , pb_out )
    
    if m :
        ss = m.group(1).strip()
        return ss.split("|||")
    else :
        return []

def parse_pkgbuild( pkgbuild ):
    
    config = cfg.aurpy_config()
    wdir = config.get_tmp_rnd_dir()
    os.makedirs(wdir)
    
    fp = open( wdir + "/PKGBUILD" , "w" )
    fp.write( pkgbuild )
    fp.close()
    
    
    cmd = """
    . PKGBUILD ; 
    printf "makedepends=||||" ; for item in ${makedepends[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "depends=||||" ; for item in ${depends[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "source=||||" ; for item in ${source[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "optdepends=||||" ; for item in ${optdepends[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "pkgname=||||" ; for item in ${pkgname[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    """
    
    fp = open( wdir + "/script" , "w" )
    fp.write( cmd )
    fp.close()
    
    os.chdir( wdir )
    pb_out = check_output( [ "bash" , "script"] ).decode()
    
    pkg_data = dict()
        
    pkg_data["depends"]     = _get_pkgbuild_variable( "depends" , pb_out )
    pkg_data["makedepends"] = _get_pkgbuild_variable( "makedepends" , pb_out )
    pkg_data["source"]      = _get_pkgbuild_variable( "source" , pb_out )
    pkg_data["optdepends"]  = _get_pkgbuild_variable( "optdepends" , pb_out )
    pkg_data["pkgname"]     = _get_pkgbuild_variable( "pkgname" , pb_out )
    
        
    print( pkg_data )
            
    return pkg_data
        
    
    
    
    
    
    
    
    