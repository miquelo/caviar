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
Keytool module.
"""

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
		
	def __update(self, op, arg):
	
		try:
			any(self.__ssh_session.execute(
				self.__das_machine.keystore_update_begin_cmd(
					self.__domain_name
				)
			))
			op(arg)
		finally:
			any(self.__ssh_session.execute(
				self.__das_machine.keystore_update_end_cmd(
					self.__domain_name,
					self.__master_password
				)
			))
			
	def __append_cacerts_op(self, cacerts):
	
		for cacert in cacerts:
			with cacert.open() as cacert_file:
				self.__ssh_session.copy(
					cacert_file,
					self.__das_machine.keystore_cacert_path(
						self.__domain_name
					)
				)
				
	def __replace_admin_certkey_op(self, admin_certkey):
	
		with admin_certkey.certificate.open() as admin_cert_file:
			self.__ssh_session.copy(
				admin_cert_file,
				self.__das_machine.keystore_admin_cert_path(
					self.__domain_name
				)
			)
		with admin_certkey.key.open() as admin_key_file:
			self.__ssh_session.copy(
				admin_key_file,
				self.__das_machine.keystore_admin_key_path(
					self.__domain_name
				)
			)
			
	def __replace_inst_certkey_op(self, inst_certkey):
	
		with inst_certkey.certificate.open() as inst_cert_file:
			self.__ssh_session.copy(
				inst_cert_file,
				self.__das_machine.keystore_inst_cert_path(
					self.__domain_name
				)
			)
		with inst_certkey.key.open() as inst_key_file:
			self.__ssh_session.copy(
				inst_key_file,
				self.__das_machine.keystore_inst_key_path(
					self.__domain_name
				)
			)
			
	def append_cacerts(self, cacerts):
	
		self.__update(self.__append_cacerts_op, cacerts)
		
	def replace_admin_certkey(self, admin_certkey):
	
		self.__update(self.__replace_admin_certkey_op, admin_certkey)
		
	def replace_inst_certkey(self, inst_certkey):
	
		self.__update(self.__replace_inst_certkey_op, inst_certkey)

