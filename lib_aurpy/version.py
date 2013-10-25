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

class version( object ):
    def __init__( self , ver ):
        
        m = re.match( '^\s*\w+[\:\.\w+]*(\-\d+){0,1}\s*$' , ver )
        
        if m == None :
            print( ver )
            raise NameError( "Invalid version string: %s !!"%ver )
        
        self._ver = ver
        self._to_list()
    
    def _to_list(self):
        self._lver = re.split( '[\:\.\-]' , self._ver )
        
    def __str__(self):
        return self._ver
        
    def __lt__( self , other ):
        
        lon = -1
        
        if len( self._lver ) < len( other._lver ) :
            l1 = self._lver
            l2 = other._lver
            lon = 2
        elif len( self._lver ) > len( other._lver ) :
            l2 = self._lver
            l1 = other._lver
            lon = 1 
        else :
            l1 = self._lver
            l2 = other._lver
            lon = 0 
    
        pv1 = int(  self._lver[-1] )
        pv2 = int( other._lver[-1] )
        
        for v1 , i  in zip( l1 , range(len(l1)) )  :
            m1 = re.match( '^\d+$' , v1 )
            m2 = re.match( '^\d+$' , l2[i] )
            if m1 and m2 :                
                if int( self._lver[i] ) < int( other._lver[i] ) :
                    return True 
                elif int( self._lver[i] ) > int( other._lver[i] ) :
                    return False
            else :
                if ( self._lver[i] ) < ( other._lver[i] ) :
                    return True
                elif ( self._lver[i] ) > ( other._lver[i] ) :
                    return False
                
        if lon == 2 :
            return False
        
        if pv1 < pv2 :
            return True
        
        return False 
    
    def __gt__( self , other ):
        if other == None :
            return False
         
        return ( other < self )
    
    def __eq__( self , other ):
        if other == None :
            return False
        
        return not( ( other < self ) or ( self < other ) )
    
