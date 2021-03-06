"""Path tools.

The config files and cmd files specified are searched in paths, like matlab.

"""

import os
import shutil

# from .. import rootconfig
from mmdps import rootconfig

def splitext(file):
	"""Split ext.
	Split file.xx.gz will result .xx.gz.
	"""
	if file[-3:] == '.gz':
		name, ext = os.path.splitext(file[:-3])
		return name, ext + '.gz'
	else:
		name, ext = os.path.splitext(file)
		return name, ext

def makedirs_file(file):
	"""Makedirs for file.
	The dir is extracted use dirname.
	"""
	d = os.path.dirname(file)
	if len(d) < 1:
		# if the given file contains only filename
		return
	makedirs(d)

def makedirs(dirs):
	"""Makedirs that use exist_ok=True."""
	os.makedirs(dirs, exist_ok=True)

def rmtree(folder):
	"""Remove tree."""
	if os.path.isdir(folder):
		shutil.rmtree(folder)

def path_tolist(pathvar):
	"""Path environment variable string split to multiple paths."""
	return pathvar.split(os.path.pathsep)

def path_tovar(pathlist):
	"""Path list joined to path environment variable."""
	return os.path.pathsep.join(pathlist)

def defaultpathlist():
	"""The default search path."""
	return [os.path.abspath('.'), rootconfig.path.tools, os.path.join(rootconfig.path.tools, 'ui_programs')]

def builtinpathlist():
	"""The built-in search path.
	Configured use MMDPS_BUILTINPATH environment variable.
	The env is set in mmdpsvarsall.bat or source mmdpsvarsall.rc.
	"""
	pathvar = os.getenv('MMDPS_BUILTINPATH', '')
	return path_tolist(pathvar)

def projectpathlist():
	"""The project search path.
	You should define this env to make your own scripts reachable by name.
	"""
	pathvar = os.getenv('MMDPS_PROJECTPATH', '')
	return path_tolist(pathvar)

def searchpathlist():
	"""The full path list for searching."""
	defaultlist = defaultpathlist()
	builtinlist = builtinpathlist()
	pathvarlist = projectpathlist()
	searchpaths = []
	searchpaths.extend(defaultlist)
	searchpaths.extend(pathvarlist)
	searchpaths.extend(builtinlist)
	searchpaths.append(os.path.join(rootconfig.path.root, 'pipeline', 'DWI'))
	searchpaths.append(os.path.join(rootconfig.path.root, 'pipeline', 'T1'))
	searchpaths.append(os.path.join(rootconfig.path.root, 'pipeline', 'BOLD'))
	searchpaths.append(os.path.join(rootconfig.path.root, 'tools', 'helper_tools'))
	searchpaths.append(os.path.join(rootconfig.path.root, 'tools', 'job_runner'))
	return searchpaths

def getfilepath(filename):
	"""Search the file in all search paths, return the full path."""
	if os.path.isfile(filename):
		return os.path.abspath(filename)
	pathlist = searchpathlist()
	return findfile(filename, pathlist)

def fullfile(filename):
	"""Search the file and return the full path in all search paths."""
	return getfilepath(filename)

def findfile(filename, pathlist):
	"""Find the file in pathlist."""
	for path in pathlist:
		p = os.path.join(path, filename)
		if os.path.isfile(p):
			return os.path.abspath(p)
	return None

def env_override(defaultstr, envname):
	"""If has env of envname, use this name; else use defaultstr."""
	thestr = os.environ.get(envname)
	if thestr == None:
		print(envname, 'not set, use default', defaultstr)
		thestr = defaultstr
	return thestr

def cwd():
	"""Current working directory."""
	return os.getcwd()

def curatlasname():
	"""Current atlas name by cwd."""
	return os.path.basename(os.path.abspath(cwd()))

def curatlas():
	"""Current atlas object by cwd."""
	from ..proc import atlas
	name = curatlasname()
	return atlas.get(name)

def curparent():
	"""Current parent dirname."""
	return os.path.dirname(os.path.abspath(cwd()))

def name_date(mriscan):
	"""Split name date."""
	l = mriscan.split('_')
	return l[0], l[1]

def clean_listdir(root_path):
	"""
	Same as os.listdir, excluding non-directory
	"""
	return [dirname for dirname in sorted(os.listdir(root_path)) if os.path.isdir(os.path.join(root_path, dirname))]
