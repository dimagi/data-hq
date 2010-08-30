#Adapted from http://code.google.com/p/keyczar/wiki/SamplePythonUsage
import os
import settings
from keyczar import keyczar
from keyczar import keyczart
from keyczar.errors import KeyczarError

#need to create 256 bit aeskey
#keyczart addkey --location=aes_keyset --status=primary --size=256

# Note that the names used in these format strings
# should be used in your code
#
FMT_CREATE = 'create --location=%(loc)s --purpose=crypt'
FMT_ADDKEY = 'addkey --location=%(loc)s --status=primary --size=256'
#


def _require_dir( loc):
    '''Make sure that loc is a directory.
    If it does not exist, create it.
    '''
    if os.path.exists( loc):
        if not os.path.isdir( loc):
            raise ValueError( '%s must be a directory' % loc)
    else:
        # should we verify that containing dir is 0700?
        os.makedirs( loc, 0755)

def _tool(fmt, **kwds):
    '''Package the call to keyczart.main
    which is awkwardly setup for command-line use without
    organizing the underlying logic for direct function calls.
    '''
    return keyczart.main( (fmt % kwds).split() )
    
def _initialize(loc, **kwds):
    '''Initialize a location
    create it
    add a primary key
    '''
    _require_dir( loc)
    steps = [ FMT_CREATE, FMT_ADDKEY]
    for step in steps:
        _tool( step, loc=loc, **kwds)

class Crypter(object):
    '''Simplify use of keyczar.Crypter class
    '''
    location = 'stdkeyset'

    @staticmethod
    def _read(loc):
        return keyczar.Crypter.Read( loc)

    def __init__( self, loc=None):
        if loc is None:
            loc = self.location
        try:
            self.crypt = self._read( loc)
        except KeyczarError:
            _initialize( loc)
            self.crypt = self._read( loc)

    def encrypt( self, s):
        return self.crypt.Encrypt( s)

    def decrypt( self, s):
        return self.crypt.Decrypt( s)


def make_device_key(device_id):    
    location = os.path.join(settings.KEYSTORE_PATH, device_id)
    if not os.path.exists(device_id):
        os.mkdir(location)
    _initialize(location)
    fin = open(os.path.join(location,'1'))
    keyjson = fin.read()
    fin.close()
    return keyjson


#if __name__ == '__main__':
#    crypter = Crypter()
#    input = 'Library Reference (keep this under your pillow)'
#    print len(input), input
#    c = crypter.encrypt( input)
#    print len(c), c
#    plain = crypter.decrypt( c)
#    assert plain == input, ' in<%s>\nout<%s>' % (input, plain)