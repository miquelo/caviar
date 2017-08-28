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
import caviar.engine.management

from unittest.mock import patch

ANY_MACHINE_HOST = "host"
ANY_ADMIN_PORT = "4848"
ANY_HTTP_AUTH = caviar.network.http.HTTPBasicAuth(
	"admin",
	"12345678"
)

HTTP_ACCEPTED_STATUS = 200

DOMAIN_RESPONSE_CONTENT = {
	"command": "command",
	"exit_code": "SUCCESS"
}

class ManagementTestCase(unittest.TestCase):

	def setUp(self):
	
		machine_patcher = patch(
			"testsuite.unit.caviar.provider.machinery.fake.server.ServerMachine"
		)
		ServerMachine = machine_patcher.start()
		self.addCleanup(machine_patcher.stop)
		
		network_module_patcher = patch(
			"caviar.network"
		)
		NetworkModule = network_module_patcher.start()
		self.addCleanup(network_module_patcher.stop)
		
		http_resource_patcher = patch(
			"caviar.network.http.HTTPResource"
		)
		HTTPResource = http_resource_patcher.start()
		self.addCleanup(http_resource_patcher.stop)
		
		http_request_patcher = patch(
			"caviar.network.http.HTTPRequest"
		)
		HTTPRequest = http_request_patcher.start()
		self.addCleanup(http_request_patcher.stop)
		
		http_response_patcher = patch(
			"caviar.network.http.HTTPResponse"
		)
		HTTPResponse = http_response_patcher.start()
		self.addCleanup(http_response_patcher.stop)
		
		any_das_machine = ServerMachine()
		any_das_machine.host = ANY_MACHINE_HOST
		
		self.http_response = HTTPResponse()
		
		http_request = HTTPRequest()
		http_request.perform.return_value = self.http_response
		
		http_resource = HTTPResource()
		http_resource.request.return_value = http_request
		http_resource.push.return_value = http_resource
		
		network = NetworkModule()
		network.http_resource.return_value = http_resource
		
		self.management = caviar.engine.management.Management(
			any_das_machine,
			ANY_ADMIN_PORT,
			ANY_HTTP_AUTH,
			network
		)
		
		# XXX Code snippet...
		# http_res_method_patcher = patch.object(self.management, "resource")
		# http_res_method = http_res_method_patcher.start()
		# self.addCleanup(http_res_method_patcher.stop)
		
	def test_domain(self):
	
		self.http_response.status_code = HTTP_ACCEPTED_STATUS
		self.http_response.content = DOMAIN_RESPONSE_CONTENT
		
		domain = self.management.domain()
	
		self.assertIsInstance(
			domain,
			caviar.engine.management.ManagementResource
		)

