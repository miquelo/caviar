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
import caviar.engine.asadmin

from unittest.mock import ANY, call, patch

SOME_MASTER_PASSWORD = "12345678"

SOME_CMD = "some command"

SOME_DOMAIN_LIST_LINES = [
	"domain-01  das-host   4848  true  false",
	"domain-02  das-host  24848  true  true"
]

SOME_DOMAIN_LIST = [
	{
		"name": "domain-01",
		"admin-host": "das-host",
		"admin-port": "4848",
		"running": True,
		"restart-required": False
	},
	{
		"name": "domain-02",
		"admin-host": "das-host",
		"admin-port": "24848",
		"running": True,
		"restart-required": True
	}
]

ANY_DOMAIN_NAME = "domain"
ANY_ADMIN_PORT = "port"
ANY_ADMIN_USER = "user"
ANY_ADMIN_PASSWORD = "password"

class AsadminTestCase(unittest.TestCase):

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
		
		machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.server.ServerMachine"
		)
		ServerMachine = machine_patcher.start()
		self.addCleanup(machine_patcher.stop)
		
		ssh_session_fact = SSHSessionFactory()
		self.ssh_session = SSHSession()
		ssh_session_fact.session.return_value = self.ssh_session
		machine = ServerMachine()
		machine.asadmin_cmd.return_value = SOME_CMD
		self.asadmin = caviar.engine.asadmin.Asadmin(
			ssh_session_fact,
			machine,
			SOME_MASTER_PASSWORD
		)
		
	def test_list_domains(self):
	
		self.ssh_session.execute.side_effect = [
			SOME_DOMAIN_LIST_LINES
		]
		
		domain_list = list(self.asadmin.list_domains())
		
		self.assertListEqual(domain_list, SOME_DOMAIN_LIST)
		self.ssh_session.execute.assert_called_one_with(SOME_CMD)
		
	def test_create_domain(self):
	
		self.asadmin.create_domain(
			ANY_DOMAIN_NAME,
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		#	self.ssh_session.execute.assert_has_calls([
		#		call(ANY),
		#		call(ANY),
		#		call(ANY)
		#	])
		
	def test_enable_secure_admin(self):
	
		self.asadmin.enable_secure_admin(
			ANY_ADMIN_PORT,
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		#	self.ssh_session.execute.assert_has_calls([
		#		call(ANY),
		#		call(ANY),
		#		call(ANY)
		#	])
		
	def test_set_admin_listener_host(self):
	
		self.asadmin.set_admin_listener_host(
			ANY_ADMIN_PORT,
			ANY_ADMIN_USER,
			ANY_ADMIN_PASSWORD
		)
		
		#	self.ssh_session.execute.assert_has_calls([
		#		call(ANY),
		#		call(ANY),
		#		call(ANY)
		#	])
		
	def test_start_domain(self):
	
		self.asadmin.start_domain(
			ANY_DOMAIN_NAME
		)
		
		#	self.ssh_session.execute.assert_has_calls([
		#		call(ANY),
		#		call(ANY),
		#		call(ANY)
		#	])
		
	def test_stop_domain(self):
	
		self.asadmin.stop_domain(
			ANY_DOMAIN_NAME
		)
		
		#	self.ssh_session.execute.assert_has_calls([
		#		call(ANY),
		#		call(ANY),
		#		call(ANY)
		#	])

