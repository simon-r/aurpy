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

import argparse


def parse_args():
    desc = "A python based AUR helper for Arch Linux "
    
    parser = argparse.ArgumentParser( description=desc )
    
    parser.add_argument("-D", "--database",
        action="store_true",
        dest="database",
        help="Modify the package database.")
    
    parser.add_argument("-Q", "--query",
        action="store_true",
        dest="query",
        help="Query the package database")
    
    parser.add_argument("-S", "--sync",
        action="store_true",
        dest="sync",
        help="Synchronize packages")

    parser.add_argument("-T", "--deptest",
        action="store_true",
        dest="deptest",
        help="Check dependencies.")
    
    parser.add_argument("-U", "--upgrade",
        action="store_true",
        dest="upgrade",
        help="Upgrade or add package(s) to the system and install the required dependencies from sync repos.")
    
    parser.add_argument("-V", "--version",
        action="store_true",
        dest="version",
        help="Display version and exit.")
        
    parser.add_argument("-b", "--dbpath",
        action="store",
        dest="dbpath",
        help="Specify an alternative database location (a typical default is /var/lib/pacman).")
    
    parser.add_argument("-r", "--root",
        action="store",
        dest="root",
        help="Specify an alternative installation root (default is /)" )
    
    parser.add_argument("-v", "--verbose",
        action="store_true",
        dest="verbose",
        help="Output paths such as as the Root, Conf File, DB Path, Cache Dirs, etc. " )
    
    parser.add_argument( "--arch",
        action="store",
        dest="arch",
        help="Specify an alternate architecture. " )
    
    parser.add_argument("--cachedir", 
        action="store",
        dest="cachedir",
        help="Specify an alternative package cache location (a typical default is /var/cache/pacman/pkg)." )
    
#     parser.add_argument("", "",
#         action="store",
#         dest="",
#         help="" )    
    
    parser.add_argument("--config",
        action="store",
        dest="config",
        help="Specify an alternate configuration file. " )   
    
    parser.add_argument("--debug", 
        action="store_true",
        dest="debug",
        help="Display debug messages. When reporting bugs, this option is recommended to be used." )   
    
    parser.add_argument("--gpgdir", 
        action="store",
        dest="gpgdir",
        help="Specify a directory of files used by GnuPG to verify package signatures (a typical default is /etc/pacman.d/gnupg). " )   

    parser.add_argument("--logfile", 
        action="store",
        dest="logfile",
        help="Specify an alternate log file. This is an absolute path, regardless of the installation root setting." )
    
    parser.add_argument("--noconfirm", 
        action="store_true",
        dest="noconfirm",
        help="Bypass any and all “Are you sure?” messages. It’s not a good idea to do this unless you want to run pacman from a script. " )
    
#### Transaction Options (apply to -S, -R and -U)
    
    parser.add_argument("-d", "--nodeps" ,
        action="store_true",
        dest="nodeps",
        help="Skips dependency version checks. Package names are still checked." )    

    parser.add_argument("--dbonly", 
        action="store_true",
        dest="dbonly",
        help="Adds/Removes the database entry only, leaves all files in place." )  

    parser.add_argument("--noprogressbar", 
        action="store_true",
        dest="noprogressbar",
        help="Do not show a progress bar when downloading files. " )  
    
    parser.add_argument("--noscriptlet", 
        action="store_true",
        dest="noscriptlet",
        help="If an install scriptlet exists, do not execute it. Do not use this unless you know what you are doing." )  
    
    parser.add_argument("-p","--print" ,
        action="store_true",
        dest="print",
        help="Only print the targets instead of performing the actual operation (sync, remove or upgrade). " )  
    
    parser.add_argument("--print-format", 
        action="store",
        dest="print-format",
        help="Specify a printf-like format to control the output of the --print operation." )  
    
### Upgrade Options (apply to -S and -U)    
    
#     parser.add_argument("", 
#         action="store",
#         dest="",
#         help="" )  
    
### Query Options

### Remove Options

### Sync Options
    
    
    parser.add_argument(
        dest="packages",
        nargs='*',
        default=[]
        )

    return parser.parse_args()
    