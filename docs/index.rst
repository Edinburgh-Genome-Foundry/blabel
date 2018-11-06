
.. image:: _static/title.svg
   :width: 500px
   :align: center

.. raw:: html
  
  <p></p>

Welcome to icebreaker's documentation!
======================================

 
Icebreaker provides Python interface for the `JBEI ICE sample manager <https://github.com/JBEI/ice>`_.

See the full API documentation `here <https://edinburgh-genome-foundry.github.io/icebreaker/>`_

Installation
-------------

Icebreaker is written for Python 3+. You can install icebreaker via PIP:

.. code::

    sudo pip install icebreaker

Alternatively, you can unzip the sources in a folder and type

.. code::

    sudo python setup.py install

Example of use
---------------

In this example we assume that we are a lab who wants to find primers from its
database to sequence a given construct. We will (1) pull all our primers from
ICE, (2) find which primers are adapted to our sequence, using the
`Primavera package <https://edinburgh-genome-foundry.github.io/Primavera/>`_, and
(3) we will ask ICE for the location of the selected primers.


Connexion to an ICE instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can connecct to your ICE instance using either an API token (see below
for how to create a token), or an email/password authentication.

.. code:: python

    import icebreaker

    # CONNECT TO ICE
    configuration = dict(
        root="https://my.ice.instance.org",
        api_token="WMnlYlWHz+BC+7eFV=...",
        api_token_client = "icebot"
    )
    ice = icebreaker.IceClient(configuration)

Or:

.. code:: python

    # CONNECT TO ICE
    configuration = dict(
        root="https://my.ice.instance.org",
        email="michael.swann@genomefoundry.org",
        password = "ic3ic3baby"
    )
    ice = icebreaker.IceClient(configuration)

The configuration can also be written in a yaml file so you can write
``IceClient('config.yml')`` where ``config.yml`` reads as follows:

```
root: https://my.ice.instance.org
email: michael.swann@genomefoundry.org
password: ic3ic3baby
```

Extracting all records from a folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next we pull all primers in the database:

.. code:: python

    # FIND THE ID OF THE FOLDER WITH ALL PRIMERS
    primers_folder = ice.get_folder_id("PRIMERS", collection="SHARED")

    # GET INFOS ON ALL ENTRIES IN THE FOLDER (PRIMER NAME, ID, CREATOR...)
    primers_entries = ice.get_folder_entries(primers_folder)

    # GET A BIOPYTHON RECORD FOR EACH PRIMER
    primers_records = {primer["id"]: ice.get_record(primer["id"])
                       for primer in primers_entries}


Primer selection with Primavera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next provide this information to Primavera and select some primers (see the
`Primavera docs <https://edinburgh-genome-foundry.github.io/Primavera/>`_):

.. code:: python

    from primavera import PrimerSelector, Primer, load_record

    available_primers = [
        Primer(sequence=primers_records[entry['id']].seq.tostring(),
            name=entry['name'],
            metadata=dict(ice_id=entry['id']))
        for entry in primers_entries
    ]
    constructs = [load_record("RTM3_39.gb", linear=False)]
    selector = PrimerSelector(read_range=(150, 1000), tm_range=(55, 70),
                            size_range=(16, 25), coverage_resolution=10,
                            primer_reuse_bonus=200)
    selected_primers = selector.select_primers(constructs, available_primers)


Finding available samples
~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally we look for available samples for each primer:

.. code:: python

    selected_primers = set(sum(selected_primers, []))
    for primer in selected_primers:
        ice_id = primer.metadata.get("ice_id", None)
        if ice_id is not None:
            samples = ice.get_samples(ice_id)
            if len(samples) > 0:
                location = icebreaker.sample_location_string(samples[0])
                print("Primer %s is in %s." % (primer.name, location))

Result:

.. code:: bash

    Primer PRV_EMMA_IN00042 is in PRIMER_PLATE_1/E06.
    Primer PRV_EMMA_IN00043 is in PRIMER_PLATE_1/F06.
    Primer PRV_EMMA_IN00028 is in PRIMER_PLATE_1/G04.
    Primer PRV_EMMA_IN00060 is in PRIMER_PLATE_1/G08.
    Primer PRV_EMMA_IN00064 is in PRIMER_PLATE_1/C09.
    Primer PRV_EMMA_IN00038 is in PRIMER_PLATE_1/A06.
    Primer PRV_EMMA_IN00068 is in PRIMER_PLATE_1/G09.

API
---

.. autoclass:: icebreaker.IceClient
  :members:


Getting an ICE token
--------------------

There are several ways to get ICE tokens. We suggest you create one throug
the web interface as follows (see screenshot for indications):

0. Create an account with administrator rights
1. Go to the administrator panel
2. Click on "API keys"
3. Click on "create new". Note everything down !

.. image:: _static/api_key_screenshot.png
   :alt: screenshot
   :align: center

License = MIT
--------------

Icebreaker is an open-source software originally written at the Edinburgh
Genome Foundry by `Zulko <https://github.com/Zulko>`_ and `released on
Github <https://github.com/Edinburgh-Genome-Foundry/icebreaker>`_ under
the MIT licence (¢ Edinburg Genome Foundry). Everyone is welcome to
contribute !


More biology software
-----------------------

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Edinburgh-Genome-Foundry.github.io/master/static/imgs/logos/egf-codon-horizontal.png
 :target: https://edinburgh-genome-foundry.github.io/

Icebreaker is part of the `EGF Codons <https://edinburgh-genome-foundry.github.io/>`_ synthetic biology software suite for DNA design, manufacturing and validation.

.. raw:: html
  
  <a href="https://github.com/Edinburgh-Genome-Foundry/icebreaker" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#fff; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>