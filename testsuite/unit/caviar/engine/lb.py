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
import caviar.engine.lb

from unittest.mock import patch

ANY_MASTER_PASSWORD = "12345678"

SOME_INSTANCE_NAME = "inst-01"
SOME_INSTANCE_HOST = "inst-01-host"
SOME_INSTANCE_PORT = "inst-01-port"

SOME_CMD = "command for load balancer"

class LoadBalancerTestCase(unittest.TestCase):

	def setUp(self):

		ssh_session_fact_patcher = patch(
			"caviar.network.ssh.SSHSessionFactory"
		)
		SSHSessionFactory = ssh_session_fact_patcher.start()
		self.addCleanup(ssh_session_fact_patcher.stop)
		
		ssh_session_patcher = patch(
			"caviar.network.ssh.SSHSession"
		)
		SSHSession = ssh_session_patcher.start()
		self.addCleanup(ssh_session_patcher.stop)
		
		server_machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.server.ServerMachine"
		)
		ServerMachine = server_machine_patcher.start()
		self.addCleanup(server_machine_patcher.stop)
		
		lb_machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.lb"
			".AJP13LoadBalancerMachine"
		)
		AJP13LoadBalancerMachine = lb_machine_patcher.start()
		self.addCleanup(lb_machine_patcher.stop)
		
		ssh_session_fact = SSHSessionFactory()
		
		self.ssh_session = SSHSession()
		ssh_session_fact.session.return_value = self.ssh_session
		
		self.das_machine = ServerMachine()
		self.lb_machine = AJP13LoadBalancerMachine()
		
		self.load_balancer = caviar.engine.lb.LoadBalancer(
			ssh_session_fact,
			self.das_machine,
			self.lb_machine,
			ANY_MASTER_PASSWORD
		)
		
	def test_add_instance(self):
	
		self.lb_machine.add_instance_cmd.return_value = SOME_CMD
		
		self.load_balancer.add_instance(
			SOME_INSTANCE_NAME,
			SOME_INSTANCE_HOST,
			SOME_INSTANCE_PORT
		)
		
		self.ssh_session.execute.assert_called_once_with(
			SOME_CMD
		)
		self.lb_machine.add_instance_cmd.assert_called_once_with(
			SOME_INSTANCE_NAME,
			SOME_INSTANCE_HOST,
			SOME_INSTANCE_PORT
		)
		
	def test_remove_instance(self):
	
		self.lb_machine.remove_instance_cmd.return_value = SOME_CMD
		
		self.load_balancer.remove_instance(
			SOME_INSTANCE_NAME
		)
		
		self.ssh_session.execute.assert_called_once_with(
			SOME_CMD
		)
		self.lb_machine.remove_instance_cmd.assert_called_once_with(
			SOME_INSTANCE_NAME
		)

