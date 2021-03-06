
.. contents::

Introduction
============

This package implements a simple catcher for gitlab tag event
webhooks.  The program will checkout the tag, create a source
distribution of the python package and upload it to a given pypi.
There is also a helper script to upload existing tags in a repository
to pypi.

Usage
=====

gitlab-taghook-upload-tags
--------------------------

This script clones a repository to a temporary folder and pushes all
tags as source releases to a specified pypi repository.

Arguments:

* :code:`--pypi PYPINAME` PyPI repository where to upload your product to
* :code:`--repository REPO` URL pointing to the git repository of your sources
* :code:`--python-path PATH` optional argument, path to the python
  interpreter used to create the distribution


gitlab-taghook-catcher
----------------------

When calling the catcher with `gitlab-taghook-catcher` you have to give
two arguments.

* :code:`--port PORT` specifies the port (surprise)
* :code:`--repository REPO` specifies the name of the pypi where to
  upload to
* :code:`--allowed IP [IP ...]` optional argument, list of hosts that
  are allowed to push events to the server
* :code:`--gitlabdomain DOMAIN [DOMAIN ..]` optional argument, list of hostnames of
  authorized gitlab instances
* :code:`--python-path PATH` optional argument, path to the python
  interpreter used to create the distribution

Configuration
=============

For the script to work it is requiered that user who executes the
script has a properly configured :code:`.pypirc`.  Also the user
running script needs read access to the gitlab repository to checkout
the source.

License and Copyright
=====================

Copyright 2014 Sebastian Jordan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
