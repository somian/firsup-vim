#!/usr/bin/python-27

# xdgvim.py - a demo script (so far) written by a py-novice (relatively).
# The purpose of this small program is to discover and compose a list of
# the vimruntime directories, bothe the system one and the user one. It
# is intended that having discovered these locations a private or 'virtual'
# vimruntime all under a user's control without su authority can be set up.
import sys
from sys import stderr
from xdg import BaseDirectory
import os
from os import environ as ev
import itertools
import re
from re import search
import subprocess

def sep_canon():
   if os.altsep: return os.altsep
   else: return os.sep

def shinah():
  fore = list()
  for grant in BaseDirectory.load_data_paths(r'vim'):
    fore.append(grant)
# print >> stderr, ('%02u entries' % len(fore))
  if len(fore) == 1:
    zop = re.compile(r'^' + fore[0] + '/vim[^/]+$')
    for sd, d, f in os.walk(fore[0] , topdown = True):
    # if sd.endswith('lang'): break
      if len(d) >= 12:
        print >> stderr, ('%s is likely parent, looking at %s' % (sd,d))
        fore.append(sd)
      elif sd != fore[0]:
        print >> stderr, ('%s is not a version-dir, skipping' % sd)
        
      d[:] = [dir for dir in d if (dir == fore[0] or zop.search(os.path.join(sd,dir)))]
   #  print >> stderr, ('Remaining: %s' % d)

  return fore

def sysvrts(pathspecs):
  usr = ('/usr/share/')
  sysonly = list()
  for ikk in pathspecs:
    if ikk.startswith(usr): sysonly.append(ikk)
  return sysonly

def lur():
  vh = list()
  spose = ''
  vh[:] = (ev.get('VIMRUNTIME', r''))
  return vh

def vim_tells_us():
  vix = u''
  our = list()
  try:
    vix = subprocess.check_output( [r'vim', r'-e', r'-T', r'dumb', r'--cmd', r'exe "set t_cm=\<C-M\>"|echo $VIMRUNTIME|quit'] )
  except subprocess.CalledProcessError as err:
    print >> stderr, ('vim query ERROR:', err)

  vix = vix.strip("\r\n")
  if vix.startswith(r'<C-M>'):
  # print >> stderr, ('Leader on string returned by vim: %s'  % vix)
    our.append( vix[vix.find('>') + 1 : len(vix) ] )
    if len(our) == 1 and our[0].startswith('/'):
      vix = our[0]

  our = vix.split(':')
  if len(our) > 1:
    vix = "\n".join(our)
  else:
    if our[0] != vix:
      print >> stderr, ('We find %s as part of %s' % (our[0] ,vix))
    else:
      print >> stderr, ('Vim tell us of just one entry: %s' % (our[0]))
 # return a list in any case
  return our

def hown():
  Home = os.path.expanduser('~')
  return re.compile('^' + Home + r'/\.vim')

def own(dpath):
  homepath = os.path.expanduser('~')
  rslt = r''
  icwd = os.getcwd()

  if not dpath:
    dpath = hown()
    return own(dpath)
  elif type(dpath) == 'str':
    print '(1) arg is %s and is a %s\n   icwd is %s' % (dpath , type(dpath) , icwd)
    if dpath == icwd:
      rslt = icwd
    elif dpath == icwd + r'/.vim':
      rslt = icwd + r'/.vim'

    else:
      print  >> stderr, '(1) arg is %s and icwd is %s' % (dpath , icwd)

  elif type(dpath) != 'str':
    print >>stderr, ('We are now in %s' % icwd)
    print >>stderr, ( '(2) arg is %s' % str(dpath) )
    boole = False
    try:
      boole = dpath.search(re.escape(icwd))
    except AttributeError as AE:
      print >> stderr, '(3) arg is %s and is unexpectedly a %s' % (str(dpath) , type(dpath))
      dpath = re.compile(dpath)
    finally:
      boole = dpath.search(re.escape(icwd))
   #  return r''

    if boole is False:
      try:
        os.chdir(homepath)
        print >>stderr, ('We are now in %s' % os.getcwd())
        own(os.getcwd() + r'/.vim')
      except OSError as err:
        print >> stderr, ('FAIL return : tried to chdir to %s and got %s' % err.filename, err.strerror)
        return 'Failure'
    else:
      waq = os.path.join(homepath, '.vim')
      print >> stderr, ('We ought to find ourselves in %s' % waq)
      return waq
  else:
    print >> stderr, '(3) arg is %s and is unexpectedly a %s' % (str(dpath) , type(dpath))
    return 'FAILURE'
 #  try:
 #    os.chdir(homepath)
 #  except OSError as err:
 #    print >> stderr, ('FAIL return : tried to chdir to %s and got %s' % err.filename, err.strerror)
 #    return 'FAILURE'

  return rslt

def xdg_usr_data():
  x_d_h = os.path.expanduser(BaseDirectory.xdg_data_home)
  return x_d_h

def _reduce_funct_(AA,AB):
  pathelsep = os.pathsep

  if  AA == AB: return AA
  elif AB in AA: return AA
  else: return pathelsep.join([AA , AB])
  return 'DUD'

unhom = sysvrts(shinah())
vtell = vim_tells_us()
jaa = lur()
parf = sep_canon().join( [xdg_usr_data(), 'vim'] )
# dall = shinah() + lur()
# print out lur() and vim_tells_us()
print >> stderr, ('system dirs according to xdg: %-34s\n' % unhom)
print >> stderr, ('system dirs according to vim: %-34s\n' % vtell)
print >> stderr, ('user h dir  according to xdg: %-34s\n' % parf)

if len(jaa) == 1 and jaa[0] != vim_tells_us()[0]:
  print >> stderr, ('runtime dirs modified in ENV: %-34s\n' % lur())

runtl = reduce(_reduce_funct_, itertools.chain(unhom,vtell), '/usr/share/vim')
sys.stdout.write( 'System List of Dirs: ' + runtl +"\n")
# Now find the vim directory under own()
sys.stdout.write( "\n" + 'VIMRUNTIME including xdg-style user dir: ' + os.pathsep.join( [parf, own(''), runtl ]) + "\n")
