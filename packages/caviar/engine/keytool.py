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

	def __init__(self, domain_name, ssh_session_fact, das_machine,
			master_password):
			
		self.__domain_name = domain_name
		self.__ssh_session = ssh_session_fact.session(
			das_machine.appserver_user,
			das_machine.host
		)
		self.__das_machine = das_machine
		self.__master_password = master_password
		
	def aliases(self):
	
		pass
		
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
		self.__file_path = das_machine.keystore_file_path
		
	def put(self, alias, cacert):
	
		"""
		Put a CA certificate entry.
		
		:param str alias:
		   Entry alias.
		:param Certificate cacert:
		   CA certificate entry.
		"""
		
		try:
			any(self.__ssh_session.execute(
				self.__das_machine.keytool_update_begin_cmd(
					self.__domain_name
				)
			))
			
			raise Exception("Unimplemented")
			
		finally:
			any(self.__ssh_session.execute(
				self.__das_machine.keytool_update_cacerts_cmd(
					self.__domain_name,
					alias,
					self.__master_password
				)
			))
		
class KeystoreKeytool(Keytool):

	"""
	Keystore keytool.
	"""

