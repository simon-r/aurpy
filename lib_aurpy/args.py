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
    
    parser.add_argument( "-A" , "--aur",
        action="store_true",
        dest="aur",
        help="Perform operation on AUR: aurpy --aur some_pkg .. install or upgrade the given pkg")
    
    
    parser.add_argument("-D", "--database",
        action="count",
        default=0 ,
        
        dest="database",
        help="Modify the package database.")
    
    parser.add_argument("-Q", "--query",
        action="count",
        default=0 ,
        dest="query",
        help="Query the package database")
    
    parser.add_argument("-S", "--sync",
        action="count",
        default=0 ,
        dest="sync",
        help="Synchronize packages")
    
    parser.add_argument("-R", "--remove",
        action="count",
        default=0 ,
        dest="remove",
        help="Remove package(s) from the system.")    

    parser.add_argument("-T", "--deptest",
        action="count",
        default=0 ,
        dest="deptest",
        help="Check dependencies.")
    
    parser.add_argument("-U", "--upgrade",
        action="count",
        default=0 ,
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
    
#     parser.add_argument("--", 
#         action="store_true",
#         dest="",
#         help="" )  

    parser.add_argument("-f", "--force",
        action="store_true",
        dest="force",
        help=" Bypass file conflict checks and overwrite conflicting files. " )  

    parser.add_argument("--asdeps", 
        action="store_true",
        dest="asdeps",
        help="Install packages non-explicitly; in other words, fake their install reason to be installed as a dependency. " )  

    parser.add_argument("--asexplicit", 
        action="store_true",
        dest="asexplicit",
        help="Install packages explicitly; in other words, fake their install reason to be explicitly installed." )  

    parser.add_argument("--ignore", 
        action="store",
        dest="ignore",
        help="Directs pacman to ignore upgrades of package even if there is one available. " )  

    parser.add_argument("--ignoregroup", 
        action="store",
        dest="ignoregroup",
        help="Directs pacman to ignore upgrades of all packages in group even if there is one available." )  

    parser.add_argument("--needed", 
        action="store",
        dest="needed",
        help="Do not reinstall the targets that are already up to date. " )  
    
    parser.add_argument("--recursive", 
        action="store_true",
        dest="recursive",
        help="Recursively reinstall all dependencies of the targets. " ) 
    
### Query Options

    parser.add_argument( "-c" , "--changelog", 
        action="store_true",
        dest="changelog",
        help="View the ChangeLog of a package if it exists. " ) 

    parser.add_argument( "--deps", 
        action="store_true",
        dest="deps",
        help="Restrict or filter output to packages installed as dependencies." ) 

    parser.add_argument( "-e" , "--explicit", 
        action="store_true",
        dest="explicit",
        help="Restrict or filter output to explicitly installed packages." ) 

    parser.add_argument( "-g" , "--groups", 
        action="store_true",
        dest="groups",
        help="Display all packages that are members of a named group." ) 

    parser.add_argument( "-i" , "--info", 
        action="store_true",
        dest="info",
        help="Display information on a given package. " ) 

    parser.add_argument( "-k" , "--check", 
        action="store_true",
        dest="check",
        help="Check that all files owned by the given package(s) are present on the system." ) 

    parser.add_argument( "-l" , "--list", 
        action="store_true",
        dest="list",
        help="List all files owned by a given package. Multiple packages can be specified on the command line. " ) 

    parser.add_argument( "-m" , "--foreign", 
        action="store_true",
        dest="foreign",
        help="Restrict or filter output to packages that were not found in the sync database(s)." ) 

    parser.add_argument( "-o" , "--owns", 
        action="store",
        dest="owns",
        help="Search for packages that own the specified file(s). The path can be relative or absolute and one or more files can be specified." ) 

    parser.add_argument( "--file", 
        action="store_true",
        dest="file",
        help="Signifies that the package supplied on the command line is a file and not an entry in the database." ) 

    parser.add_argument( "-q" , "--quiet", 
        action="store_true",
        dest="quiet",
        help="Show less information for certain query operations. " ) 

#     parser.add_argument( "-" , "--", 
#         action="store_true",
#         dest="",
#         help="" ) 

    parser.add_argument( "-s" , "--search", 
        action="store",
        dest="search",
        help="Search each locally-installed package for names or descriptions that match regexp." ) 

    parser.add_argument( "-t" , "--unrequired", 
        action="store_true",
        dest="unrequired",
        help="Restrict or filter output to packages not required by any currently installed package. " ) 

    parser.add_argument( "-u" , "--upgrades", 
        action="store_true",
        dest="upgrades",
        help="Restrict or filter output to packages that are out of date on the local system." ) 

### Remove Options

    parser.add_argument( "--cascade", 
        action="store_true",
        dest="cascade",
        help="Remove all target packages, as well as all packages that depend on one or more target packages." ) 

    parser.add_argument( "-n" , "--nosave", 
        action="store_true",
        dest="nosave",
        help="Instructs pacman to ignore file backup designations. " ) 

#     parser.add_argument( "--recursive", 
#         action="store_true",
#         dest="recursive",
#         help="Remove each target specified including all of their dependencies, provided that (A) they are not required by other packages." ) 

    parser.add_argument( "--unneeded", 
        action="store_true",
        dest="unneeded",
        help="Removes targets that are not required by any other packages." ) 

### Sync Options


    parser.add_argument( "--clean", 
        action="store_true",
        dest="clean",
        help="Remove packages that are no longer installed from the cache as well as currently unused sync databases to free up disk space. " ) 

#     parser.add_argument( "-g" , "--groups", 
#         action="store_true",
#         dest="groups",
#         help="Display all the members for each package group specified." ) 

#     parser.add_argument( "-i" , "--info", 
#         action="store_true",
#         dest="info",
#         help="Display information on a given sync database package. Passing two --info or -i " ) 

#     parser.add_argument( "-l" , "--list", 
#         action="store_true",
#         dest="list",
#         help="" ) 

#     parser.add_argument( "-" , "--", 
#         action="store_true",
#         dest="",
#         help="" ) 

#     parser.add_argument( "-" , "--", 
#         action="store_true",
#         dest="",
#         help="" ) 

    parser.add_argument(  "--sysupgrade" , 
        action="store_true",
        dest="sysupgrade",
        help="Upgrades all packages that are out of date. Each currently-installed package will be examined and upgraded" ) 

    parser.add_argument( "-w" , "--downloadonly", 
        action="store_true",
        dest="downloadonly",
        help="Retrieve all packages from the server, but do not install/upgrade anything." ) 

    parser.add_argument( "-y" , "--refresh", 
        action="store_true",
        dest="refresh",
        help="Download a fresh copy of the master package list from the server(s) defined in pacman.conf(5). " ) 

#     parser.add_argument( "--needed", 
#         action="store_true",
#         dest="needed",
#         help="Do not reinstall the targets that are already up to date. " ) 

#######

    parser.add_argument(
        dest="packages",
        nargs='*',
        default=[]
        )

    return parser.parse_args()
    