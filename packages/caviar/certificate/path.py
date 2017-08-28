#
# This file is part of CAVIAR.
#
# CAVIAR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CAVIAR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CAVIAR.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Path certificate module.
"""

class PathCertificate:

	"""
	Path :class:`Certificate` implementation.
	
	:param str path:
	   Certificate file path.
	"""
	
	def __init__(self, path):
	
		self.__path = path
		
	def open(self):
	
		"""
		Open certificate for reading.
		
		:rtype:
		   fileobj
		:return:
		   The opened certificate for reading.
		"""
		
		return open(self.__path, "r")
		
class PathPrivateKey:

	"""
	Path :class:`PrivateKey` implementation.
	
	:param str path:
	   Private key file path.
	:param str password:
	   Password used to encrypt this private key, if any.
	"""
	
	def __init__(self, path, password=None):
	
		self.__path = path
		self.__password = password
		
	@property
	def password(self):
	
		"""
		Password used to encrypt this private key, if any.
		
		:rtype:
		   str
		"""
		
		return self.__password
		
	def open(self):
	
		"""
		Open private key for reading.
		
		:rtype:
		   fileobj
		:return:
		   The opened private key for reading.
		"""
		
		return open(self.__path, "r")

