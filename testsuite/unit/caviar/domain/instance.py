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
import caviar.domain.instance

SOME_INSTANCE_NAME = "inst-01"

SOME_NODE = caviar.domain.node.Node(
	None,
	"node-01"
)

class InstanceTestCase(unittest.TestCase):

	def setUp(self):
	
		self.instance = caviar.domain.instance.Instance(
			None,
			SOME_INSTANCE_NAME,
			SOME_NODE
		)
		
	def test_name(self):
	
		inst_name = self.instance.name
		
		self.assertEqual(inst_name, SOME_INSTANCE_NAME)

