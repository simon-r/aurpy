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
    
    parser.add_argument("", "",
        action="store_true",
        dest="",
        help="")