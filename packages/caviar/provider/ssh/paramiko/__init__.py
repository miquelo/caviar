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

import paramiko

import caviar

class SSHClient:

	def __init__(self):
	
		pass
		
	def login(self, target, private_key_path):
	
		try:
			paramiko_client = paramiko.SSHClient()
			paramiko_client.set_missing_host_key_policy(
				paramiko.AutoAddPolicy()
			)
			paramiko_client.connect(
				hostname=target.host,
				username=target.user,
				allow_agent=False,
				look_for_keys=False,
				key_filename=private_key_path
			)
			return SSHPhysicalSession(
				paramiko_client
			)
		except:
			paramiko_client.close()
			raise caviar.network.ssh.SSHUnavailableSessionError(target)
			
	def close(self):
	
		pass
		
class SSHPhysicalSession:

	def __init__(self, paramiko_client):
	
		self.__paramiko_client = paramiko_client
		self.__paramiko_file_client = None
		
	def __close(self):
	
		self.__paramiko_client.close()
		if self.__paramiko_file_client is not None:
			self.__paramiko_file_client.close()
			
	def execute(self, cmd):
	
		try:
			stdin, stdout, stderr = self.__paramiko_client.exec_command(cmd)
			return stdout, stderr
		except Exception as e:
			self.__close()
			raise SSHInvalidSessionError(e)
			
	# TODO Test coverage...
	def copy(self, source_path, target_path):
	
		try:
			if self.__paramiko_file_client is None:
				self.__paramiko_file_client = self.__paramiko_client.open_sftp()
			with self.__paramiko_file_client.open(target_path, mode="w") as tf:
				with open(source_path, mode="r") as sf:
					tf.write(sf.read())
		except IOError as e:
			raise e
		except Exception as e:
			self.__close()
			raise SSHInvalidSessionError(e)
			
	def logout(self):
	
		self.__paramiko_client.exec_command("exit")
		self.__close()

