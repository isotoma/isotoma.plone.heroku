# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is a startup command to run from Procfile (on heroku or foreman)
# It will let you run a Zope instance from virtualenv, too.
# It expects to be passed a port to listen to on the command line
# It expects that DATABASE_URL is available.

import os, sys, optparse
from isotoma.plone.heroku.instance import Instance

def run():
    p = optparse.OptionParser()
    opts, args = p.parse_args()

    if not os.path.exists(args[0]):
        print args[0], "not found"
        sys.exit(1)

    Instance().run("run", *args)


def debug():
    Instance().run("debug")

