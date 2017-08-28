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
SOME_HOST = "host"

ANY_STATE = "happy"

class MachineTestCase(unittest.TestCase):

	def setUp(self):
	
		docker_client_patcher = patch(
			"docker.APIClient"
		)
		DockerClient = docker_client_patcher.start()
		self.addCleanup(docker_client_patcher.stop)
		
		self.client = DockerClient()
		
		self.machine = caviar.provider.machinery.docker.machine.Machine(
			client=self.client,
			container_id=SOME_CONTAINER_ID
		)
		
	def test_host(self):
	
		self.client.containers.return_value = [{
			"State": ANY_STATE,
			"NetworkSettings": {
				"Networks": {
					"bridge": {
						"IPAddress": SOME_HOST
					}
				}
			}
		}]
		
		host = self.machine.host
		
		self.assertEqual(host, SOME_HOST)
		
class MachineInfoTestCase(unittest.TestCase):

	def setUp(self):
	
		docker_client_patcher = patch(
			"docker.APIClient"
		)
		DockerClient = docker_client_patcher.start()
		self.addCleanup(docker_client_patcher.stop)
		
		self.client = DockerClient()
		self.client.containers.return_value = [{
			"State": ANY_STATE,
			"NetworkSettings": {
				"Networks": {
					"bridge": {
						"IPAddress": SOME_HOST
					}
				}
			}
		}]
		
		self.info = caviar.provider.machinery.docker.machine.MachineInfo(
			client=self.client,
			container_id=SOME_CONTAINER_ID
		)
		
	def test_host(self):
		
		host = self.info.host
		
		self.assertEqual(host, SOME_HOST)

