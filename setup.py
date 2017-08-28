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

import distutils.cmd
import distutils.log

from setuptools import setup, find_packages

class CoverageCommand(distutils.cmd.Command):

	description = "Generate a test coverage report."
	user_options = []
	
	def initialize_options(self):
	
		pass
	
	def finalize_options(self):
	
		pass 
		
	def run(self):
	
		import subprocess
		
		subprocess.check_call([
			"coverage",
			"run",
			"--source=packages",
			"setup.py",
			"test",
		])
		self.announce(
			"COVERAGE REPORT",
			level=distutils.log.INFO
		)
		subprocess.check_call([
			"coverage",
			"report"
		])
		subprocess.check_call([
			"coverage",
			"html"
		])

setup(
	cmdclass={
		"coverage": CoverageCommand
	},
	
	name="caviar",
	version="0.1.5",

	author="Miquel A. Ferran Gonzalez",
	author_email="miquel.ferran.gonzalez@gmail.com",

	packages=find_packages("packages"),
	namespace_packages=[
		"caviar",
		"caviar.provider",
		"caviar.provider.machinery",
		"caviar.provider.ssh"
	],
	package_dir={
		"": "packages"
	},
	test_suite="testsuite",

	url="https://pypi.python.org/pypi/caviar",

	license="LICENSE.txt",
	description="Easy to use tools for advanced GlassFish management.",
	long_description=open("README-PIP.md").read()
)

