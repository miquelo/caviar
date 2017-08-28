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
import caviar.domain.cluster

SOME_CLUSTER_NAME = "cluster-01"

class ClusterTestCase(unittest.TestCase):

	def setUp(self):
	
		self.cluster = caviar.domain.cluster.Cluster(
			None,
			SOME_CLUSTER_NAME
		)
		
	def test_name(self):
	
		cluster_name = self.cluster.name
		
		self.assertEqual(cluster_name, SOME_CLUSTER_NAME)

