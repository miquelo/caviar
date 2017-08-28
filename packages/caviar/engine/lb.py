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
Load balancer module.
"""

class LoadBalancer:

	"""
	Load balancer.
	"""

	def __init__(self, ssh_session_fact, das_machine, lb_machine,
			master_password):

		self.__das_ssh_session = ssh_session_fact.session(
			das_machine.appserver_user,
			das_machine.host
		)
		self.__lb_ssh_session = ssh_session_fact.session(
			lb_machine.web_user,
			lb_machine.host
		)
		self.__das_machine = das_machine
		self.__lb_machine = lb_machine
		self.__master_password = master_password
		
	# TODO Test coverage...
	@property
	def host(self):
	
		return self.__lb_machine.host
		
	# TODO Test coverage...
	def prepare(self, domain_name):
	
		any(self.__lb_ssh_session.execute(
			self.__lb_machine.ping_cmd()
		))
		any(self.__das_ssh_session.execute(
			self.__das_machine.install_certificates_cmd(
				domain_name,
				self.__master_password,
				self.__lb_machine.host
			)
		))
		
	def add_instance(self, name, host, port):

		"""
		Add an instance with the given name, host and port to the load balancer.

		:param str name:
		   Instance name.
		:param str host:
		   Instance host.
		:param str port:
		   Instance port.
		"""

		any(self.__lb_ssh_session.execute(
			self.__lb_machine.add_instance_cmd(name, host, port)
		))
		
	def remove_instance(self, name):

		"""
		Remove the instance with the given name from the load balancer.
		
		:param str name:
		   Instance name.
		"""

		any(self.__lb_ssh_session.execute(
			self.__lb_machine.remove_instance_cmd(name)
		))

