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

import caviar
import caviar.network

import unittest

ANY_PROTOCOL = "proto"
ANY_HOST = "host"
ANY_PORT = "1000"
ANY_AUTH = None
ANY_HEADERS = {}

class TestCase(unittest.TestCase):

	def test_http_resource(self):
	
		resource = caviar.network.http_resource(
			ANY_PROTOCOL,
			ANY_HOST,
			ANY_PORT,
			ANY_AUTH,
			ANY_HEADERS
		)
		
		self.assertIsInstance(resource, caviar.network.http.HTTPResource)

