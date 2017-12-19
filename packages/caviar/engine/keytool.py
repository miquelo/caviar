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

class Entry:

	"""
	Keystore entry.
	
	:param str alias:
	   Entry alias.
	"""
	
	def __init__(self, alias):
	
		self.__alias = alias
		
	@property
	def alias(self):
	
		"""
		Entry alias.
		
		:rtype:
		   str
		"""
		
		return self.__alias
		
class CertificateEntry(Entry):

	"""
	Keystore certificate entry.
	
	:param str alias:
	   Entry alias.
	"""
	
	def __init__(self, alias):
		
		super().__init__(alias)
		
class KeyEntry(Entry):

	"""
	Ketstore private key entry.
	
	:param str alias:
	   Entry alias.
	"""
	
	def __init__(self, alias):
	
		super().__init__(alias)
		
class Keytool:

	"""
	Keytool.
	"""
	
	def __init__(self):
	
		pass
		
	def entries(self):
	
		"""
		List keystore entries.
		
		:rtype:
		   iter
		:return:
		   Iterator of :class:`Entry` items.
		"""
		
		pass
		
	def put(self, alias, certificate, key=None):
	
		"""
		Put a certificate or a private key entry.
		
		:param str alias:
		   Entry alias.
		:param Certificate certificate:
		   Entry certificate.
		:param PrivateKey key:
		   Entry private key. It becomes a :class:`CertificateEntry` when
		   this parameter is `None`, or a :class:`KeyEntry` otherwhise.
		"""
		
		pass
		
	def remove(self, alias):
	
		"""
		Remove a keystore entry.
		
		:param str alias:
		   Entry alias.
		"""
		
		pass

