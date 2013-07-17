Freevle Software for Schools [![Build Status](https://travis-ci.org/Freevle/Freevle.png?branch=project-hiroshima)](https://travis-ci.org/Freevle/Freevle)
=========================

What is Freevle
------------

Freevle is a Virtual Learning Environment (VLE). Now, there's some pretty good
examples of those out there, but Freevle is different. We wanted to integrate
every aspect of a school into Freevle: the website for non-students, parents or
teachers; the schedules for teachers, students, classes and classrooms, with
homework integrated; the environment for putting assignments online as well as
ways to learn or study on the web and other tools, like a students-only forum
and a project management system.

Features
--------

While Freevle is modular and thus extensible, it has a few essential modules
(or apps, as we call them) included. These are:

* User
* Importer
* CMS
* VirtualCR
* Organizer
* Galleries
* News
* Downloads


Installation
------------

### Dependencies

At this moment, the Hiroshima version of Freevle is only officially supporting
Python 3.3, and thus needs a few experimental branches of some libraries. This
might make it a bit of a pain to install it, for now. In the list below you can
not only find what versions you need, but also where to find them, if they're
not easy to find.

Instead of manually installing all these, you can also just check out the
`.travis.yml` file and follow the same steps as Travis would in its install
process.

* Python 3.3
* Flask 0.10.1
* Flask-SQLAlchemy 0.17
  (install from [github](https://github.com/mitsuhiko/flask-sqlalchemy))
* Flask-Babel 0.8.1
* Flask-SeaSurf 0.1.19
  (install from [github fork](https://github.com/FSX/flask-seasurf))
* SQLAlchemy 0.8
* Babel 1.0dev
  (install from [bitbucket](https://bitbucket.org/babel3_developers/babel3), be
  sure to follow [these instructions](http://babel.edgewall.org/wiki/SubversionCheckout)
  on how to import the locale data).

### Development

After going through the long and tedious process of installing all the packages
you can finally start working on Freevle!

It's a fairly simple process: copy the `settings.cfg.sample` to your own
personal `settings.cfg` file and change the settings to match your personal
setup. You can then run Freevle and its testing suite in either of two ways:

* Environment variable  
  Define an environment variable called `FREEVLE_SETTINGS` with the path to
  your `settings.cfg` file, then normally call `run.py` and `test.py`.
* Command line argument  
  Call the scripts with the path to your settings file as argument, so
  somewhat like `python run.py ../settings.cfg` and the same for `test.py`.

That's about it... for now.
