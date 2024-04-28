========================================
niapi - The Network Information API Tool
========================================

niapi is an API for gathering information about the network data.

It is built on the `Litestar <https://litestar.dev>`_ framework and `Pydantic <https://pydantic.dev/>`_.

Installation
------------

.. code-block:: shell

   pip install niapi

Usage
-----

You can use the hosted web interface, or ``pip install niapi`` and use the CLI:

.. code-block:: shell
    :caption: Get the network information for 10.200.0.1 with the 26 bit mask

    niapi check 10.200.0.1/26


.. toctree::
    :titlesonly:
    :caption: Documentation
    :hidden:

    usage/index
    api/index
    changelog
