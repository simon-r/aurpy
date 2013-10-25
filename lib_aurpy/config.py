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



import configparser as cp
import lib_aurpy.glob as glob
import os
import os.path
import string
import random
import sqlite3


class aurpy_config( object ):
    def __init__(self):
        self._cfg_dir = os.path.expanduser("~") + "/.config/aurpy"
        self._cfg_file = "aurpy.cfg"
        
        self._database = """ create table package (
                                name text not null unique ,
                                id integer primary key autoincrement , 
                                compile_dir text ,
                                base_package integer ,
                                origin text ,
                                origin_pkgbuild_url text ,
                                origin_src_pkg_url text
                                )  """.strip()
        
        self._sqlite_file = "aurpy.sqlite"
        
        if not os.path.exists( self.cfg_file() ) :
            self.write_dafault()   
            
        if not os.path.exists( self.sqlite_file() ) :
            self.init_database()      
        
        self._config = cp.ConfigParser()
        fp = open( self.cfg_file() )
        self._config.readfp( fp )
        

        
    
    def cfg_file(self):
        return self._cfg_dir + "/" + self._cfg_file
    
    def sqlite_file(self):
        return self._cfg_dir + "/" + self._sqlite_file
    
    
    def init_database(self):
        conn = sqlite3.connect( self.sqlite_file() )
        c = conn.cursor()
        c.execute( self._database )
        conn.commit()
        c.close()
    
    def write_dafault(self):
        config = cp.ConfigParser()
        
        config.add_section( "global" )
        config.set('global', 'compile_dir', '/tmp/aurpy/pkg' )
        config.set('global', 'tmp_dir', '/tmp/aurpy/tmp' )
        config.set('global', 'download', 'wget' )
        
        config.add_section( "aur" )
        config.set('aur', 'url', 'https://aur.archlinux.org/packages')
        
        if not os.path.exists(self._cfg_dir):
            os.makedirs(self._cfg_dir)
        
        with open( self.cfg_file() , 'w' ) as configfile:
            config.write( configfile )
        
        configfile.close()
        
        
    def get_aur_url(self):
        return self._config.get( "aur" , "url" )
    
    def get_tmp_dir(self):
        return self._config.get( "global" , "tmp_dir" )
    
    def get_tmp_rnd_dir(self):
        chars=string.ascii_uppercase + string.digits
        return self.get_tmp_dir() + "/" + ''.join(random.choice(chars) for x in range(20))
    
    def get_pkg_build_dir( self , pkg_name ):
        return self.get_compile_dir( pkg_name ) + "/" + pkg_name
    
    def _sqlite_get_compile_dir( self , pkg_name ):
        conn = sqlite3.connect( self.sqlite_file() )
        c = conn.cursor()
        
        qe = " select compile_dir from package where name == \"%s\" " % pkg_name
        
        c.execute( qe )
        res = None 
        
        for row in c:
            res = row[0]
        c.close()
        return res 
    
    def get_compile_dir( self , pkg_name=None ):
        
        if pkg_name != None :
            cd = self._sqlite_get_compile_dir( pkg_name )
            if cd :
                return cd
        
        return self._config.get( "global" , "compile_dir" )    
    
    def set_subpackages(self , base_pkg_name , sub_pkg_names ):
        """
        Insert a base package plus his sub-packages in the database  
        :param pkg_name: The name of the package
        :param sub_pkg_names: A list with the names of the sub-packages
        """          
        conn = sqlite3.connect( self.sqlite_file() )
        c = conn.cursor()
        qe = " select * from package where name == \"%s\" " % base_pkg_name
        
        res = None
        c.execute( qe )
        for row in c:
            res = row[0]
        
        if res :
            sbs = self.has_subpackages(base_pkg_name)
        else :
            qe = "insert into package ( name ) values ( \"%s\" ) "% ( base_pkg_name )
            c.execute( qe )
            conn.commit()
            
            qe = "select id from package where name == \"%s\" " % base_pkg_name
            c.execute( qe )
            id_base = -1
            for row in c:
                id_base = row[0]
            
            for p in sub_pkg_names :
                if p == base_pkg_name : 
                    qe = "update package set base_package = %s  where name == \"%s\" "% ( id_base , base_pkg_name )
                    continue
                qe = "insert into package ( name , base_package ) values ( \"%s\" , %s ) "% ( base_pkg_name , id_base )
                c.execute( qe )
            conn.commit()
        
        c.close()
    
        
    def is_subpackage( self , pkg_name ):
        """
        If the installed package is a sub-package it returns the name of the base package
        :param pkg_name: The name of the package
        :rtype: return the name of the main package or if do not exists return None  
        """        
        conn = sqlite3.connect( self.sqlite_file() )
        c = conn.cursor()
        
        qe = " select name from package where id in ( select base_package from package where name == \"%s\" ) " % pkg_name
        
        res = None
        c.execute( qe )
        for row in c:
            res = row[0]        
        
        c.close()
        
        return res  
    
    def has_subpackages( self , pkg_name ):
        """
        If the installed package has some sub-packages it returns a list containing the names of the sub-packages
        :param pkg_name: The name of the package
        :rtype: return the name of the sub package or if do not exists return None  
        """         
        conn = sqlite3.connect( self.sqlite_file() )
        c = conn.cursor()
        
        qe = " select name from package where base_package in ( select id from package where name == \"%s\" ) " % pkg_name
        
        res = []
        c.execute( qe )
        for row in c:
            res.append( row[0] )        
        
        c.close()
        
        if len( res ) > 0 :
            return res
        else : 
            return None
        
    
    def get_aur_dw_pkg_url( self , pkg_name ):
        return self.get_aur_url() + "/" + pkg_name[:2] + "/" + pkg_name + "/" + pkg_name + ".tar.gz"
      
    def get_pkg_url( self , origin , pkg_name ):
                
        if origin == glob.AUR :
            return self._config.get( "aur" , "url" ) + "/" + pkg_name
        elif origin == glob.PACKAGES :
            return ""
        
    def get_pkgbuild_url( self , origin , pkg_name ):
        
        if origin == glob.AUR :
            return self._config.get( "aur" , "url" ) + "/" + pkg_name[:2] + "/" + pkg_name + "/" + "PKGBUILD"
    
        return ""