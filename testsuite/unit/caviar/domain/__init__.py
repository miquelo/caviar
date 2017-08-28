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
import caviar.domain

from unittest.mock import ANY, patch

SOME_DOMAIN_NAME = "domain-01"
SOME_ADMIN_HOST = "localhost"
SOME_ADMIN_PORT = 4848
SOME_ADMIN_USER = "admin"
SOME_ADMIN_PASSWORD = "12345678"
SOME_CERTIFICATE = caviar.domain.Certificate(
	subject_path="/subject",
	issuer_path="/issuer",
	private_key_path="/private/key"
)

SOME_NODE_DIR = "/node"

SOME_DOMAIN_DATA_LIST = [
	{
		"name": SOME_DOMAIN_NAME,
		"admin-host": None,
		"admin-port": None,
		"running": None,
		"restart-required": None
	},
	{
		"name": "domain-02",
		"admin-host": None,
		"admin-port": None,
		"running": None,
		"restart-required": None
	}
]

SOME_DOMAIN_LIST = [
	caviar.domain.Domain(
		None,
		SOME_DOMAIN_NAME,
		None,
		None,
		None,
		None
	),
	caviar.domain.Domain(
		None,
		"domain-02",
		None,
		None,
		None,
		None
	)
]

SOME_NODE_ALLOCATOR_HOST = "node-allocator-host-01"

FIRST_NODE_NAME = "node-01"
SECOND_NODE_NAME = "node-02"
THIRD_NODE_NAME = "node-03"

THREE_NODE_LIST = [
	caviar.domain.node.Node(
		None,
		FIRST_NODE_NAME
	),
	caviar.domain.node.Node(
		None,
		SECOND_NODE_NAME
	),
	caviar.domain.node.Node(
		None,
		THIRD_NODE_NAME
	)
]

FIRST_CLUSTER_NAME = "cluster-01"
SECOND_CLUSTER_NAME = "cluster-02"
THIRD_CLUSTER_NAME = "cluster-03"

THREE_CLUSTER_LIST = [
	caviar.domain.cluster.Cluster(
		None,
		FIRST_CLUSTER_NAME
	),
	caviar.domain.cluster.Cluster(
		None,
		SECOND_CLUSTER_NAME
	),
	caviar.domain.cluster.Cluster(
		None,
		THIRD_CLUSTER_NAME
	)
]

ANY_MACHINERY_MODULE_NAME = "testsuite.unit.caviar.provider.machinery.fake"
ANY_MACHINERY_PARAMS = {}
ANY_MGMT_PUBLIC_KEY_PATH = "mgmt-public-key.pem"
ANY_MGMT_PRIVATE_KEY_PATH = "mgmt-private-key.pem"
ANY_MASTER_PASSWORD = "12345678"
ANY_SSH_MODULE_NAME = "testsuite.unit.caviar.provider.ssh.fake"

ANY_DOMAIN_NAME = "domain"

ANY_ADMIN_HOST = "localhost"
ANY_ADMIN_PORT = 4848
ANY_ADMIN_USER = "admin"
ANY_ADMIN_PASSWORD = "12345678"

ANY_NODE_ALLOCATOR_NAME = "node-allocator"

class TestCase(unittest.TestCase):

	def test_environment(self):

		environment = caviar.domain.environment(
			ANY_MACHINERY_MODULE_NAME,
			ANY_MACHINERY_PARAMS,
			ANY_MGMT_PUBLIC_KEY_PATH,
			ANY_MGMT_PRIVATE_KEY_PATH,
			ANY_MASTER_PASSWORD,
			ssh_module_name=ANY_SSH_MODULE_NAME
		)
		
		self.assertIsInstance(environment, caviar.domain.Environment)

