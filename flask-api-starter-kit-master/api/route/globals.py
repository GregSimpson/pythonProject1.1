
# https://www.tutorialspoint.com/configuration-file-parser-in-python-configparser
import configparser

parser = configparser.ConfigParser()
parser.read('settings.ini')
for sect in parser.sections():
   print('gjs Section:', sect)
   for k,v in parser.items(sect):
      print(' {} = {}'.format(k,v))
   print()


#globals.py

class dbinfo :      # for database globals
    username = 'abcd'
    password = 'xyz'

class runtime :
    debug = False
    output = 'stdio'

class client :
    id = parser.get('ttec-ped-developers','client_id')
    secret = parser.get('ttec-ped-developers','client_secret')
    domain = parser.get('ttec-ped-developers', 'client_domain')

class auth0 :
    url_get_token = parser.get('Auth0Info','url_get_token')


