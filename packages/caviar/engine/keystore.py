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
Keystore module.
"""

# TODO Test coverage...
class Keystore:

	"""
	Keystore.
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
		
	def setup(self, subject_path, issuer_path, private_key_path):
	
		any(self.__ssh_session.execute(
			self.__das_machine.keystore_setup_begin_cmd(self.__domain_name)
		))
		
		self.__ssh_session.copy(
			subject_path,
			self.__das_machine.keystore_setup_subject_path(self.__domain_name)
		)
		self.__ssh_session.copy(
			issuer_path,
			self.__das_machine.keystore_setup_issuer_path(self.__domain_name)
		)
		self.__ssh_session.copy(
			private_key_path,
			self.__das_machine.keystore_setup_private_key_path(
				self.__domain_name
			)
		)
		
		any(self.__ssh_session.execute(
			self.__das_machine.keystore_setup_end_cmd(
				self.__domain_name,
				self.__master_password
			)
		))

