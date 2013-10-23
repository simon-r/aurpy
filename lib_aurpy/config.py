import configparser as cp
import lib_aurpy.glob as glob
import os
import os.path
import string
import random

class aurpy_config( object ):
    def __init__(self):
        self._cfg_dir = os.path.expanduser("~") + "/.config/aurpy"
        self._cfg_file = "aurpy.cfg"
        
        if not os.path.exists( self.cfg_file() ) :
            self.write_dafault()        
        
        self._config = cp.ConfigParser()
        fp = open( self.cfg_file() )
        self._config.readfp( fp )
        
    
    def cfg_file(self):
        return self._cfg_dir + "/" + self._cfg_file
    
    
    def write_dafault(self):
        config = cp.ConfigParser()
        
        config.add_section( "global" )
        config.set('global', 'compile_dir', '/tmp/aurpy' )
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