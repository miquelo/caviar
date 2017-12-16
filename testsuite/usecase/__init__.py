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

import docker
import io
import os
# TODO Remove...
# import requests
import subprocess
import unittest

import caviar
# import caviar.certificates
import caviar.domain
import caviar.domain.node

DEFAULT_DOCKER_BASE_URL = "unix:///var/run/docker.sock"

DOCKER_MACHINERY_BASE_NAME = "caviar-test"

PUBLIC_DOMAIN_NAME = "caviar.test"

DOMAIN_NAME = "test-domain"

ADMIN_USER = "admin"
ADMIN_PASSWORD = "12345678"

NODE01_NAME = "node-01"
NODE02_NAME = "node-02"
NODE03_NAME = "node-03"

ALLOC01_NAME = "alloc-01"
ALLOC02_NAME = "alloc-02"
ALLOC03_NAME = "alloc-03"

CLUSTER_NAME = "cluster-01"

INST01_NAME = "inst-01"
INST02_NAME = "inst-02"
INST03_NAME = "inst-03"

NODE_SET = set([
	caviar.domain.node.Node(
		None,
		NODE01_NAME
	),
	caviar.domain.node.Node(
		None,
		NODE02_NAME
	),
	caviar.domain.node.Node(
		None,
		NODE03_NAME
	)
])

# TODO Remove...
# HTTP_STATUS_OK = 200

class TestCase(unittest.TestCase):

	def setUp(self):

		self.docker_client = self.restore_docker_client()
		
		self.environment = caviar.domain.environment(
			machinery_module_name="caviar.provider.machinery.docker",
			machinery_params={
				"client": self.docker_client,
				"build-images": True,
				"base-name": DOCKER_MACHINERY_BASE_NAME
			},
			mgmt_public_key_path=os.path.expanduser(
				"~/.ssh/id_rsa_caviar_test.pub"),
			mgmt_private_key_path=os.path.expanduser(
				"~/.ssh/id_rsa_caviar_test"),
			master_password="12345678",
			log_out=io.StringIO()
		)
		
		for cont in self.docker_client.containers({
			"name": "{}*".format(DOCKER_MACHINERY_BASE_NAME)
		}):
			self.docker_client.remove_container(
				container=cont["Id"],
				v=True,
				force=True
			)
			
		self.domain_cacerts, \
		self.domain_admin_certkey, \
		self.domain_inst_certkey, \
		self.cluster_certkey = self.restore_certificates()
		
	def tearDown(self):

		self.environment.close()
		self.docker_client.close()

	def test_common_cluster(self):

		test_domain = next(
			filter(
				lambda domain: domain.name == DOMAIN_NAME,
				self.environment.domains()
			),
			None
		)
		self.assertIsNone(test_domain)
		
		test_domain = self.environment.create_domain(
			name=DOMAIN_NAME,
			admin_user=ADMIN_USER,
			admin_password=ADMIN_PASSWORD,
			cacerts=self.domain_cacerts,
			admin_certkey=self.domain_admin_certkey,
			inst_certkey=self.domain_inst_certkey
		)
		self.assertEqual(test_domain.name, DOMAIN_NAME)

		managed_domain = test_domain.manage(
			ADMIN_USER,
			ADMIN_PASSWORD
		)
		self.assertIsInstance(managed_domain, caviar.domain.ManagedDomain)

		node01 = managed_domain.create_node(NODE01_NAME, ALLOC01_NAME)
		self.assertEqual(node01.name, NODE01_NAME)
		
		node02 = managed_domain.create_node(NODE02_NAME, ALLOC02_NAME)
		self.assertEqual(node02.name, NODE02_NAME)
		
		node03 = managed_domain.create_node(NODE03_NAME, ALLOC03_NAME)
		self.assertEqual(node03.name, NODE03_NAME)
		
		node_set = set(managed_domain.nodes())
		self.assertSetEqual(node_set, NODE_SET)
		
		clust = managed_domain.create_cluster(
			name=CLUSTER_NAME,
			certkey=self.cluster_certkey
		)
		self.assertEqual(clust.name, CLUSTER_NAME)
		
		inst01 = node01.create_instance(INST01_NAME, clust)
		self.assertEqual(inst01.name, INST01_NAME)
		
		inst02 = node02.create_instance(INST02_NAME, clust)
		self.assertEqual(inst02.name, INST02_NAME)
		
		inst03 = node03.create_instance(INST03_NAME, clust)
		self.assertEqual(inst03.name, INST03_NAME)
		
		clust.start()
		
		# TODO Remove...
		# resp = requests.get("http://{}/".format(clust.load_balancer_host))
		# self.assertEqual(resp.status_code, HTTP_STATUS_OK)
		
	def restore_docker_client(self):
	
		return docker.APIClient(
			base_url=os.environ["DOCKER_HOST"] \
				if "DOCKER_HOST" in os.environ \
				else DEFAULT_DOCKER_BASE_URL,
			tls=docker.tls.TLSConfig(
				client_cert=(
					os.path.join(os.environ["DOCKER_CERT_PATH"], "cert.pem"),
					os.path.join(os.environ["DOCKER_CERT_PATH"], "key.pem")
				)
			) if "DOCKER_CERT_PATH" in os.environ else None,
			version="1.23"
		)
		
	def restore_certificates(self):
	
		base_dir = os.path.dirname(os.path.realpath(__file__))
		cert_dir = os.path.join(base_dir, "certificate")
		subprocess.check_call([
			"sh",
			os.path.join(cert_dir, "build.sh")
		])
		
		build_dir = os.path.join(cert_dir, "build")
		return (
			[
				caviar.certificate.path.PathCertificate(
					path=os.path.join(
						build_dir,
						"ca/certs/chain.pem"
					)
				)
			],
			caviar.certificate.SimpleCertificateKey(
				certificate=caviar.certificate.path.PathCertificate(
					path=os.path.join(
						build_dir,
						"server/certs/domain-admin-cert.pem"
					)
				),
				key=caviar.certificate.path.PathPrivateKey(
					path=os.path.join(
						build_dir,
						"server/private/domain-admin-key.pem"
					)
				)
			),
			caviar.certificate.SimpleCertificateKey(
				certificate=caviar.certificate.path.PathCertificate(
					path=os.path.join(
						build_dir,
						"server/certs/domain-inst-cert.pem"
					)
				),
				key=caviar.certificate.path.PathPrivateKey(
					path=os.path.join(
						build_dir,
						"server/private/domain-inst-key.pem"
					)
				)
			),
			caviar.certificate.SimpleCertificateKey(
				certificate=caviar.certificate.path.PathCertificate(
					path=os.path.join(
						build_dir,
						"server/certs/cluster-cert.pem"
					)
				),
				key=caviar.certificate.path.PathPrivateKey(
					path=os.path.join(
						build_dir,
						"server/private/cluster-key.pem"
					)
				)
			)
		)