class DomainTestCase(unittest.TestCase):

	def setUp(self):

		engine_patcher = patch(
			"caviar.engine.Engine"
		)
		Engine = engine_patcher.start()
		self.addCleanup(engine_patcher.stop)
		
		asadmin_patcher = patch(
			"caviar.engine.asadmin.Asadmin"
		)
		Asadmin = asadmin_patcher.start()
		self.addCleanup(asadmin_patcher.stop)
		
		self.engine = Engine()
		
		self.asadmin = Asadmin()
		self.engine.asadmin.return_value = self.asadmin
		
	def test_name(self):
	
		some_domain = caviar.domain.Domain(
			self.engine,
			SOME_DOMAIN_NAME,
			ANY_ADMIN_HOST,
			ANY_ADMIN_PORT,
			running=False,
			restart_required=False
		)
		
		self.assertEqual(some_domain.name, SOME_DOMAIN_NAME)
		
	def test_manage(self):

		any_domain = caviar.domain.Domain(
			self.engine,
			ANY_DOMAIN_NAME,
			ANY_ADMIN_HOST,
			ANY_ADMIN_PORT,
			running=False,
			restart_required=False
		)
		
		managed_domain = any_domain.manage(
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		self.assertIsInstance(managed_domain, caviar.domain.ManagedDomain)
		
	def test_manage_ready(self):

		ready_domain = caviar.domain.Domain(
			self.engine,
			SOME_DOMAIN_NAME,
			ANY_ADMIN_HOST,
			ANY_ADMIN_PORT,
			running=True,
			restart_required=False
		)
		
		ready_domain.manage(
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		self.asadmin.start_domain.assert_not_called()
		self.asadmin.restart_domain.assert_not_called()
		
	def test_manage_stopped(self):

		ready_domain = caviar.domain.Domain(
			self.engine,
			SOME_DOMAIN_NAME,
			ANY_ADMIN_HOST,
			ANY_ADMIN_PORT,
			running=False,
			restart_required=False
		)
		
		ready_domain.manage(
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		self.asadmin.start_domain.assert_called_once_with(
			SOME_DOMAIN_NAME
		)
		self.asadmin.restart_domain.assert_not_called()
		
	def test_manage_restart_required(self):

		ready_domain = caviar.domain.Domain(
			self.engine,
			SOME_DOMAIN_NAME,
			ANY_ADMIN_HOST,
			ANY_ADMIN_PORT,
			running=True,
			restart_required=True
		)
		
		ready_domain.manage(
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		self.asadmin.start_domain.assert_not_called()
		self.asadmin.restart_domain.assert_called_once_with(
			SOME_DOMAIN_NAME
		)
		
class ManagedDomainTestCase(unittest.TestCase):

	def setUp(self):

		engine_patcher = patch(
			"caviar.engine.Engine"
		)
		Engine = engine_patcher.start()
		self.addCleanup(engine_patcher.stop)
		
		management_patcher = patch(
			"caviar.engine.management.Management"
		)
		Management = management_patcher.start()
		self.addCleanup(management_patcher.stop)
		
		management_resource_patcher = patch(
			"caviar.engine.management.ManagementResource"
		)
		ManagementResource = management_resource_patcher.start()
		self.addCleanup(management_resource_patcher.stop)
		
		node_allocator_patcher = patch(
			"caviar.engine.nodealloc.NodeAllocator"
		)
		NodeAllocator = node_allocator_patcher.start()
		self.addCleanup(node_allocator_patcher.stop)

		engine = Engine()
		engine.server_node_dir = SOME_NODE_DIR
		
		management = Management()
		engine.management.return_value = management
		
		self.management_res = ManagementResource()
		child_res = self.management_res.extra_properties.child_resources
		child_res.__getitem__.return_value = self.management_res
		management.domain.return_value = self.management_res
		
		self.some_node_allocator = NodeAllocator()
		self.some_node_allocator.prepare.return_value = SOME_NODE_ALLOCATOR_HOST
		engine.node_allocator.return_value = self.some_node_allocator

		self.managed_domain = caviar.domain.ManagedDomain(
			caviar.domain.ManagedDomainContext(
				engine,
				SOME_DOMAIN_NAME,
				ANY_ADMIN_PORT,
				SOME_ADMIN_USER,
				SOME_ADMIN_PASSWORD
			)
		)
		
	def test_nodes(self):
	
		child_res = self.management_res.extra_properties.child_resources
		child_res.items.return_value = [
			( FIRST_NODE_NAME, self.management_res ),
			( SECOND_NODE_NAME, self.management_res ),
			( THIRD_NODE_NAME, self.management_res )
		]
		self.management_res.extra_properties.entity.type = "SSH"
		
		node_list = list(self.managed_domain.nodes())
		
		self.assertListEqual(node_list, THREE_NODE_LIST)
		
	def test_create_node(self):
	
		child_res = self.management_res.extra_properties.child_resources
		child_res.items.return_value = [
			( FIRST_NODE_NAME, self.management_res )
		]
		self.management_res.extra_properties.entity.type = "SSH"
		
		some_node = self.managed_domain.create_node(
			FIRST_NODE_NAME,
			ANY_NODE_ALLOCATOR_NAME
		)
		
		self.some_node_allocator.prepare.assert_called_with(
			SOME_DOMAIN_NAME,
			FIRST_NODE_NAME
		)
		commands = self.management_res.extra_properties.commands
		commands.create_node_ssh.assert_called_once_with(
			id=FIRST_NODE_NAME,
			nodedir=SOME_NODE_DIR,
			nodehost=SOME_NODE_ALLOCATOR_HOST,
			install=False
		)
		self.assertEqual(some_node.name, FIRST_NODE_NAME)
		
	def test_clusters(self):
	
		child_res = self.management_res.extra_properties.child_resources
		child_res.keys.return_value = [
			FIRST_CLUSTER_NAME,
			SECOND_CLUSTER_NAME,
			THIRD_CLUSTER_NAME
		]
		
		clust_list = list(self.managed_domain.clusters())
		
		self.assertListEqual(clust_list, THREE_CLUSTER_LIST)
		
	def test_create_cluster(self):
	
		child_res = self.management_res.extra_properties.child_resources
		child_res.keys.return_value = [
			FIRST_CLUSTER_NAME
		]
		
		some_clust = self.managed_domain.create_cluster(FIRST_CLUSTER_NAME)
		
		self.assertEqual(some_clust.name, FIRST_CLUSTER_NAME)
		
class ManagedDomainContextTestCase(unittest.TestCase):

	def setUp(self):

		engine_patcher = patch(
			"caviar.engine.Engine"
		)
		Engine = engine_patcher.start()
		self.addCleanup(engine_patcher.stop)
		
		node_allocator_patcher = patch(
			"caviar.engine.nodealloc.NodeAllocator"
		)
		NodeAllocator = node_allocator_patcher.start()
		self.addCleanup(node_allocator_patcher.stop)
		
		self.engine = Engine()
		
		self.node_allocator = NodeAllocator()
		self.engine.node_allocator.return_value = self.node_allocator
		
		self.context = caviar.domain.ManagedDomainContext(
			self.engine,
			SOME_DOMAIN_NAME,
			SOME_ADMIN_PORT,
			SOME_ADMIN_USER,
			SOME_ADMIN_PASSWORD
		)
		
	def test_management(self):
	
		management = self.context.management()
		
		self.engine.management.assert_called_once_with(
			SOME_DOMAIN_NAME,
			SOME_ADMIN_PORT,
			SOME_ADMIN_USER,
			SOME_ADMIN_PASSWORD
		)
		
	def test_prepare_node(self):
	
		self.node_allocator.prepare.return_value = SOME_NODE_ALLOCATOR_HOST
		
		host = self.context.prepare_node(
			ANY_NODE_ALLOCATOR_NAME,
			FIRST_NODE_NAME
		)
		
		self.assertEqual(host, SOME_NODE_ALLOCATOR_HOST)
		
class EnvironmentTestCase(unittest.TestCase):

	def setUp(self):
	
		engine_patcher = patch(
			"caviar.engine.Engine"
		)
		Engine = engine_patcher.start()
		self.addCleanup(engine_patcher.stop)
		
		asadmin_patcher = patch(
			"caviar.engine.asadmin.Asadmin"
		)
		Asadmin = asadmin_patcher.start()
		self.addCleanup(asadmin_patcher.stop)
		
		self.engine = Engine()
		self.asadmin = Asadmin()
		self.engine.asadmin.return_value = self.asadmin
		
		self.environment = caviar.domain.Environment(self.engine)
		
	def test_domains(self):
	
		self.asadmin.list_domains.return_value = SOME_DOMAIN_DATA_LIST
		
		domain_list = list(self.environment.domains())
		
		self.assertListEqual(domain_list, SOME_DOMAIN_LIST)
		
	def test_create_domain(self):
	
		self.asadmin.list_domains.return_value = SOME_DOMAIN_DATA_LIST
		
		created_domain = self.environment.create_domain(
			SOME_DOMAIN_NAME,
			SOME_ADMIN_USER,
			SOME_ADMIN_PASSWORD,
			SOME_CERTIFICATE
		)
		
		self.assertEqual(created_domain.name, SOME_DOMAIN_NAME)
		self.asadmin.create_domain.assert_called_once_with(
			SOME_DOMAIN_NAME,
			SOME_ADMIN_USER,
			SOME_ADMIN_PASSWORD
		)
		self.asadmin.start_domain.assert_called_once_with(
			SOME_DOMAIN_NAME
		)
		self.asadmin.enable_secure_admin.assert_called_once_with(
			ANY,
			ANY,
			ANY
		)
		self.asadmin.set_admin_listener_host.assert_called_once_with(
			ANY,
			ANY,
			ANY
		)
		self.asadmin.stop_domain.assert_called_once_with(
			SOME_DOMAIN_NAME
		)
		
	def test_close(self):
	
		self.environment.close()
		
		self.engine.close.assert_called_once_with()

