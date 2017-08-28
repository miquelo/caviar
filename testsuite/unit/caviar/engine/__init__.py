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
import caviar.engine

from unittest.mock import ANY, call, patch

ANY_DOMAIN_NAME = "domain"
ANY_ADMIN_PORT = 4848
ANY_ADMIN_USER = "admin"
ANY_ADMIN_PASSWORD = "12345678"

SOME_DOMAIN_NAME = "domain"
SOME_ADMIN_PORT = 4848
SOME_ADMIN_USER = "admin"
SOME_ADMIN_PASSWORD = "12345678"

SOME_MASTER_PASSWORD = "12345678"
SOME_NODE_ALLOCATOR_NAME = "node-allocator-01"
SOME_CLUSTER_NAME = "cluster-01"

SOME_DAS_SERVER_NAME = "test-das"
SOME_NODE_ALLOC_SERVER_PREFIX = "test-node-alloc"
SOME_NODE_ALLOC_SERVER_NAME = "{}-{}".format(
	SOME_NODE_ALLOC_SERVER_PREFIX,
	SOME_NODE_ALLOCATOR_NAME
)

SOME_PUBLIC_KEY_PATH = "/some/public/key/path"

class EngineTestCase(unittest.TestCase):

	def setUp(self):

		machinery_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.Machinery"
		)
		Machinery = machinery_patcher.start()
		self.addCleanup(machinery_patcher.stop)
		
		ssh_session_fact_patcher = patch(
			"caviar.network.ssh.SSHSessionFactory"
		)
		self.addCleanup(ssh_session_fact_patcher.stop)
		SSHSessionFactory = ssh_session_fact_patcher.start()
		
		self.machinery = Machinery()
		self.ssh_session_fact = SSHSessionFactory()
		
		self.engine = caviar.engine.Engine(
			self.machinery,
			self.ssh_session_fact,
			SOME_MASTER_PASSWORD,
			SOME_DAS_SERVER_NAME,
			SOME_NODE_ALLOC_SERVER_PREFIX
		)
		
	def test_management(self):
	
		management = self.engine.management(
			ANY_DOMAIN_NAME,
			ANY_ADMIN_PORT,
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		self.assertIsInstance(management, caviar.engine.management.Management)
		self.machinery.server.assert_called_once_with(SOME_DAS_SERVER_NAME)
		
	def test_asadmin(self):
	
		asadmin = self.engine.asadmin()
		
		self.assertIsInstance(asadmin, caviar.engine.asadmin.Asadmin)
		self.machinery.server.assert_called_once_with(SOME_DAS_SERVER_NAME)
		
	def test_node_allocator(self):
	
		machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.server.ServerMachine"
		)
		ServerMachine = machine_patcher.start()
		self.addCleanup(machine_patcher.stop)
		
		machine = ServerMachine()
		machine.appserver_public_key_path = SOME_PUBLIC_KEY_PATH
		self.machinery.server.return_value = machine
		
		node_allocator = self.engine.node_allocator(SOME_NODE_ALLOCATOR_NAME)
		
		self.assertIsInstance(
			node_allocator,
			caviar.engine.nodealloc.NodeAllocator
		)
		self.machinery.server.assert_has_calls([
			call(SOME_DAS_SERVER_NAME),
			call(SOME_DAS_SERVER_NAME),
			call(SOME_NODE_ALLOC_SERVER_NAME, SOME_PUBLIC_KEY_PATH)
		])
		
	def test_load_balancer(self):
	
		machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.server.ServerMachine"
		)
		ServerMachine = machine_patcher.start()
		self.addCleanup(machine_patcher.stop)
		
		machine = ServerMachine()
		machine.appserver_public_key_path = SOME_PUBLIC_KEY_PATH
		self.machinery.server.return_value = machine
		
		load_balancer = self.engine.load_balancer(SOME_CLUSTER_NAME)
		
		self.assertIsInstance(load_balancer, caviar.engine.lb.LoadBalancer)
		self.machinery.load_balancer.assert_called_once_with(
			SOME_CLUSTER_NAME,
			SOME_PUBLIC_KEY_PATH
		)
		
	def test_close(self):
	
		self.engine.close()
		
		self.ssh_session_fact.close.assert_called_once_with()

