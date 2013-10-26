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


import re
import sys
import urllib.request
from collections import defaultdict

#from exception import Exception

import lib_aurpy.version as ver
import lib_aurpy.tools as tools
import lib_aurpy.glob as glob
import lib_aurpy.config as cfg 
import lib_aurpy.query as qe
import lib_aurpy.pacman as pacman


class package_not_found(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class package( object ):
    def __init__( self ):
        self._origin = None
        self._name = None
        self._reason = None
        self._depends = None
        self._vcs_pkgbuild = None 
        self._repo_version = ver.version( "0.0.0-0" )
        self._installed_version = ver.version( "0.0.0-0" )

    def set_origin( self , orig ):
        self._origin = orig
        
    def get_origin(self):
        return self._origin
    
    origin = property( get_origin , set_origin , doc="" )
    
    def set_name( self , n ):
        self._name = n
        
    def get_name(self):
        return self._name
    
    name = property( get_name , set_name , doc="" )
    
    def get_reason(self):
        return self._reason
    
    def set_reason( self , r ):
        self._reason = r 
        
    reason = property( get_reason , set_reason , doc="" )
    
    def get_repo_version(self):
        if self._repo_version == None :
            return None 
        return self._repo_version 
    
    def set_repo_version(self,v):
        if self._repo_version == None :
            return None 
        self._repo_version = ver.version( v ) 
    
    repo_version = property( get_repo_version , set_repo_version , doc="" )
    
    def get_installed_version(self):
        if self._installed_version == None :
            return None 
        return self._installed_version 
    
    def set_installed_version(self,v):
        self._installed_version = ver.version( v )
        
    installed_version = property( get_installed_version , set_installed_version , doc="" )    
    
    
    def get_has_subpackages(self):
        if len( self._pkg_data["name"] ) > 1 :
            return True 
        else :
            return False
        
    has_subpackages = property( get_has_subpackages , doc="" )
    
    
    def test_vcs(self):
        for v in glob.VCS_SUFF :
            if re.search( "\-%s"%v , self.name ) :
                self._vcs_pkgbuild = v
                return v
        self._vcs_pkgbuild = False
        return False
    
    def get_vcs(self):
        if self._vcs_pkgbuild == None :
            self.test_vcs()
        return self._vcs_pkgbuild
    
    vcs = property( get_vcs , doc="" )
    
    def edit_pkgbuild(self):
        tools.edit_file( self.name , "PKGBUILD" )
    
    def edit_build_file( self , file_name ):
        if file_name in self._pkg_data["install"] :
            tools.edit_file( self.name , file_name )
            
    def get_install(self):
        return self._pkg_data["install"]
    
    def download_src(self):
        tools.download_pkg( self.origin , self.name )
        
    def unpack_src(self):
        tools.unpack_src( self.name )
    
    def compile(self):
        tools.compile_pkg( self.name )
        
    def install( self , asdeps=False ):
        arch = self._pkg_data["CARCH"][0]
        
        if "any" in self._pkg_data["arch"] :
            arch = "any"
        
        if self.vcs :
            pkg_file_name = [ tools.get_vcs_pkg_file_name( self.name , self.vcs ) ]
        elif self.has_subpackages :
            get_sub_pkg_file_names( self.name , self._pkg_data["name"] )
        else :
            pkg_file_names = [ "%s-%s-%s%s" % ( self.name , self.repo_version , arch , self._pkg_data["PKGEXT"][0] ) ]
        
        if asdeps :
            pacman.install_pkg_list( self.name , pkg_file_names , reason=glob.DEPENDS )
        else :    
            pacman.install_pkg_list( self.name , pkg_file_names )
        
        
        if self.has_subpackages :
            config = cfg.aurpy_config()
            config.set_subpackages( self.name , pkg_file_names )
    
    
    def read_repo_data(self):
        
        config = cfg.aurpy_config()
        query = qe.query()
        
        if self.origin == glob.AUR :
        
            opener = urllib.request.FancyURLopener({})
            f = opener.open( config.get_pkg_url( self.origin , self.name ) )
            
            try :
                aur_html = f.read()
                self._aur_html = aur_html.decode()
            except :
                return False
            
            #print( self._aur_html )
            
            r = '<h2>Package\s+Details\:\s+([\w\-]+)\s+([\w+\-\.\:]+)\s*<\/h2>'
            m = re.search( r , self._aur_html )
            
            if m == None :
                raise NameError("Invalid AUR HTML format")
                 
                
            self.name = m.group(1)
            self.repo_version = m.group(2) 
            self.test_vcs()
            
            inst = query.test_installed_package( self.name )
            if inst :
                self.installed_version = inst[1]
            
            return True
        
        else :
            
            inf = query.test_repo_package( self.name )
            inst = query.test_installed_package( self.name )
            
            if inf == None and inst == None :
                return False
            
            self.repo_version = inf[2]
            
            if inst :
                self.installed_version = inst[1]
                
            return True
                
    
    def read_pkgbuild_data(self):
        self._pkgbuild = tools.get_pkgbuild( self.origin , self.name )
        self._pkg_data = tools.parse_pkgbuild( self._pkgbuild )
        
    
    def _list_dependecies( self , dep ):
        query = qe.query()
        
        for d in self._pkg_data[dep] :
            if query.test_installed_package( d ) :
                self._pkg_data["%s_installed"%dep].append( d )
            elif query.test_repo_package( d ) :
                self._pkg_data["%s_repo"%dep].append( d )
            elif query.test_aur_packege( d ) :
                self._pkg_data["%s_aur"%dep].append( d )
            elif query.test_group_package( d ) :
                self._pkg_data["%s_group"%dep].append( d )
            else :
                self._pkg_data["%s_nd"%dep].append( d )        
        
        
    def test_dependecies(self):
        self._list_dependecies( "depends" )
        self._list_dependecies( "makedepends" )
        #self._build_dependecies( "optdepends" )
        
    def get_depends_istalled( self , dep="depends" ):
        return self._pkg_data[ "%s_installed"%dep ]
    
    def get_depends_repo( self , dep="depends" ):
        return self._pkg_data[ "%s_repo"%dep ]
    
    def get_depends_aur( self , dep="depends" ):
        return self._pkg_data[ "%s_aur"%dep ]
    
    def get_depends_nd( self , dep="depends" ):
        return self._pkg_data[ "%s_nd"%dep ]
       
    def get_depends_list_rec(self):
        if self._depends == None :
            return []
        else :
            r = []
            for d in self._depends.keys() :
                r += self._depends[d].get_depends_list_rec()
            return r 
    
    def build_depends_rec(self):
        aur_l   = self.get_depends_aur() 
        aur_mkl = self.get_depends_aur( "makedepends" )
        
        repo_l   = self.get_depends_repo()
        repo_mkl = self.get_depends_repo("makedepends")
        
        print( aur_l + aur_mkl + repo_l + repo_mkl )
        if len(aur_l) + len(aur_mkl) == 0 :
            return False
        
        self._depends = defaultdict()
        
        for dd in ( aur_l + aur_mkl + repo_l + repo_mkl ) :
            d = tools.clean_pkg_name( dd )
            print(d)
            pkg = package()
            pkg.name = d 
            
            if tools.own_package( d , aur_l + aur_mkl ) :
                pkg.origin = glob.AUR
            else :
                pkg.origin = glob.PACKAGES
                
            f = pkg.read_repo_data()
            
            if not f :
                raise package_not_found( " The package named: %s do not exists ! "%d )
                 
            ######################################
            ######################################
            pkg.read_pkgbuild_data() 
            pkg.test_dependecies()
            
            if tools.own_package( d , aur_mkl ) :
                pkg.reason = glob.MAKE_DEPENDS
            else :
                pkg.reason = glob.DEPENDS
            
            print( "ssssssssssssssssssssssssssssssssssssss" )
            #pkg.read_pkgbuild_data() 
            pkg.build_depends_rec()
            
            self._depends[ pkg.name ] = pkg
          
        return True 

         
    def compile_install_depends_rec(self):
        
        query = qe.query()
        
        if self._depends == None :
            return 
        
        for pkg in self._depends.keys() :
            self._depends[pkg].compile_install_depends_rec()
            if not query.test_installed_package( pkg ) :
                f = compile_sequence( self._depends[pkg] )
                if f :
                    install_sequence( self._depends[pkg] , confirm=False , asdep=True )
                    
    def new_in_repo(self):
        if self.installed_version == None :
            return True 
        
        return self.installed_version < self.repo_version 


def foreign():
    
    query = qe.query()
    
    out = query.foreign()
    
    pkgs = dict()
    
    for p in out :
        pl = p.split()
        pkgs[pl[0]] = package()
        pkgs[pl[0]].name = pl[0]
        pkgs[pl[0]].installed_version = pl[1]
        
    return pkgs
    
    
def build_pkgs_dict( pkg_list , version=True , explicit=False ):
    
    query = qe.query()
    
    pkgs = dict()
    
    for p in pkg_list :
        pl = p.split()
        
        pkgs[pl[0]] = package()
        pkgs[pl[0]].name = pl[0]
        if version : 
            pkgs[pl[0]].installed_version = pl[1]
            
        if explicit :
            pkgs[pl[0]].reason = glob.EXPLICIT
            
    return pkgs

def test_packages( pkgs ):
    
    default_origin = glob.AUR
    
    update_lst = []
    
    i = 1
    
    print("\x1b[1;32m* Retrieving Packages form PKGBUILD'S repositories: \x1b[0m")
    
    for k in pkgs.keys() :
        pkgs[k].origin = default_origin
        f = pkgs[k].read_repo_data()
        
        tools.progress_bar( int( i / len(pkgs) * 100 ) )
        i+=1
        
        sys.stdout.flush()
                
        if f and pkgs[k].new_in_repo() :
            #print( "%s\n %s -> %s\n"%( pkgs[k].name , pkgs[k].installed_version , pkgs[k].repo_version ) )
            update_lst.append(k)
        elif pkgs[k].reason == glob.EXPLICIT :
            update_lst.append(k)
    
    print()
    
    return update_lst


def test_dependencies( pkgs , update_lst ):
    for k in update_lst :
        pkgs[k].read_pkgbuild_data()
        pkgs[k].test_dependecies()


def print_deps_list( message , up_lst ):
    if len(up_lst): 
        print(  message + "".join( ( s + " ")  for s in up_lst ) )
    

def print_update_list( pkgd , update_lst ):
    
    for pkg , i in zip( update_lst , range( len( update_lst ) ) ):
        ins = pkgd[pkg].get_depends_istalled()
        rep = pkgd[pkg].get_depends_repo()
        aur = pkgd[pkg].get_depends_aur()
        
        mkins = pkgd[pkg].get_depends_istalled( "makedepends" )
        mkrep = pkgd[pkg].get_depends_repo( "makedepends" )
        mkaur = pkgd[pkg].get_depends_aur( "makedepends" )
        
        print( "%d. \x1b[1;33m%s \x1b[0m"%( i,pkg ) , end=" " )
        
        if pkgd[pkg].vcs :
            print( "\x1b[33m version control system based pkg:\x1b[35m %s \x1b[0m"%( pkgd[pkg].vcs ), end="\n" )
        else:
            print( "\x1b[33m %s ->\x1b[35m %s \x1b[0m"%( pkgd[pkg].installed_version , pkgd[pkg].repo_version ) , end="\n" )
        
        print_deps_list( "   Installed  deps:     " , ins )
        print_deps_list( "   Repository deps:     " , rep )
        print_deps_list( "   AUR        deps:     " , aur )
        print_deps_list( "   Installed  makedeps: " , mkins )
        print_deps_list( "   Repository makedeps: " , mkrep )
        print_deps_list( "   AUR        makedeps: " , mkaur )
        
        print()


def select_packages( pkgd , update_lst ):
    
    print("\x1b[1;32m* Select Packages \x1b[0m")
    print_update_list( pkgd , update_lst )
    print()
    s = input("Do you want to exclude some package from the update list? [y/N] ")
    
    if s in ["Y","y"] :
        while True :
            s = input("Insert the number of a package that must not be updated [e: exit]: ")
            if s == "e" :
                break 
            
            try :
                nr = int( s )
            except :
                print( "Wrong input value, please insert a valid number" )
            
            try :
                name = update_lst[nr]
                del update_lst[nr]
                print( " \x1b[31m  %s \x1b[0m - has been removed" % name )
            except :
                print( "Wrong input value, please insert a valid number" )
            
            print() 
            print_update_list( pkgd , update_lst )
                
    return update_lst
    

def compile_sequence( package ):
    
    print( "\x1b[1;34m======================================> \x1b[0m " )
    print( "\x1b[1;34m===> \x1b[1;31mCOMPILING: \x1b[1;37m %s \x1b[0m " % package.name )
    print( "\x1b[1;34m======================================> \x1b[0m " )
    print()
        
    package.download_src()
    package.unpack_src()
    print()
    ed = input( "\x1b[1;36mEdir PKGBUILD with $EDITOR [Y/n]: \x1b[0m" )
    if ed not in [ "n" , "N" ] :
        package.edit_pkgbuild()
        
    inl = package.get_install()
    
    for i in inl :
        print()
        ed = input( "\x1b[1;36mEdit %s with $EDITOR [Y/n]: \x1b[0m"%i )
        if ed not in [ "n" , "N" ] :
            package.edit_build_file( i )
    
    try :
        deps_f = package.build_depends_rec()
        
        if deps_f :
            print( "\x1b This package require the compilation of the following dependencies: \x1b[0m" )
        
        package.compile_install_depends_rec()
        package.compile()
        
        return True 
    except package_not_found as pnf_err :
        print ( " \x1b[1;31mIt is impossible to build %s \x1b[0m" % package.name )
        print ( " \x1b[1;31m%s \x1b[0m" % str( pnf_err  ) )
        raise pnf_err
    except tools.compilation_error as cerr :
        print ( " \x1b[1;31mIt is impossible to build %s \x1b[0m" % package.name )
        print ( " \x1b[1;31m An error as been occurred during the compilation of %s !  \x1b[0m" % str( cerr )  )
        raise tools.compilation_error( package.name )
    except :
        raise
        
        
    
    
def install_sequence( package , confirm=True , asdep=False ):
    
    while True :
        print()
        if confirm :
            ist = input( "\x1b[1;36m Confirm the installation of: %s with all dependencies [Y/n] \x1b[0m" % package.name )
        else :
            ist = "y"
            
        if ist in [ "y" , "Y" ] :
            package.install( asdeps=asdep )
            break 


def update_packages_base( pkgd , update_lst ):

    print()
    print()
    print("\x1b[1;32m-- Starting PACKAGES UPDATE --\x1b[0m")
    print_update_list( pkgd , update_lst )
    print()
    
    for pkg_name in update_lst :
        compile_sequence( pkgd[pkg_name] )
        install_sequence( pkgd[pkg_name] )
#         try :
#             compile_sequence( pkgd[pkg_name] )
#             install_sequence( pkgd[pkg_name] )
#         except :
#             print()
#             print ( " \x1b[1;31m The compilation of %s has been interrupted due to an error "
#                     "during the building procedure !!! \x1b[0m" % pkg_name )
#             print()
#             #####
            
            
        
        
    
    
         
         
        
        
        
    
    