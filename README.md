CAVIAR
======

Distribute package
------------------

With an already registered user in [Python Package Index](https://pypi.org/),
build and upload it with

```
$ python3 setup.py bdist_egg upload
```

The home page of the package will be available
[here](https://pypi.python.org/pypi/caviar/).

Publish documentation
---------------------

To publish documentation at GitHub Pages, at the project root path and
documentation branch, follow next steps. If *gf-pages* remote branch
exists, remove it.

```
$ python3 setup.py build_sphinx
$ mkdir .tmp
$ mv docs/build/html/* .tmp
$ git stash
$ git checkout --orphan gh-pages
$ rm -rf *
$ mv .tmp/* .
$ rm -rf .tmp
$ touch .nojekyll
$ git add --all .
$ git commit -m "Project doumentation"
$ git push <remote> gh-pages
$ git checkout <documentation_branch>
$ git branch -D gh-pages
$ git stash pop
```

Documentation will be available [here](http://miquelo.github.io/caviar/).
