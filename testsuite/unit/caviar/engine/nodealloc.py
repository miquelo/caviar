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
import caviar.engine.nodealloc

from unittest.mock import call, patch

ANY_DOMAIN_NAME = "domain"
ANY_NODE_NAME = "node"

SOME_DAS_HOST = "das-host"
SOME_NODE_HOST = "node-01-host"

SOME_INSTALL_MASTER_PASSWORD_CMD = "install master password"
SOME_PING_CMD = "ping"

class NodeAllocatorTestCase(unittest.TestCase):

	def setUp(self):

		ssh_session_fact_patcher = patch(
			"caviar.network.ssh.SSHSessionFactory"
		)
		SSHSessionFactory = ssh_session_fact_patcher.start()
		self.addCleanup(ssh_session_fact_patcher.stop)
		
		das_ssh_session_patcher = patch(
			"caviar.network.ssh.SSHSession"
		)
		DASSSHSession = das_ssh_session_patcher.start()
		self.addCleanup(das_ssh_session_patcher.stop)
		
		node_alloc_ssh_session_patcher = patch(
			"caviar.network.ssh.SSHSession"
		)
		NodeAllocatorSSHSession = node_alloc_ssh_session_patcher.start()
		self.addCleanup(node_alloc_ssh_session_patcher.stop)
		
		das_machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.server.ServerMachine"
		)
		DASMachine = das_machine_patcher.start()
		self.addCleanup(das_machine_patcher.stop)
		
		node_alloc_machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.server.ServerMachine"
		)
		NodeAllocatorMachine = node_alloc_machine_patcher.start()
		self.addCleanup(node_alloc_machine_patcher.stop)
		
		self.das_machine = DASMachine()
		self.das_machine.host = SOME_DAS_HOST
		self.das_machine.install_master_password_cmd.side_effect = [
			SOME_INSTALL_MASTER_PASSWORD_CMD
		]
		
		self.node_alloc_machine = NodeAllocatorMachine()
		self.node_alloc_machine.host = SOME_NODE_HOST
		self.node_alloc_machine.ping_cmd.side_effect = [
			SOME_PING_CMD
		]
		
		self.das_ssh_session = DASSSHSession()
		self.node_alloc_ssh_session = NodeAllocatorSSHSession()
		
		ssh_session_fact = SSHSessionFactory()
		
		def ssh_session_fact_session(user, host):
		
			if host == SOME_DAS_HOST:
				return self.das_ssh_session
			if host == SOME_NODE_HOST:
				return self.node_alloc_ssh_session
			return None
			
		ssh_session_fact.session.side_effect = ssh_session_fact_session
		
		self.node_allocator = caviar.engine.nodealloc.NodeAllocator(
			ssh_session_fact,
			self.das_machine,
			self.node_alloc_machine
		)
		
	def test_prepare(self):
	
		node_host = self.node_allocator.prepare(
			ANY_DOMAIN_NAME,
			ANY_NODE_NAME
		)
	
		self.assertEqual(node_host, SOME_NODE_HOST)
		self.node_alloc_ssh_session.execute.assert_called_once_with(
			SOME_PING_CMD
		)
		self.das_ssh_session.execute.assert_called_once_with(
			SOME_INSTALL_MASTER_PASSWORD_CMD
		)

