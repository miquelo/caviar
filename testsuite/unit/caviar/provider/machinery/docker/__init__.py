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

import docker
import unittest

import caviar

from unittest.mock import ANY, call, patch

SOME_BASE_NAME = "prefix"
SOME_MGMT_PUBLIC_KEY_PATH = "/some/public/key.pem"

SOME_SERVER_NAME = "srv"

NONE_OUTPUT = None

class MachineryTestCase(unittest.TestCase):

	def setUp(self):

		docker_client_patcher = patch(
			"docker.APIClient"
		)
		DockerClient = docker_client_patcher.start()
		self.addCleanup(docker_client_patcher.stop)
		
		self.client = DockerClient()
		
		self.machinery = caviar.provider.machinery.docker.Machinery(
			{
				"client": self.client,
				"build-images": True,
				"base-name": SOME_BASE_NAME
			},
			SOME_MGMT_PUBLIC_KEY_PATH,
			NONE_OUTPUT
		)
		
	def test_build_images(self):
	
		#	self.client.build.assert_has_calls([
		#		call(path=ANY, tag=ANY, rm=True),
		#		call(path=ANY, tag=ANY, rm=True)
		#	])
		
		pass
		
	def test_server_node_dir(self):
	
		server_node_dir = self.machinery.server_node_dir
		
		self.assertIsInstance(server_node_dir, str)
		
	def test_server(self):
	
		machine = self.machinery.server(SOME_SERVER_NAME)
		
		self.assertIsInstance(
			machine,
			caviar.provider.machinery.docker.server.ServerMachine
		)

