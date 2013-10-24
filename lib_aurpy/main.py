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


import lib_aurpy.package as pkg
import lib_aurpy.version as ver 
import lib_aurpy.query as que
import lib_aurpy.tools as tools 
import lib_aurpy.args as args
import lib_aurpy.glob as glob
import lib_aurpy.pacman as pacman 

from collections import OrderedDict
import sys

def full_aur_update():
    pkgd = pkg.foreign()
    
    print()
    update_lst = sorted ( pkg.test_packages( pkgd ) )
    print()
    
    pkg.test_dependencies( pkgd , update_lst )
    pkg.select_packages( pkgd , update_lst )
    pkg.update_packages( pkgd , update_lst )
    
    
def isntall_aur_pkgs( pkgs_list ):
    pkgd = pkg.build_pkgs_dict( pkgs_list , version=False )
    print( pkgd )
    update_lst = sorted ( pkg.test_packages( pkgd ) )
    print( update_lst )
    pkg.test_dependencies( pkgd , update_lst )
    pkg.select_packages( pkgd , update_lst )
    pkg.update_packages( pkgd , update_lst )
    


def main():
 
    options = args.parse_args()

    q = que.query()

    if options.version :
        print( "                       aurpy v%s" % glob.get_version() )
        print( "------------------------------------")
        print( q.pacman_version() )
        exit(0)

    if len( sys.argv ) <= 1 :
        exit(1)

    if options.aur :
        if len( options.packages ) > 0 :
            pkgs_list = sorted( list( OrderedDict.fromkeys( options.packages ).keys() ) )
            isntall_aur_pkgs( pkgs_list )
            exit(0)
    
    if options.aur and options.upgrades :
        full_aur_update()
        exit(1)
    
    argv = list( sys.argv )
    argv.pop(0) 

    ## call pacman ....
    if sum( [ options.database , options.query , options.remove , options.sync , options.deptest , options.upgrade ] ) > 1 :
        print( "error: only one operation may be used at a time" )
        exit(1) 

    if options.query or options.deptest or ( options.sync and options.info ):
        pacman.user_pacman( argv )
        return 0
    
    
    if options.database or options.upgrade or options.remove or options.sync :
        pacman.root_pacman( argv )
        return 0 

    pacman.try_pacman( argv )
    
    #tools.sync_pacman()


    
    