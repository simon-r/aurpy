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
from collections import defaultdict 


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
    cmd.append( "--directory-prefix=" + config.get_compile_dir() )
    
    call( cmd )
    
    
def edit_file( pkg_name , file_name ):
    
    config = cfg.aurpy_config()
    
    print( config.get_pkg_build_dir( pkg_name ) )
    print( config.get_pkg_build_dir( pkg_name ) )
    print( config.get_pkg_build_dir( pkg_name ) )
    
    os.chdir( config.get_pkg_build_dir( pkg_name ) )
    
    cmd= os.environ[ "EDITOR" ] + " " + file_name
    
    call( cmd.split() )
    
def unpack_src( pkg_name ):
    
    config = cfg.aurpy_config()
    
    os.chdir( config.get_compile_dir() )

    cmd = [ "tar" , "xvzf" , pkg_name + ".tar.gz"  ]
    call( cmd )    
    
    
def compile_pkg( pkg_name ):

    config = cfg.aurpy_config()

    os.chdir( config.get_pkg_build_dir( pkg_name ) )
        
    cmd = "makepkg -f"    
    call( cmd.split() )

def install_pkg( pkg_name , pkg_files_names ):
    
    config = cfg.aurpy_config()
    os.chdir( config.get_pkg_build_dir( pkg_name ) )
    
    cmd = "sudo pacman -U %s"% ( "".join( " %s "%s for s in pkg_files_names ) )
    
    print()
    print( "\x1b[1;37m Installing packages with the command:\x1b[0m"  )
    print( cmd  )
    
    call( cmd.split() )
    
def install_pacman( pkg_name ):
    
    cmd = "sudo pacman -S %s" % pkg_name
    
    print()
    print( "\x1b[1;37m Installing packages with the command:\x1b[0m"  )
    print( "  \x1b[32m%s\x1b[0m"%cmd  )
    
    call( cmd.split() )
    
def sync_pacman():
    
    cmd = "sudo pacman -Sy "
    
    print()
    print( "\x1b[1;37m Sync repos with the command:\x1b[0m" , end=" " )
    print( "  \x1b[32m%s\x1b[0m"%cmd  )
    print()
    
    call( cmd.split() )



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
    . /etc/makepkg.conf
    printf "makedepends=||||" ; for item in ${makedepends[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "depends=||||" ; for item in ${depends[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "source=||||" ; for item in ${source[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "optdepends=||||" ; for item in ${optdepends[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "pkgname=||||" ; for item in ${pkgname[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "install=||||" ; for item in ${install[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "CARCH=||||" ; for item in ${CARCH[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "arch=||||" ; for item in ${arch[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    printf "PKGEXT=||||" ; for item in ${PKGEXT[*]}; do printf "%s|||" $item ; done ; printf "|\n";
    """
    
    fp = open( wdir + "/script" , "w" )
    fp.write( cmd )
    fp.close()
    
    os.chdir( wdir )
    pb_out = check_output( [ "bash" , "script"] ).decode()
    
    pkg_data = defaultdict( list )
        
    pkg_data["depends"]     = _get_pkgbuild_variable( "depends" , pb_out )
    pkg_data["makedepends"] = _get_pkgbuild_variable( "makedepends" , pb_out )
    pkg_data["source"]      = _get_pkgbuild_variable( "source" , pb_out )
    pkg_data["optdepends"]  = _get_pkgbuild_variable( "optdepends" , pb_out )
    pkg_data["pkgname"]     = _get_pkgbuild_variable( "pkgname" , pb_out )
    pkg_data["install"]     = _get_pkgbuild_variable( "install" , pb_out )
    pkg_data["CARCH"]     = _get_pkgbuild_variable( "CARCH" , pb_out )
    pkg_data["arch"]     = _get_pkgbuild_variable( "arch" , pb_out )
    pkg_data["PKGEXT"]     = _get_pkgbuild_variable( "PKGEXT" , pb_out )
    
    print( pkg_data )
            
    return pkg_data
        
    
    
    
    
    
    
    
    