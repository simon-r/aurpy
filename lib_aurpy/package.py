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
import lib_aurpy.version as ver
import lib_aurpy.tools as tools
import lib_aurpy.glob as glob

class package( object ):
    def __init__( self ):
        pass

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
    
    def compile(self):
        tools.download_pkg( self.origin , self.name )
        tools.compile_pkg( self.name )
        
    
    def read_repo_data(self):
        opener = urllib.request.FancyURLopener({})
        f = opener.open( tools.get_pkg_url( self.origin , self.name ) )
        
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
             
            
        self._name = m.group(1)
        self._repo_version = ver.version( m.group(2) )
        
        return True
    
    def read_pkgbuild_data(self):
        self._pkgbuild = tools.get_pkgbuild( self.origin , self.name )
        self._pkg_data = tools.parse_pkgbuild( self._pkgbuild )
        
    
    def get_repo_version(self):
        return str( self._repo_version )
    
    repo_version = property( get_repo_version , doc="" )
    
    def get_installed_version(self):
        return str( self._installed_version )
    
    def set_installed_version(self,v):
        self._installed_version = ver.version( v )
        
    installed_version = property( get_installed_version , set_installed_version , doc="" )
    
    def new_in_repo(self):
        return  self._installed_version < self._repo_version 
    
    def install(self):
        pass

    
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
    
    print()
    
    return update_lst


def print_update_list( pkgd , update_lst ):
    for pkg , i in zip( update_lst , range( len( update_lst ) ) ):
         print( "%d. \x1b[1;33m%s \x1b[0m"%( i,pkg ) , end=" " )
         print( "\x1b[33m %s -> %s \x1b[0m"%( pkgd[pkg].installed_version , pkgd[pkg].repo_version ) , end=" " )
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
    

def update_packages( pkgd , update_lst ):

    print()
    print()
    print("\x1b[1;32m-- Starting PACKAGES UPDATE --\x1b[0m")
    print_update_list( pkgd , update_lst )
    print()
    
    for pkg_name in update_lst :
        print( "\x1b[1;34m===> \x1b[1;31mCOMPILING: \x1b[1;37m %s \x1b[0m " % pkg_name )
        pkgd[pkg_name].compile()
        
        
    
    
         
         
        
        
        
    
    