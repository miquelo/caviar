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
Domain module.
"""

import caviar.domain.cluster
import caviar.domain.node
import caviar.engine
import caviar.network

import importlib
import random
import string
import sys

class Domain:

	"""
	Domain.

	:param caviar.engine.Engine engine:
	   Underlying engine.
	"""

	def __init__(self, engine, name, admin_host, admin_port, running,
			restart_required):

		self.__engine = engine
		self.__name = name
		self.__admin_host = admin_host
		self.__admin_port = admin_port
		self.__running = running
		self.__restart_required = restart_required

	def __eq__(self, other):

		return self.__name == other.__name

	def __asadmin(self):

		return self.__engine.asadmin()

	@property
	def name(self):
	
		"""
		Domain name.
		
		:rtype:
		   str
		"""
		
		return self.__name
		
	def manage(self, admin_user, admin_password):

		"""
		Manage this domain.

		Ensure it is running and without requiring to be restarted, and update
		its state.

		:param str admin_user:
			Name of the administrator user.
		:param str admin_password:
			Password of the administrator user.

		:rtype:
			ManagedDomain
		:return:
			The managed domain.
		"""

		asadmin = self.__asadmin()
		if not self.__running:
			asadmin.start_domain(self.__name)
		elif self.__restart_required:
			asadmin.restart_domain(self.__name)
		self.__running = True
		self.__restart_required = False
		
		return ManagedDomain(ManagedDomainContext(
			self.__engine,
			self.__name,
			self.__admin_port,
			admin_user,
			admin_password
		))

class ManagedDomain:

	"""
	Managed domain.

	:param ManagedDomainContext context:
	   Managed domain context.
	"""

	def __init__(self, context):
	
		self.__context = context
		
	def __management(self):

		return self.__context.management()
		
	def __prepare_node(self, allocator_name, name):

		return self.__context.prepare_node(allocator_name, name)
		
	def __prepare_cluster(self, name):

		return self.__context.prepare_cluster(name)
		
	def nodes(self):

		"""
		Available nodes.

		:rtype:
		   iter
		:return:
		   Iterator that yields available nodes.
		"""
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["nodes"]
		res = res.extra_properties.child_resources["node"]
		for name, node_res in res.extra_properties.child_resources.items():
			if node_res.extra_properties.entity.type == "SSH":
				yield caviar.domain.node.Node(
					self.__context,
					name
				)
				
	def create_node(self, name, allocator_name):

		"""
		Create a node on this domain.

		:param str name:
		   Node name.
		:param str allocator_name:
			Node allocator name.

		:rtype:
		   node.Node
		:return:
		   The created node.
		"""
		
		host = self.__prepare_node(allocator_name, name)
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["nodes"]
		res.extra_properties.commands.create_node_ssh(
			id=name,
			install=False,
			nodedir=self.__context.node_dir,
			nodehost=host
		)
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["nodes"]
		res = res.extra_properties.child_resources["node"]
		res.extra_properties.child_resources.cache_evict()
		return next(
			filter(
				lambda node: node.name == name,
				self.nodes()
			),
			None
		)
		
	def clusters(self):

		"""
		Available clusters.

		:rtype:
		   iter
		:return:
		   Iterator that yields available clusters.
		"""
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["clusters"]
		res = res.extra_properties.child_resources["cluster"]
		for name in res.extra_properties.child_resources.keys():
			yield caviar.domain.cluster.Cluster(
				self.__context,
				name
			)
			
	def create_cluster(self, name, cacerts=None, certkey=None,
			keystore_inst_alias=None):
		
		"""
		Create a cluster.
		
		:param str name:
		   Cluster name.
		:param iter cacerts:
		   Iterator of CA :class:`Certificate` entries.
		:param CertificateKey certkey:
		   Certificate and private key used for SSL, if any.
		:param str keystore_inst_alias:
		   Alias of entry used by instance listener. `None` if it is
		   using the default certificate and key.
		"""
		
		self.__prepare_cluster(name)
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["clusters"]
		res = res.extra_properties.child_resources["cluster"]
		res = res.extra_properties.methods.post(
			id=name
		)
		res.extra_properties.child_resources.cache_evict()
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["clusters"]
		res = res.extra_properties.child_resources["cluster"]
		res = res.extra_properties.child_resources[name]
		config_ref = res.extra_properties.entity.configRef
		
		res = self.__management().domain()
		res = res.extra_properties.child_resources["configs"]
		res = res.extra_properties.child_resources["config"]
		res = res.extra_properties.child_resources[config_ref]
		res.raise_not_success()
		res = res.extra_properties.child_resources["network-config"]
		nl_res = res.extra_properties.child_resources["network-listeners"]
		
		res = nl_res.extra_properties.child_resources["network-listener"]
		hl1_res = res.extra_properties.child_resources["http-listener-1"]
		res = hl1_res.extra_properties.commands.create_ssl(
			certNickname=self.__context.http_protocol_keystore_alias,
			target=name
		)
		res.raise_not_success()
		
		res = hl1_res.extra_properties.methods.post(
			address=hl1_res.extra_properties.entity.address,
			jkEnabled=True,
			name=hl1_res.extra_properties.entity.name,
			port=hl1_res.extra_properties.entity.port,
			protocol=hl1_res.extra_properties.entity.protocol,
			transport=hl1_res.extra_properties.entity.transport
		)
		res.raise_not_success()
		
		# TODO Do something with http-listener-2
		
		return next(
			filter(
				lambda clust: clust.name == name,
				self.clusters()
			),
			None
		)
		
class ManagedDomainContext:

	"""
	Managed domain context.
	
	:param caviar.engine.Engine engine:
	   Underlying engine.
	:param str domain_name:
	   Domain name.
	:param str admin_port:
	   Administrator port.
	:param str admin_user:
	   Administrator user name.
	:param str admin_password:
	   Administrator password.
	"""
	
	def __init__(self, engine, domain_name, admin_port, admin_user,
			admin_password):
			
		self.__engine = engine
		self.__domain_name = domain_name
		self.__admin_port = admin_port
		self.__admin_user = admin_user
		self.__admin_password = admin_password
		
	def __node_allocator(self, name):
	
		return self.__engine.node_allocator(name)
		
	def __load_balancer(self, cluster_name):
	
		return self.__engine.load_balancer(cluster_name)
		
	@property
	def node_dir(self):
	
		"""
		Node directory.
		
		:rtype:
		   str
		"""
		
		return self.__engine.server_node_dir
		
	@property
	def http_protocol_keystore_alias(self):
	
		"""
		HTTP protocol keystore alias.
		
		:rtype:
		   str
		"""
		
		return self.__engine.http_protocol_keystore_alias
		
	def management(self):
	
		"""
		Domain management for this context.
		
		:rtype:
		   caviar.engine.management.Management
		:return:
		   Domain management.
		"""
		
		return self.__engine.management(
			self.__domain_name,
			self.__admin_port,
			self.__admin_user,
			self.__admin_password
		)
		
	def prepare_node(self, allocator_name, name):
		
		"""
		Prepare an allocated node.
		
		:param str allocator_name:
		   Node allocator name.
		:param str name:
		   Node name.
		   
		:rtype:
		   str
		:return:
		   Node allocator host.
		"""
		
		return self.__node_allocator(allocator_name).prepare(
			self.__domain_name,
			name
		)
		
	def prepare_cluster(self, name):
		
		"""
		Prepare a cluster load balancer.
		
		:param str name:
		   Cluster name.
		"""
		
		self.__load_balancer(name).prepare(
			self.__domain_name
		)
		
	def add_instance(self, cluster_name, name, host, port):
	
		self.__engine.load_balancer(cluster_name).add_instance(
			name,
			host,
			port
		)
		
	def remove_instance(self, cluster_name, name):
	
		self.__engine.load_balancer(cluster_name).remove_instance(name)
		
class Environment:

	"""
	GlassFish environment.

	:param caviar.engine.Engine engine:
	   GlassFish engine.
	"""

	def __init__(self, engine):

		self.__engine = engine
		
	@property
	def __keystore_admin_alias(self):
	
		return self.__engine.__keystore_admin_alias
		
	@property
	def __keystore_inst_alias(self):
	
		return self.__engine.__keystore_inst_alias
		
	def __asadmin(self):

		return self.__engine.asadmin()
		
	def __keytool(self):
	
		return self.__engine.keytool()
		
	def domains(self):

		"""
		Available domains.

		:rtype:
		   iter
		:return:
		   Iterator that yields available domains.
		"""

		for data in self.__asadmin().list_domains():
			yield Domain(
				self.__engine,
				data["name"],
				data["admin-host"],
				data["admin-port"],
				data["running"],
				data["restart-required"]
			)
			
	def create_domain(self, name, admin_user, admin_password,
			cacerts_entries=None, keystore_entries=None,
			keystore_admin_alias=None):
	
		"""
		Create a domain.
		
		:param str name:
		   Domain name.
		:param str admin_user:
		   Administrator user name.
		:param str admin_password:
		   Administrator user password.
		:param dict cacerts_entries:
		   Dictionary of alias and :class:`Certificate` entries for CA
		   certificates.
		:param dict keystore_entries:
		   Dictionary of alias and :class:`CertificateKey` entries for
		   keystore.
		:param str keystore_admin_alias:
		   Alias of entry used by administrator listener. `None` if it is
		   using the default certificate and key.
		   
		:rtype:
		   Domain
		:return:
		   The created domain.
		"""
		
		self.__asadmin().create_domain(
			name,
			admin_user,
			admin_password
		)
		domain_data = next(
			filter(
				lambda data: data["name"] == name,
				self.__asadmin().list_domains()
			),
			None
		)
		
		self.__asadmin().start_domain(
			domain_data["name"]
		)
		
		self.__asadmin().enable_secure_admin(
			domain_data["admin-port"],
			admin_user,
			admin_password
		)
		self.__asadmin().set_admin_listener_host(
			domain_data["admin-port"],
			admin_user,
			admin_password
		)
		
		if cacerts is not None:
			for certificate in cacerts:
				self.__keytool().cacerts(domain_data["name"]).put(
					alias="caviar-{}".format("".join(
						random.choice(string.ascii_lowercase + string.digits)
						for _ in range(8)
					)),
					certificate=certificate
				)
		if admin_certkey is None:
			self.__keytool().keystore(domain_data["name"]).self_signed(
				alias="caviar-admin",
				subject={
					"CN": "admin.{}".format(domain_data["name"])
				}
			)
		elif:
			self.__keytool().keystore(domain_data["name"]).put(
				alias="caviar-admin",
				certificate=admin_certkey.certificate,
				key=admin_certkey.key
			)
		if inst_certkey is None:
			self.__keytool().keystore(domain_data["name"]).self_signed(
				alias="caviar-inst",
				subject={
					"CN": "inst.{}".format(domain_data["name"])
				}
			)
		elif:
			self.__keytool().keystore(domain_data["name"]).put(
				alias="caviar-inst",
				certificate=inst_certkey.certificate,
				key=inst_certkey.key
			)
			
		self.__asadmin().restart_domain(
			domain_data["name"]
		)
		
		# TODO Domain cleanup through management
		# - Remove http-listener-1 on server-config
		# - Remove http-listener-2 on server-config
		
		# TODO Create SSL for admin-listener with "caviar-admin" alias
		
		self.__asadmin().stop_domain(
			domain_data["name"]
		)
		
		return next(
			filter(
				lambda domain: domain.name == name,
				self.domains()
			),
			None
		)
		
	def close(self):
	
		"""
		Close this environment.
		
		Shutdown the engine.
		"""
		
		self.__engine.close()
		
def environment(
	machinery_module_name,
	machinery_params,
	mgmt_public_key_path,
	mgmt_private_key_path,
	master_password,
	log_out=sys.stdout,
	ssh_module_name="caviar.provider.ssh.paramiko",
	das_server_name="das",
	node_alloc_server_prefix="nodealloc"
):

	"""
	Restore the specified environment.

	:param str machinery_module_name:
	   Machinery module name.
	:param dict machinery_params:
	   Machinery parameters.
	:param str mgmt_public_key_path:
	   Management public key path.
	:param str mgmt_private_key_path:
	   Management private key path.
	:param str master_password:
	   Used master password.
	:param fileobj log_out:
	   Logging output.

	:rtype:
	   Environment
	:return:
	   The restored environment.
	"""

	machinery_module = importlib.import_module(machinery_module_name)
	ssh_module = importlib.import_module(ssh_module_name)
	return Environment(caviar.engine.Engine(
		machinery_module.Machinery(
			machinery_params,
			mgmt_public_key_path,
			log_out
		),
		caviar.network.ssh_session_factory(
			ssh_module.SSHClient(),
			mgmt_private_key_path
		),
		master_password,
		das_server_name,
		node_alloc_server_prefix
	))
