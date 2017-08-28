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
Certificate module.
"""

class SimpleCertificateKey:

	"""
	Simple :class:`CertificateKey` implementation.
	
	:param Certificate certificate:
	   Certificate element.
	:param PrivateKey key:
	   Private key element.
	"""
	
	def __init__(self, certificate, key):
	
		self.__certificate = certificate
		self.__key = key
		
	@property
	def certificate(self):
	
		"""
		Certificate element.
		
		:rtype:
		   Certificate
		"""
		
		return self.__certificate
		
	@property
	def key(self):
	
		"""
		Private key element.
		
		:rtype:
		   PrivateKey
		"""
		
		return self.__key

