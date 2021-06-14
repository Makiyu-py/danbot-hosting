.. currentmodule:: danbot_api

#############
API Reference
#############

The following section outlines the API of danbot-hosting-py.

Version Related Info
====================

There are two main ways to query version information about the library.

.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

    Just like :obj:`py:sys.version_info` the valid values for ``releaselevel`` are 'alpha', 'beta', 'candidate' and 'final'.

.. data:: __version__

    A string representation of the version. e.g. ``'0.1.0'``.

Client
======

.. autoclass:: DanBotClient
    :members:

Exceptions
==========

.. autoexception:: DBHException
    :show-inheritance:

.. autoexception:: HTTPException
    :show-inheritance:

.. autoexception:: ServerError
    :show-inheritance:

.. autoexception:: APIError
    :show-inheritance:

Event reference
===============

.. function:: on_dbh_post(data)

    Called when the autopost successfully posts the data to the DBH API.

    :param data: The data that was posted to the API.

    Example: ::

        @bot.event
        async def on_dbh_post(data):
            print(data)
