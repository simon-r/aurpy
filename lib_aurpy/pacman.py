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

from subprocess import call, check_output

def try_pacman ( argv ):
    
    cmd = [ "pacman" ] + argv
    
    try :
        call ( [ "pacman" ] + argv )
        return 
    except :
        pass
    
    
    cmd = [ "sudo" ] + cmd 
    
    try :
        call ( [ "sudo", "pacman" ] + argv )
        return 
    except :
        return False
    
def user_pacman ( argv ):
    cmd = [ "pacman" ] + argv
    
    try :
        call ( [ "pacman" ] + argv )
        return 
    except :
        pass

def root_pacman ( argv ):
    cmd = [ "sudo" , "pacman" ] + argv
    
    try :
        call ( cmd )
        return 
    except :
        pass