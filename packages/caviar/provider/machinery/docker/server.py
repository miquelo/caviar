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

DOMAIN_DIR = "/var/glassfish/domains"
NODE_DIR = "/var/glassfish/nodes"

class ServerMachine(machine.Machine):

	def __init__(self, client, container_id, appserver_user, web_user,
			appserver_public_key_path):
	
		super().__init__(client, container_id)
		
		self.__appserver_user = appserver_user
		self.__web_user = web_user
		self.__appserver_public_key_path = appserver_public_key_path
		
	def __keystore_setup_file_path(self, domain_name, file_name):
	
		return "/tmp/keystore-{}/{}".format(domain_name, file_name)
		
	@property
	def appserver_user(self):
	
		return self.__appserver_user
		
	@property
	def appserver_public_key_path(self):
	
		return self.__appserver_public_key_path
		
	def password_file_path(self, pwd_id):
	
		return "/tmp/passwords-{}.txt".format(pwd_id)
		
	def asadmin_cmd(self, asadmin_args):
	
		args = []
		args.append("$HOME/bin/asadmin")
		args.extend(asadmin_args)
		return " ".join(args)
		
	def create_password_file_cmd(self, pwd_id, passwords):
	
		return "echo '{}' >> {}".format(
			"\n".join([
				"{}={}".format(key, value) for key, value in passwords.items()
			]),
			self.password_file_path(pwd_id)
		)
		
	def delete_password_file_cmd(self, pwd_id):
	
		return "rm {}".format(self.password_file_path(pwd_id))
		
	def install_master_password_cmd(self, domain_name, node_name, node_host):
	
		return " ".join([
			"$HOME/bin/install-master-password.sh",
			self.appserver_user,
			node_host,
			NODE_DIR,
			node_name,
			DOMAIN_DIR,
			domain_name
		])
		
	def install_certificates_cmd(self, domain_name, master_password, lb_host):
	
		return " ".join([
			"$HOME/bin/install-certificates.sh",
			DOMAIN_DIR,
			domain_name,
			master_password,
			self.__web_user,
			lb_host
		])
		
	def keystore_setup_begin_cmd(self, domain_name):
	
		return " ".join([
			"$HOME/bin/keystore-setup-begin.sh",
			domain_name
		])
		
	def keystore_setup_end_cmd(self, domain_name, master_password):
	
		return " ".join([
			"$HOME/bin/keystore-setup-end.sh",
			domain_name,
			master_password
		])
		
	def keystore_setup_subject_path(self, domain_name):
	
		return self.__keystore_setup_file_path(domain_name, "subject")
		
	def keystore_setup_issuer_path(self, domain_name):
	
		return self.__keystore_setup_file_path(domain_name, "issuer")
		
	def keystore_setup_private_key_path(self, domain_name):
	
		return self.__keystore_setup_file_path(domain_name, "private-key")

