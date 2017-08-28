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

import paramiko
import unittest

import caviar
import caviar.provider.ssh.paramiko

from unittest.mock import ANY, patch

SOME_CMD = "ssh command"

ANY_PRIVATE_KEY_PATH = "/private/key.pem"

UNREAL_TARGET = caviar.network.ssh.SSHUserHost("unreal", "unreal")

class SSHClientTestCase(unittest.TestCase):

	def setUp(self):

		self.ssh_client = caviar.provider.ssh.paramiko.SSHClient()
		
	def test_login(self):
	
		with self.assertRaises(caviar.network.ssh.SSHUnavailableSessionError):
			self.ssh_client.login(
				UNREAL_TARGET,
				ANY_PRIVATE_KEY_PATH
			)
			
	def test_close(self):
	
		pass
		
class SSHPhysicalSessionTestCase(unittest.TestCase):

	def setUp(self):
	
		paramiko_client_patcher = patch(
			"paramiko.SSHClient"
		)
		SSHClient = paramiko_client_patcher.start()
		self.addCleanup(paramiko_client_patcher.stop)
		
		self.paramiko_client = SSHClient()
		
		self.physical_session = \
				caviar.provider.ssh.paramiko.SSHPhysicalSession(
			self.paramiko_client
		)
		
	def test_execute(self):
	
		self.paramiko_client.exec_command.return_value = ( 1, 2, 3 )
		
		self.physical_session.execute(SOME_CMD)
		
		self.paramiko_client.exec_command.assert_called_once_with(SOME_CMD)
		
	def test_logout(self):
	
		self.physical_session.logout()
		
		self.paramiko_client.exec_command.assert_called_once_with(ANY)

