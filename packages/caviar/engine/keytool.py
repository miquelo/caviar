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
		
class Keytool:

	"""
	Keytool.
	"""
	
	def __init__(self, domain_name, ssh_session_fact, das_machine,
			master_password):

		self.__domain_name = domain_name
		self.__ssh_session = ssh_session_fact.session(
			das_machine.appserver_user,
			das_machine.host
		)
		self.__das_machine = das_machine
		self.__master_password = master_password
		
	def entries(self):
	
		"""
		List keystore entries alias.
		
		:rtype:
		   iter
		:return:
		   Iterator of entries alias.
		"""
		
		raise Exception("Unimplemented")
		
	def remove(self, alias):
	
		"""
		Remove a keystore entry.
		
		:param str alias:
		   Entry alias.
		"""
		
		raise Exception("Unimplemented")
		
class CACertificatesKeytool(Keytool):

	"""
	CA certificates keytool.
	"""
	
	def __init__(self, domain_name, ssh_session_fact, das_machine,
			master_password):
			
		super().__init__(
			domain_name,
			ssh_session_fact,
			das_machine,
			master_password
		)
		
	def put(self, alias, cacert):
	
		"""
		Put a CA certificate entry.
		
		:param str alias:
		   Entry alias.
		:param Certificate cacert:
		   CA certificate entry.
		"""
		
		raise Exception("Unimplemented")
		
class KeystoreKeytool(Keytool):

	"""
	Keystore keytool.
	"""
	
	def __init__(self, domain_name, ssh_session_fact, das_machine,
			master_password):
			
		super().__init__(
			domain_name,
			ssh_session_fact,
			das_machine,
			master_password
		)
		
	def put(self, alias, certkey):
	
		"""
		Put a certificate and key entry.
		
		:param str alias:
		   Entry alias.
		:param CertificateKey certkey:
		   Certificate and key entry.
		"""
		
		raise Exception("Unimplemented")

