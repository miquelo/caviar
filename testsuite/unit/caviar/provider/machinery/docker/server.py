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

import unittest

import caviar
import caviar.provider.machinery.docker.server

from unittest.mock import patch

SOME_CONTAINER_ID = "a1b2c3d4"
SOME_APPSERVER_USER = "appserver"
SOME_APPSERVER_PUBLIC_KEY_PATH = "/appserver/public/key.pem"

ANY_ASADMIN_ARGS = [
	"arg1", "arg2", "arg3"
]
ANY_PASSWORD_ID = "abcdef"
ANY_PASSWORDS = {
	"pwd1": "12345678",
	"pwd2": "87654321"
}

ANY_DOMAIN_NAME = "domain"
ANY_NODE_NAME = "node"
ANY_NODE_HOST = "host"

class ServerMachineTestCase(unittest.TestCase):

	def setUp(self):
	
		docker_client_patcher = patch(
			"docker.APIClient"
		)
		DockerClient = docker_client_patcher.start()
		self.addCleanup(docker_client_patcher.stop)
		
		client = DockerClient()
		
		self.machine = caviar.provider.machinery.docker.server.ServerMachine(
			client=client,
			container_id=SOME_CONTAINER_ID,
			appserver_user=SOME_APPSERVER_USER,
			appserver_public_key_path=SOME_APPSERVER_PUBLIC_KEY_PATH
		)
		
	def test_appserver_user(self):
	
		appserver_user = self.machine.appserver_user
		
		self.assertEqual(appserver_user, SOME_APPSERVER_USER)
		
	def test_appserver_public_key_path(self):
	
		public_key_path = self.machine.appserver_public_key_path
		
		self.assertEqual(public_key_path, SOME_APPSERVER_PUBLIC_KEY_PATH)
		
	def test_password_file_path(self):
	
		cmd = self.machine.password_file_path(ANY_PASSWORD_ID)
		
		self.assertIsInstance(cmd, str)
		
	def test_asadmin_cmd(self):
	
		cmd = self.machine.asadmin_cmd(ANY_ASADMIN_ARGS)
		
		self.assertIsInstance(cmd, str)
		
	def test_create_password_file_cmd(self):
	
		cmd = self.machine.create_password_file_cmd(
			ANY_PASSWORD_ID,
			ANY_PASSWORDS
		)
		
		self.assertIsInstance(cmd, str)
		
	def test_delete_password_file_cmd(self):
	
		cmd = self.machine.delete_password_file_cmd(
			ANY_PASSWORD_ID
		)
		
		self.assertIsInstance(cmd, str)
		
	def test_install_master_password_cmd(self):
	
		cmd = self.machine.install_master_password_cmd(
			ANY_DOMAIN_NAME,
			ANY_NODE_NAME,
			ANY_NODE_HOST
		)
		
		self.assertIsInstance(cmd, str)

