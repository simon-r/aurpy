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

class compilation_error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def progress_bar( pc ):
    
    len = 100
    pcc = int(pc/100*len)
    
    print( "[" + "#" * pcc + "%3d%%"%pcc + " " * (len-pcc) + "]" + chr(27) + "[A" )

    
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
 
def get_vcs_pkg_file_name( pkg_name , vcs ):
       
    config = cfg.aurpy_config()
    
    pkdir = config.get_pkg_build_dir( pkg_name )
    
    lsdir = os.listdir( pkdir )
    
    max = 0.0
    res = None
    
    for f in lsdir :
        m = re.search( "^%s.+pkg.+"%pkg_name , f )
        if m :
            if os.path.getmtime( pkdir + "/" + f ) > max :
                res = f
    return res

def get_sub_pkg_file_names( base_pkg_name , sub_pkg_names ):
    
    config = cfg.aurpy_config()
    
    pkdir = config.get_pkg_build_dir( base_pkg_name )
    
    lsdir = os.listdir( pkdir )
    
    res = []
    
    for f in lsdir :
        max = 0.0
        for m in re.finditer( "^%s.+pkg.+"%pkg_name , f ) :
            if os.path.getmtime( pkdir + "/" + f ) > max :
                res.append( f )
                
    return res 
            
    
            
    
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

    cmd = [ "bsdtar" , "xzf" , pkg_name + ".tar.gz"  ]
    call( cmd )    
    

def own_package( pkg_name , pkg_list ):
    
    for p in pkg_list :
        pl = p.split(">=")
        
        if pl[0] == pkg_name :
            return True
        
        return False
     
    
def compile_pkg( pkg_name ):

    config = cfg.aurpy_config()

    os.chdir( config.get_pkg_build_dir( pkg_name ) )
        
    cmd = "makepkg -f"    
    ret = call( cmd.split() )
    
    if ret != 0 :
        raise compilation_error( pkg_name )
    
def sync_pacman():
    
    cmd = "sudo pacman -Sy "
    
    print()
    print( "\x1b[1;37m Sync repos with the command:\x1b[0m" , end=" " )
    print( "  \x1b[32m%s\x1b[0m"%cmd  )
    print()
    
    call( cmd.split() )



def _get_pkgbuild_variable( var_name , pb_out ):
    m = re.search( "=%s=\|\|\|\|(.*)\|\|\|\|"%var_name , pb_out )
    
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
    
    list_cmd = """
    printf "=<VARIABLE>=||||" ; for item in ${<VARIABLE>[@]}; do printf "%s|||" $item ; done ; printf "|\n";
    """
    
    variables = """
     pkgname
     pkgver
     pkgrel
     pkgdir
     epoch
     pkgbase
     pkgdesc
     arch
     url
     license
     groups
     depends
     optdepends
     makedepends
     checkdepends
     provides
     conflicts
     replaces
     backup
     options
     install
    changelog
     source
     noextract
     md5sums sha1sums sha256sums sha384sums sha512sums 
     CARCH PKGEXT
    """.split()
        
    cmd = """
        . /etc/makepkg.conf ; 
        . PKGBUILD ; 
    """
    
    for v in variables :
        cmd = cmd + re.sub( "<VARIABLE>" , v , list_cmd ) + "\n"
    
    
    fp = open( wdir + "/script" , "w" )
    fp.write( cmd )
    fp.close()
    
    os.chdir( wdir )
    pb_out = check_output( [ "bash" , "script"] ).decode()
    
    pkg_data = defaultdict( list )
    
    for v in variables :
        pkg_data[v]     = _get_pkgbuild_variable( v , pb_out )
           
    print( pkg_data )
            
    return pkg_data
        
    
    
    
    
    
    
    
    