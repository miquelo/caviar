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

"""
Instance module.
"""

class Instance:

	"""
	Instance.

	:param caviar.domain.ManagedDomainContext context:
	   Managed domain context.
	:param str name:
	   Instance name.
	:param caviar.domain.node.Node node:
	   Node where instance resides.
	"""

	def __init__(self, context, name, node):

		self.__context = context
		self.__name = name
		self.__node = node
		
	def __eq__(self, other):

		return self.__name == other.__name
		
	@property
	def name(self):
	
		"""
		Instance name.
		
		:rtype:
		   str
		"""
		
		return self.__name

