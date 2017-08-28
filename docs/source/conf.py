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

#
# General configuration
#

extensions = [
	"sphinx.ext.autodoc",
	"sphinx.ext.intersphinx",
	"sphinx.ext.ifconfig"
]

templates_path = [
	"_templates"
]
source_suffix = ".rst"
master_doc = "index"

project = "CAVIAR"
version = "0.1"
release = "0.1"

copyright = "2017, Miquel A. Ferran Gonzalez"
author = "Miquel A. Ferran Gonzalez"

language = None
exclude_patterns = []
pygments_style = "sphinx"
todo_include_todos = False
autodoc_member_order = "bysource"

#
# Options for HTML output
#

html_theme = "sphinx_rtd_theme"
# FIX for Debian Jessie
import sphinx_rtd_theme
html_theme_path = [
	sphinx_rtd_theme.get_html_theme_path()
]
# END FIX
html_static_path = [
	"_static"
]
htmlhelp_basename = "CAVIARdoc"

#
# Options for LaTeX output
#

latex_elements = {
}
latex_documents = [
	(
		master_doc,
		"CAVIAR.tex",
		"CAVIAR Documentation",
		"Miquel A. Ferran",
		"manual"
	)
]

#
# Options for manual page output
#

man_pages = [
	(
		master_doc,
		"trocola",
		"CAVIAR Documentation",
		[
			author
		],
		1
	)
]

#
# Options for Texinfo output
#

texinfo_documents = [
	(
		master_doc,
		"CAVIAR",
		"CAVIAR Documentation",
		author,
		"CAVIAR",
		"Easy to use tools for advanced GlassFish management.",
		"Miscellaneous"
	)
]

#
# Other options
#

intersphinx_mapping = {
	"https://docs.python.org/3/": None
}
