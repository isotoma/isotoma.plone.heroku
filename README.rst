Plone on Heroku
===============

** WARNING ** Currently Plone contains syntax errors (skins aren't valid
python, why are we calling then .py!!) and heroku really doesn't like that.
Currently you can't deploy again after the first successful Plone
deployment because of it. I have reported this.


You will require
----------------

 * The heroku tools installed locally and working
 * A verified heroku account
 * A willingness to spend $15 a month for 20GB of Postgres (Plone doesnt
   fit in 5mb).


Starting a project
------------------

We need to be able to install Plone in a virtualenv and do without any of the
environment building capabilities of buildout. On top of that, the runtime
environment is temporary, so we cant build it manually after the initial push.

In your requirements.txt::

    isotoma.depends.zope2_13_8
    isotoma.depends.plone4_1
    isotoma.plone.heroku

The first 2 eggs are virtual packages that install 200+ packages in your
virtualenv. These are needed because we need to pin the versions of Plone that
are to be used.

The third egg provides ``bin/plone`` and ``bin/migrate``. These helpers
will dynamically provision their environment as it is required and instance
a site / run migrations.

We'll be using RelStorage to get cheap persistent storage. We have to use 1.4.2
over the 1.5.x series in order to avoid the plpgsql requirement it would
introduce.

At the time of writing it *appears* that only Django Python apps get a database
automatically. You can get one by adding a folder with an empty settings.py::

    django_bait/
        settings.py

You will need a Procfile so heroku knows how to run a zope instance::

    web: ./bin/plone -p $PORT


Doing a local build
-------------------

Build your virtualenv::

    virtualenv .
    ./bin/pip install -r requirements.txt

You can start a plone instance like this::

    ./bin/plone

That will get you a plone instance running on port 8080. By default it won't
be using any data store.


Adding your product
-------------------

You can quickly create a new product with ZopeSkel::

    source bin/activate
    mkdir src && cd src
    pip install zopeskel
    zopeskel plone my.app

Then follow the prompts. Make sure to answer yes to the GenericSetup question.

You can add your own custom eggs to requirements.txt::

    -e src/myapp.app

The instructions tell you to use ``file:`` prefixes. They lie. Don't.

Your ZCML should be found by z3c.autoinclude.

Then you should be able to install your products throught the ZMI or by using the
migrate script described below.


Deploying to heroku
-------------------

Make sure all your changes are committed to your Git repo. Then::

    ~/bin/heroku create --stack cedar
    git push heroku master

Then wait. It should just work, if it doesn't its probably a timeout. It takes
a long time to deploy 200+ eggs and heroku probably thinks your deployment has gone
wrong and times out.

So edit your requirements::

    isotoma.depends.zope2_13_8
    # isotoma.depends.plone4_1
    isotoma.plone.heroku

Commit and push to heroku.

That will build Zope without Plone, about half of the eggs that needed to be built.
Then you can uncomment the Plone dependency egg and push again to finish off.

You should now have a working Plonesite!


Re-rooting your portal
----------------------

By default your actual site won't be at ``/`` it will be at ``/Plone``. We can fix
that with some old school Zope magic - note that the ``migrate`` command can set
this up for you automatically.

 * In the ZMI, in ``/Plone`` create a SiteRoot object. Default settings are fine.

 * In the ZMI, in ``/`` create a DTMLMethod containing::

       <dtml-let stack="REQUEST['TraversalRequestNameStack']">
         <dtml-if "stack and stack[-1]=='zmi'">
           <dtml-call "stack.pop()">
           <dtml-call "REQUEST.setVirtualRoot('zmi')">
         <dtml-else>
           <dtml-call "stack.append('Plone')">
         </dtml-if>
       </dtml-let>

 * In the ZMI, at ``/`` create an AccessRule and point it at the DTMLMethod we
   just created.

Now any requests for ``/foo`` will be handled by ``/Plone/foo`` and any requests
for ``/zmi/manage`` will be handled by ``/manage``. Success.


The migrate tool
----------------

The migrate script uses the plone setup features of ``isotoma.recipe.plonetools`` to
automate setup of your site. It can apply profiles, install products, set properties
and even call random mutators.

Add a migrate.cfg to the root of your project::

    [main]
    # The id of the Plone Site that is created. Default is Plone.
    site-id = Plone

    # The admin user that was created by mkzopeinstance - for us it will almost
    # certainly be admin. Default is admin.
    admin-user = admin

    # Whether or not to apply the SiteRoot/AccessRule policy described in the previous
    # section. Default is False.
    rootify = True

    # List of products to install on the initial migrate (when ``/Plone`` is created)
    products-initial =
        Products.foo

    # List of products to install (or reinstall) every time migrate is run
    products =
        Products.LinguagePlone

    # List of GenericSetup profiles to apply the first time migrate is run (when
    # ``/Plone`` is created)
    profiles-initial =
        myapp.policy:initial

    # List of GenericSetup profiles to apply every time ``bin/migrate`` is run
    profiles =
        myapp.policy:default

That one doesn't make any sense, but does show what you can do. To run it locally::

    ./bin/migrate -c migrate.cfg

And to run against your heroku app::

    ~/bin/heroku run ./bin/migrate -c migrate.cfg

The default is to look for a migrate.cfg in the root of the branch you you don't
have to tell it that - you can just ``./bin/migrate``.


Maintaining your app
--------------------

You can look at your looks with the built in heroku log tool::

    ./bin/heroku logs

You can get an interpreter pointed at your database with the debug command::

    ./bin/heroku run ./bin/debug

You can run a script in your git repo using the run command::

    ./bin/heroku run ./bin/run scripts/myscript.py

