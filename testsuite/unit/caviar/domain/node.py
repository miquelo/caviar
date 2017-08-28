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
import caviar.domain.node

from unittest.mock import patch

SOME_NODE_NAME = "node-01"

class NodeTestCase(unittest.TestCase):

	def setUp(self):
	
		managed_domain_context_patcher = patch(
			"caviar.domain.ManagedDomainContext"
		)
		ManagedDomainContext = managed_domain_context_patcher.start()
		self.addCleanup(managed_domain_context_patcher.stop)
		
		managed_domain_context = ManagedDomainContext()
		
		self.node = caviar.domain.node.Node(
			managed_domain_context,
			SOME_NODE_NAME
		)
		
	def test_name(self):
	
		node_name = self.node.name
		
		self.assertEqual(node_name, SOME_NODE_NAME)

