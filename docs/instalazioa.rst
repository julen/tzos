Instalazioa
===========

TZOS makina berri batean instalatzeko eman beharreko pausuak azaltzen 
dira hemen. Instalazioa GNU/Linux sistematarako deskribatuko da.

.. _sistemaren-beharrak:

Sistemaren beharrak
-------------------

Zerbitzari batean TZOS instalatzeko, ondorengo behar zehatzak ase behar dira:

Python
    2.6 edo berriagoa.

    Lengoaiaren euskarriaz gainera, Python-eko pakete konkretu batzuk ere
    behar dira: `pip`_, `setuptools`_ eta `virtualenv`_.
Oracle DB-XML
    2.5.16 bertsioa, Python-erako `binding`\ekin konpilatuta. DB-XMLren
    instalazioari argibide gehiago daude :ref:`instalatzea` ataleko
    :ref:`instalatzea-dbxml` azpiatalean.
MySQL
    5.x bertsioa.
Apache
    2.2.x bertsioa, `MPM Worker`_ eta `mod_wsgi`_ 3.3 moduluekin.
Memcached
    `Memcached`_ `cache` sistema Python-erako `binding`\ekin.
Bertsio-kontrolerako sistemak
    Kodea eskuratzeko beharrezkoak dira `git`_ eta `Mercurial`_.

Posta bidaltzeko aplikaziotik bertatik (izena ematerakoan, pasahitzak
berrezarri nahi direnean...), SMTP zerbitzari bat edo urruneko zerbitzari
bateko SMTP kontu bat ere behar da.

Bestetik, zerbitzariko instalazio-prozesua automatizatu nahi bada, bezeroak
iturburu-kodearen kopia eta `Fabric`_ beharko ditu [#f1]_. Esan gabe doa
zerbitzarira SSH bidezko konexioa ere behar dela.

.. _pip: http://pypi.python.org/pypi/pip/
.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv/
.. _MPM worker: http://httpd.apache.org/docs/2.0/mod/worker.html
.. _mod_wsgi: https://code.google.com/p/modwsgi/
.. _Memcached: http://memcached.org/
.. _git: http://git-scm.org/
.. _Mercurial: http://mercurial.selenic.com/
.. _Fabric: http://fabfile.org/

.. _instalatzea:

TZOS instalatzea
----------------

Kontuan izan TZOS instalatu aurretik :ref:`sistemaren-beharrak` instalatu
behar direla.

Modu automatizatua
^^^^^^^^^^^^^^^^^^

Kudeaketa-komandoak
^^^^^^^^^^^^^^^^^^^

`Flask-Script`_\en bitartez, hainbat kudeaketa-komando ditu TZOSek. Komando
hauek batez ere garapenerako ingurunean dira erabilgarriak, baina instalazioa
zerbitzari publikoan egitean ere komandoren bat zein beste beharrezko izango
da.

.. note::

    Zerbitzariko konfigurazio-fitxategia garapenekoaren desberdina bada
    (biziki gomendatzen da hala izatea), ``--config=gurekonfigurazioa.py``
    aukera gehitu beharko diogu ``manage.py`` komando bakoitzaren deiari.
    Edo bestela ``TZOS_CONFIG`` ingurune-aldagaiak konfigurazio-fitxategi
    egokira zuzendu beharko du.

Kudeaketa-komandoak ``manage.py`` fitxategiari dei eginez exekutatzen dira.
Inolako argumenturik gabe deituz gero, eskura dauden komandoen zerrenda
bistaratzen da::

    $ python manage.py
    shell         Runs a Python shell inside Flask application context.
    assets        Manage assets.
    rm_document   Removes a document from the XML-DB that matches the given name.
    add_indexes   Adds proper indexes to the DB-XML container.
    add_document  Adds a document to the XML-DB by feeding data from the given file.
    createall     Creates the SQL tables needed by the models.
    runserver     Runs the Flask development server i.e. app.run()
    dropall       Deletes all the SQL database data.
    initdb        Initializes some basic data to start playing with the app.

Hemen bereziki datu-basearekin lan egiten duten komandoak dira
interesgarrienak: ``add_indexes``, ``add_document``, ``createall`` eta
``initdb``. Lehenengo biek DB-XML datu-basearekin dute zerikusia; azken biek,
aldiz, SQL datu-basearekin.

.. _Flask-Script: http://packages.python.org/Flask-Script/

.. _instalatzea-dbxml:

DB-XML
^^^^^^

DB-XML datu-basea hasieratzeko, beharrezkoa da bi fitxategi inportatzea
aplikazioaren edukiontzi edo `container`-ean. Horren aurretik, gainera,
indizeak sortu beharko dira.

.. note::

    Indizeak beranduago ere sor daitezke baina aurretik zeuden indize guztiak
    birsortzea dakar eta eragiketa oso garestia izan daiteke tamaina handiko
    datu-baseetan.

.. code-block:: bash

    $ python manage.py add_indexes
    Indexes added successfully.
    $ python manage.py add_document -f bootstrap/tzos.xml -d tzos.xml
    Document added successfully.
    $ python manage.py add_document -f bootstrap/tzos.xcs -d tzos.xcs
    Document added successfully.

Garrantzitsua da gainera goiko dokumentu-izen horiek ezartzea, aplikazioak
izen horiek erabiltzen baititu zenbait kontsultarako.

SQL
^^^

MySQL datu-basea sortzea
````````````````````````

Aurrez MySQL datu-baseekin lan egin duen edonorentzat ohiko urratsa izango da
datu-base eta erabiltzaile berriak sortzea. Eragiketa `root` gisa egin
beharko da, oro har erabiltzaile honek izaten baitu sisteman datu-baseak
sortzeko baimena::

    # mysql -u root -p
    mysql> create database tzosdb;
    mysql> grant usage on *.* to tzos@localhost identified by 'nirepasahitza';
    mysql> grant all privileges on tzosdb.* to tzos@localhost;

Honek, beraz, `tzosdb` datu-basea sortuko du eta `tzos` erabiltzaile-izena
eta `nirepasahitza` pasahitza erabiliz atzitu ahal izango da.

Azken atazak
------------

TZOS instalatzen bukatzeko badaude azken unean egin beharreko zenbait ataza.
Konfigurazio gisa har daitezkeen arren, instalazioaren zatiaren baitan jarri
dira behin bakarrik egingo direlako eginkizun zehatz hauek.

.. rubric:: Oin-oharrak

.. [#f1] SSH erabiliz sistemen administraziorako eta aplikazioen ezarpenerako
         komando-lerroko tresna eta Python liburutegia da Fabric.
