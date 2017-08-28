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

from caviar.provider.machinery.docker import machine

# TODO Test coverage...
class AJP13LoadBalancerMachine(machine.Machine):

	def __init__(self, client, container_id, web_user):
	
		super().__init__(client, container_id)
		self.__web_user = web_user
		
		
	def __lb_cmd(self, *args):
	
		return ". ~/.bash_profile ; lb.sh {}".format(" ".join(args))
		
	# TODO Test coverage...
	@property
	def web_user(self):
	
		return self.__web_user
		
	# TODO Test coverage...
	def add_instance_cmd(self, name, host, port):
	
		return self.__lb_cmd("add", name, host, port)
		
	# TODO Test coverage...
	def remove_instance_cmd(self, name):
	
		return self.__lb_cmd("remove", name)

