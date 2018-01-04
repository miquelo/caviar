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

	def __init__(self, ssh_session_fact, das_machine, master_password):
			
		self.__ssh_session = ssh_session_fact.session(
			das_machine.appserver_user,
			das_machine.host
		)
		self.__das_machine = das_machine
		self.__master_password = master_password
		
	def __connection(self, domain_name, file_path):
	
		return KeytoolConnection(
			domain_name,
			file_path,
			self.__ssh_session_fact.session(
				self.__das_machine.appserver_user,
				self.__das_machine.host
			),
			self.__das_machine,
			self.__master_password
		)
		
	def cacerts(self, domain_name):
	
		return self.__connection(
			domain_name,
			self.__das_machine.cacerts_file_path
		)
		
	def keystore(self, domain_name):
	
		return self.__connection(
			domain_name,
			self.__das_machine.keystore_file_path
		)
		
class KeytoolConnection:

	def __init__(self, domain_name, file_path, ssh_session, das_machine,
			master_password):
			
		self.__domain_name = domain_name
		self.__file_path = file_path
		self.__ssh_session = ssh_session
		self.__das_machine = das_machine
		self.__master_password = master_password
		
	def aliases(self):
	
		raise Exception("Unimplemented")
		
	def self_signed(self, alias, subject):
	
		raise Exception("Unimplemented")
		
	def put(self, alias, certificate, key=None):
	
		"""
		Put an entry.
		
		:param str alias:
		   Entry alias.
		:param Certificate certificate:
		   Certificate entry.
		:param PrivateKey key:
		   Private key. If it is `None`, this entry is a CA certificate.
		   Otherwise, this entry is a certificate and private key pair.
		"""
		
		try:
			any(self.__ssh_session.execute(
				self.__das_machine.keytool_put_begin_cmd(
					self.__domain_name
				)
			))
			
			with certificate.open() as certificate_file:
				self.__ssh_session.copy(
					certificate_file,
					self.__das_machine.keytool_certificate_path(
						self.__domain_name
					)
				)
			
			if key is not None:	
				with key.open() as key_file:
					self.__ssh_session.copy(
						key_file,
						self.__das_machine.keytool_key_path(
							self.__domain_name
						)
					)
				
		finally:
			any(self.__ssh_session.execute(
				self.__das_machine.keytool_put_end_cmd(
					domain_name=self.__domain_name,
					alias=alias,
					master_password=self.__master_password,
					file_path=self.__file_path
				)
			))
			
	def remove(self, alias):
	
		raise Exception("Unimplemented")

