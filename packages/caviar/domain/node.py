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
Node module.
"""

import caviar
import caviar.domain
import caviar.domain.instance

class Node:

	"""
	Node.

	:param caviar.domain.ManagedDomainContext context:
	   Managed domain context.
	:param str name:
	   Node name.
	"""

	def __init__(self, context, name):

		self.__context = context
		self.__name = name
		
	def __hash__(self):
	
		return hash(self.__name)
		
	def __eq__(self, other):

		return self.__name == other.__name
		
	def __str__(self):
	
		return self.__name
		
	def __management(self):

		return self.__context.management()
		
	@property
	def name(self):
	
		"""
		Node name.
		
		:rtype:
		   str
		"""
		
		return self.__name
		
	# TODO Test coverage...
	def instances(self):

		"""
		Node instances.

		:rtype:
		   iter
		:return:
		   Iterator that yields node instances.
		"""
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["servers"]
		res = res.extra_properties.child_resources["server"]
		for name, inst_res in res.extra_properties.child_resources.items():
			if inst_res.extra_properties.entity.nodeRef == self.__name:
				yield caviar.domain.instance.Instance(
					self.__context,
					name,
					self
				)
				
	# TODO Test coverage...
	def create_instance(self, name, cluster):
	
		"""
		Create a new node instance for participating in the given cluster.
		
		:param str name:
		   Instance name.
		:param caviar.domain.cluster.Cluster cluster:
		   Cluster where participate in.
		   
		:rtype:
		   caviar.domain.instance.Instance
		:return:
		   The created instance.
		"""
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["nodes"]
		res = res.extra_properties.child_resources["node"]
		res = res.extra_properties.child_resources[self.__name]
		res = res.raise_not_success()
		node_host = res.extra_properties.entity.nodeHost
		
		res = self.__management().domain()
		res.extra_properties.commands.create_instance(
			id=name,
			nodeagent=self.__name,
			cluster=cluster.name
		)
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["servers"]
		res = res.extra_properties.child_resources["server"]
		res.extra_properties.child_resources.cache_evict()
		created_instance = next(
			filter(
				lambda inst: inst.name == name,
				self.instances()
			),
			None
		)
		
		res = res.extra_properties.child_resources[name]
		inst_res = res.raise_not_success()
		config_ref = inst_res.extra_properties.entity.configRef
		
		extra_props = inst_res.extra_properties
		sys_props_res = extra_props.child_resources["system-properties"]
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["configs"]
		res = res.extra_properties.child_resources["config"]
		res = res.extra_properties.child_resources[config_ref]
		res = res.raise_not_success()
		res = res.extra_properties.child_resources["network-config"]
		res = res.extra_properties.child_resources["network-listeners"]
		nl_res = res.extra_properties.child_resources["network-listener"]
		
		res = nl_res.extra_properties.child_resources["http-listener-1"]
		http_listener_1_res = res.raise_not_success()
		res = nl_res.extra_properties.child_resources["http-listener-2"]
		http_listener_2_res = res.raise_not_success()
		
		extra_props = sys_props_res.extra_properties
		http_listener_1_port = extra_props.system_properties.resolve(
			http_listener_1_res.extra_properties.entity.port
		)
		http_listener_2_port = extra_props.system_properties.resolve(
			http_listener_2_res.extra_properties.entity.port
		)
		
		self.__context.add_instance(
			cluster.name,
			created_instance.name,
			node_host,
			http_listener_1_port
		)
		return created_instance

