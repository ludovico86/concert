About
=====

.. image:: https://travis-ci.org/ufo-kit/concert.png?branch=master
    :target: https://travis-ci.org/ufo-kit/concert

.. image:: https://coveralls.io/repos/ufo-kit/concert/badge.png?branch=master
    :target: https://coveralls.io/r/ufo-kit/concert?branch=master

.. image:: https://pypip.in/v/concert/badge.png
    :target: https://crate.io/packages/concert/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/concert/badge.png
    :target: https://crate.io/packages/concert/
    :alt: Number of PyPI downloads

Concert is a light-weight control system interface to control Tango and native
devices. It can be used as a library::

    from concert.quantities import q
    from concert.devices.motors.dummy import Motor

    motor = Motor()
    motor.position = 10 * q.mm
    motor.move(-5 * q.mm)

or from a session and within an integrated `IPython`_ shell::

    $ concert init session
    $ concert start session

    In [1]: motor.position = 10 * q.mm
    10.0 millimeter

.. _Ipython: http://ipython.org

You can read more about *Concert* in the official `documentation`_.

.. _documentation: https://concert.readthedocs.org
