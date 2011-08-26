.. _instalazioa:

Instalazioa
===========

TZOS makina berri batean instalatzeko eman beharreko pausuak azaltzen 
dira hemen. Instalazioa Debian GNU/Linux sistematarako deskribatuko da.

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
    instalazioari argibide gehiago daude :ref:`beharrak-dbxml` azpiatalean.
MySQL
    5.x bertsioa.

    Python modulua instalatzeko ere beharrezkoa izango da `libmysqlclient-dev`
    paketea instalatzea.
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
iturburu-kodearen kopia eta `Fabric`_ 1.0 edo berriagoa beharko ditu [#f1]_
[#f2]_. Fabric komandoak exekutatzeko `sudo` eta `python-jinja2` paketeak
instalatuta izatea ere beharrezkoa da.

Esan gabe doa zerbitzarira SSH bidezko konexioa ere behar dela.

.. _pip: http://pypi.python.org/pypi/pip/
.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv/
.. _MPM worker: http://httpd.apache.org/docs/2.0/mod/worker.html
.. _mod_wsgi: https://code.google.com/p/modwsgi/
.. _Memcached: http://memcached.org/
.. _git: http://git-scm.org/
.. _Mercurial: http://mercurial.selenic.com/
.. _Fabric: http://fabfile.org/

.. _beharrak-dbxml:

DB-XML
^^^^^^

DB-XML instalatzeko beharrezkoa da eskuz konpilatzea eta instalatzea.
Konpilazioa burutu ahal izateko, `build-essential` eta `python-dev`
paketeak instalatu beharko dira Debian sistemetan.

Gero `DB-XMLren iturburu-kodea`_ deskargatu behar da (saioa hastea eskatzen
du) zerbitzarian, artxiboa despaketatu eta instalatzeko.

.. code-block:: bash

    tar xvfz dbxml-2.5.16.tar.gz
    cd dbxml-2.5.16
    sh buildall.sh --prefix=/usr/local

Honek DB-XML konpilatuko du urrats bakarrean eta ``/usr/local`` barruan
instalatuko du guztia. Instalazioa egiteko `root` baimenak beharko dira.

Jarraian DB-XMLren eta Berkeley DBren Python-erako `binding`\ak konpilatu
eta instalatu behar dira. Berkeley DBren `binding`\ak banaketako paketea
instalatuz lor daitezke, baina garrantzitsua da DB-XML konpilatu den `bsddb`
bertsio berdina erabiltzea, hortaz DB-XMLrekin batera datorren paketea
erabiliko da.

.. code-block:: bash

    cd dbxml/src/python
    python setup.py build
    python setup.py install
    cd bsddb3-4.8.1
    python setup.dbxml.py build
    python setup.dbxml.py install

`Binding` hauek, halere, beranduago sortuko den ingurune birtualean eskuz
kopiatu beharko dira.

.. _DB-XMLren iturburu-kodea:
    http://download.oracle.com/otn/berkeley-db/dbxml-2.5.16.tar.gz

.. _instalatzea:

TZOS instalatzea
----------------

Kontuan izan TZOS instalatu aurretik :ref:`sistemaren-beharrak` instalatu
behar direla.

Modu automatizatua
^^^^^^^^^^^^^^^^^^

TZOS modu automatizatuan instala daiteke eta horrela zerbitzariaren
komando-lerrotik eginkizun minimoak burutuko dira.

Hau horrela izan dadin, `Fabric` izeneko tresna erabiltzen da, `fabfile`
izeneko fitxategi (`script`) berezi baten laguntzaz. `Fabfile` batek
zerbitzarian (edo hainbat zerbitzaritan) exekutatuko diren komandoen multzoak
definitzen ditu. TZOSen iturburuan `fabfile` bat dago instalazio-prozesua
automatizatzeko eta, beraz, itruburu-kodea eskuratu beharko da ezertan hasi
aurretik::

    git clone git://github.com/julen/tzos.git

Honek ``tzos`` izeneko direktorio baten azpian utziko du iturburu-kode guztia.

.. _instalazioa-fabric:

`Fabric`\en konfigurazioa
`````````````````````````

`Fabric` erabiltzeko, zerbitzariaren xehetasunak eman beharko zaizkio
konfigurazio-fitxategi berezi batean. Horretarako, iturburu-kodearen
``configs`` direktorioaren barruan ``fabric.py`` izeneko fitxategia sortu
beharko da, ondorengo edukiarekin::

    # -*- coding: utf-8 -*-

    #
    # Connection settings
    #
    HOSTS = ['1.2.3.4']
    USER = 'erabiltzaile-izena'

    #
    # Project settings
    #
    PROJECT_NAME = 'tzos'
    PROJECT_PATH = '/var/www/%s' % PROJECT_NAME
    PROJECT_REPO = 'git://github.com/julen/tzos.git'
    PROJECT_URL = 'aplikazioaren.helbidea.tld'
    PROJECT_SETTINGS = PROJECT_PATH + '/tzos/production.py'

    #
    # Apache settings
    #
    VHOST_DIR = '/etc/apache2/sites-available'
    VHOST_FILE = VHOST_DIR + '/' + PROJECT_NAME

    #
    # WSGI settings
    #
    WSGI_FILE = PROJECT_PATH + '/tzos/tzos.wsgi'
    WSGI_USER = 'erabiltzaile-izena'
    WSGI_GROUP = 'erabiltzaile-taldea'

Konfigurazio-fitxategi honetan garrantzitsuenak ``HOSTS`` [#f3]_, ``USER`` eta
``PROJECT_URL`` aldagaiak dira. Lehenengo biek SSH konexioaren informazioa
zehazten dute. Azken ezarpena Apacheren `VirtualHost`\ean erabiliko da
`ServerName` direktibaren balio gisa.

.. note::

    Beharrezkoa da ``USER`` aldagaian zehaztutako erabiltzaileak `sudo`
    bitartez administrazio-ekintzak burutzeko gaitasuna izatea.

WSGI prozesuak zein erabiltzaile/talderen baitan exekutatuko diren zehazten dute
``WSGI_USER`` eta ``WSGI_GROUP`` gakoek. Gainontzeko aldagaien balioek bere
horretan ez lukete arazorik sortu behar Debian sistemetan. Konturatu halaber,
aplikazioaren beraren konfigurazio-fitxategia ``PROJECT_SETTINGS`` aldagaian
zehazten dela. Aldagai honen balioa ingurune-aldagai gisa ezarriko da WSGI
`script`\ean, gerora aplikazioak hortik irakur dezan konfigurazioa.

`Fabric`\en konfigurazioa burutu ostean, sistemako ``PYTHONPATH``
ingurune-aldagaian TZOSen iturburu-kodea dagoen direktorioa zehaztu beharko da,
`Fabric`\ek konfigurazio-modulua bertatik inportatu ahal izateko.

.. code-block:: bash

    export PYTHONPATH=/path/to/tzos:$PYTHONPATH

Zerbitzariko konfigurazioa
``````````````````````````

Fabric bidez konfigurazio osoa burutzeko, aplikazioak zerbitzarian izango duen
konfigurazio-fitxategia ere eman behar zaio. Bestelakorik ez bada zehaztu
`Fabric`\en ``PROJECT_SETTINGS`` konfigurazio-gakoan, fitxategi hau
``production.py`` izenarekin kokatu behar da ``configs/`` direktorioan.
Azken finean garapenean erabiltzen den ``config.py`` fitxategiaren kopia bat
da, zerbitzariko ingurunera moldatutako konfigurazioarekin eta `fabfile`\ak
eskaintzen dituen konfigurazio-balioa berrerabiltzeko prestatuta::

    DEBUG = False

    SECRET_KEY = 'f00barbaZ'

    # TZOS stuff
    TZOS_DEFAULT_DICT_LANG = 'eu'
    TZOS_REGISTER_WHITELIST = ('@ehu.es', '@ikasle.ehu.es',)
    TZOS_ACTIVATION_DAYS = 5
    TZOS_MAX_UPLOADS = 100

    TZOS_DB_HOME = '{{ project_path }}/tzos/dbs/'
    TZOS_BKP_HOME = '{{ project_path }}/backups/'

    TZOS_BEHIND_PROXY = False
    TZOS_SCRIPT_PREFIX = '/'

    TZOS_MYSQL_HOST = 'localhost'
    TZOS_MYSQL_DBNAME = 'tzosdb'
    TZOS_MYSQL_USERNAME = 'tzos'
    TZOS_MYSQL_PASSWORD = 'nirepasahitza'

    # Caching
    CACHE_TYPE = "memcached"
    CACHE_MEMCACHED_SERVERS = ["127.0.0.1:11211"]
    CACHE_DEFAULT_TIMEOUT = 900

    # SQLAlchemy database settings
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(TZOS_MYSQL_USERNAME,
                                                               TZOS_MYSQL_PASSWORD,
                                                               TZOS_MYSQL_HOST,
                                                               TZOS_MYSQL_DBNAME)
    SQLALCHEMY_ECHO = False

    # DB-XML database settings
    DBXML_ENV = '{{ project_path }}/tzos/dbs/dbxml/'
    DBXML_DATABASE = DBXML_ENV + 'tzos.dbxml'
    DBXML_BASE_URI = 'file://{{ project_path }}/tzos/xquery/'
    DBXML_CACHESIZE_GB = 0
    DBXML_CACHESIZE_BYTES = 512 * 1024 * 1024
    DBXML_MAX_LOCKS = 10000
    DBXML_MAX_LOCKERS = 10000
    DBXML_MAX_OBJECTS = 10000
    DBXML_LOG_AUTOREMOVE = True

    # Babel configuration settings
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'CET'

    # Recaptcha settings
    RECAPTCHA_USE_SSL = True
    RECAPTCHA_PUBLIC_KEY = '6LchVcASAAAAAGfvqAQAQEkq2K-YIOeG9HlAtVln'
    RECAPTCHA_PRIVATE_KEY = '6LchVcASAAAAAHU6lMuS8BaBoC5goiMwbGry1KHs'

    # Assets settings
    ASSETS_DEBUG = False
    ASSETS_DIRECTORY = '{{ project_path }}/tzos/static/'

Konfigurazioa espezifikoa da zerbitzariarentzat eta proiektuaren bideak
berrerabiltzen dira, `Fabric`\eko konfigurazioan zehaztu bezala. Bertako
konfigurazioko balioak ``{{`` eta ``}}`` karaktereen artean doaz. `Jinja
txantiloi-motorraren sintaxia`_ onartzen da fitxategi honetan beraz.

.. _Jinja txantiloi-motorraren sintaxia:
    http://jinja.pocoo.org/docs/templates/

`Fabric` komandoak
``````````````````

`Fabfile`\ak dituen komandoak bistaratzeko, `fabfile`\a dagoen direktorioan
``fab -l`` komandoa idatzi behar da.

.. code-block:: bash

    cd /path/to/tzos
    fab -l

Bistaratzen diren komandoen artean, ``bootstrap`` erabiliko da hasierako
ingurune birtuala eta direktorio-egitura sortzeko. Urrats honek, aldi berean,
iturburu-kodea deskargatuko du zerbitzarian.

Bestalde, ``deploy`` komandoak aplikazioaren menpekotasun guztiak [#f4]_
deskargatu eta instalatuko ditu eta azkenik, gunea konfiguratu eta aktibatuko
du. Komando bat baino gehiago exekuta dezakegu aldi berean, gainera::

    fab bootstrap deploy

`Fabfile`\ak automatikoki konfiguratzen eta instalatzen ditu Apache-ko
`VirtualHost` fitxategia eta WSGI `script`\a `mod_wsgi`\rentzat. Konfigurazioa
doitu nahi izanez gero, editatu ``configs/virtualhost.conf`` eta
``configs/tzos.wsgi`` fitxategiak.

.. note::

    Kontuan izan konfigurazio-aldaketek eragina izan dezaten
    ``fab update_config touch`` exekutatu behar dela. Lehenengo komandoak
    konfigurazio-fitxategiak eguneratzen ditu eta bigarrenak Apache
    zerbitzariari abisatzen dio aldaketak daudela fitxategietan eta
    kodea birkargatu behar duela.

Azkenik, :abbr:`PO (Portable Object)` formatuan dauden webgunearen itzulpen
estatikoak konpilatu behar dira. Horretarako ``compile_translations`` agindua
exekutatu behar da.

.. code-block:: bash

    fab compile_translations


Eskuzko urratsak
^^^^^^^^^^^^^^^^

Guztia ezin daitekeenez automatikoki konfiguratu, eskuz egin beharreko azken
ekintza batzuk daude. Hauetako batzuk komando-lerroko aginduen bitartez burutu
beharko dira, beste batzuk, aldiz, bereziki prestatutako kudeaketa-komandoen
bitartez.

Kudeaketa-komandoak
```````````````````

`Flask-Script`_\en laguntzarekin, hainbat kudeaketa-komando ditu TZOSek. Komando
hauek batez ere garapenerako ingurunean dira erabilgarriak baina instalazioa
zerbitzari publikoan egitean ere komandoren bat zein beste beharrezkoak dira.

.. note::

    Zerbitzariko konfigurazio-fitxategia garapenekoaren desberdina bada
    (biziki gomendatzen da hala izatea), ``--config=gurekonfigurazioa.py``
    aukera gehitu beharko diogu ``manage.py`` komando bakoitzaren deiari.
    Edo bestela ``TZOS_CONFIG`` ingurune-aldagaiak konfigurazio-fitxategi
    egokira zuzendu beharko du.

Komandoak exekutatu aurretik, zerbitzariko `shell`\ean ingurune birtuala
aktibatu behar da:

.. code-block:: bash

    cd /var/www/tzos
    source env/bin/activate

Hortik aurrera komando-lerroaren hasieran ``(env)`` agertuko da. Ingurunetik
irteteko ``deactivate`` komandoari deitu behar zaio.

Kudeaketa-komandoak ``manage.py`` fitxategiari dei eginez exekutatzen dira.
Inolako argumenturik gabe deituz gero, eskura dauden komandoen zerrenda
bistaratzen da:

.. code-block:: bash

    python manage.py
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

Ingurune birtuala osatzea
`````````````````````````

DB-XML konpilatutakoan, honen eta Berkeley DBren Python-erako `binding`\ak
ere konpilatu eta instalatu dira. Hauek ordea, aplikazioak erabiltzen duen
ingurune birtualetik kanpo daude eta kopiatu egin behar dira (instalatzean
``/usr/local`` barruan geratu dira, baina ingurune birtualaren fitxategiak
``/var/www/tzos/env`` barruan daude).

.. code-block:: bash

    cp -a /usr/local/lib/python2.6/dist-packages/bsddb3* /var/www/tzos/env/lib/python2.6/site-packages/
    cp /usr/local/lib/python2.6/dist-packages/*dbxml* /var/www/tzos/env/lib/python2.6/site-packages/


DB-XML
``````

DB-XML datu-basea hasieratzeko, beharrezkoa da bi fitxategi inportatzea
aplikazioaren edukiontzi edo `container`-ean. Horren aurretik, gainera,
indizeak sortu beharko dira.

.. note::

    Indizeak beranduago ere sor daitezke baina aurretik zeuden indize guztiak
    birsortzea dakar eta eragiketa oso garestia izan daiteke tamaina handiko
    datu-baseetan.

.. code-block:: bash

    python manage.py add_indexes
    Indexes added successfully.
    python manage.py add_document -f bootstrap/tzos.xml -d tzos.xml --config=production.py
    Document added successfully.
    python manage.py add_document -f bootstrap/tzos.xcs -d tzos.xcs --config=production.py
    Document added successfully.

Garrantzitsua da gainera goiko dokumentu-izen horiek ezartzea, aplikazioak
izen horiek erabiltzen baititu zenbait kontsultatan.

SQL
```

Aplikazioaren datu jakin batzuk (erabiltzaileak, jakintza-arloak,
jatorriak...) SQL datu-basean gordetzen dira eta datu-basea bera sortu,
eskema inportatu eta hasierako balio erabilgarri batzuk ere kargatu egin
behar dira.

MySQL datu-basea sortzea
''''''''''''''''''''''''

Aurrez MySQL datu-baseekin lan egin duen edonorentzat ohiko urratsa izango da
datu-base eta erabiltzaile berriak sortzea. Eragiketa `root` gisa egin
beharko da, hau da, `root` erabiltzaileak abiatu beharko du MySQL kontsola,
oro har erabiltzaile honek izaten baitu sisteman datu-baseak sortzeko baimena:

.. code-block:: mysql

    mysql> create database tzosdb;
    mysql> grant usage on *.* to tzos@localhost identified by 'nirepasahitza';
    mysql> grant all privileges on tzosdb.* to tzos@localhost;

Honek, beraz, `tzosdb` datu-basea sortuko du eta `tzos` erabiltzaile-izena
eta `nirepasahitza` pasahitza erabiliz atzitu ahal izango da.

Eskema eta hasierako datuak
'''''''''''''''''''''''''''

Eskema sortu eta datuak kargatzeko prest dago datu-basea beraz. Horretarako
``createall`` eta ``initdb`` komandoak daude eskura.

.. code-block:: bash

    python manage.py createall --config=production.py
    python manage.py initdb --config=production.py

``initdb`` komandoak hasierako jakintza-arloak eta terminoen jatorriak gehitzeaz
gain, lehenetsitako erabiltzaile batzuk ere sortuko ditu:

    * admin/admin: administraziorako baimenekin
    * supervisor/supervisor: gainbegiratzaile baimenekin
    * corrector/corrector: zuzentzaile baimenekin
    * member/member: besterik ezeko erabiltzaile erregistratua

Sistemaren administratzailearen lana da hasierako erabiltzaile hauek kudeatzea
erabilera egokia emateko.

``dropall`` komandoa ere badago, datu-baseko datuak husteko balio duena,
baina garapen inguruneetarako da erabilgarria soilik.

Honekin guztiarekin aplikazioa instalatuta dago. Jarraian,
:ref:`zerbitzariarekin lotutako konfigurazioa <konfigurazioa>` doitu
beharko da.


.. rubric:: Oin-oharrak

.. [#f1] SSH erabiliz sistemen administraziorako eta aplikazioen ezarpenerako
         komando-lerroko tresna eta Python liburutegia da Fabric.
.. [#f2] Gerta liteke Debian sistemetan Fabric 1.0 edo berriagoa eskura ez
         izatea. Hala bada, ``pip install fabric`` komandoarekin instalatu
         beharko da, `root` gisa, sistema osorako eskura egon dadin.
.. [#f3] Konturatu ``HOSTS`` aldagaiaren balioa Pythoneko lista bat dela,
         hau da, ``[`` eta ``]`` artean doan karaktere-kateen segida izan
         daiteke, nahi izanez gero hainbat ostalari-izen/IP helbide zehaztuz.
.. [#f4] Aplikazioaren menpekotasunak ``requirements.txt`` fitxategian
         definitzen dira. `Pip-ek ulertzen duen formatuan`_ dago.

.. _Pip-ek ulertzen duen formatuan:
    http://www.pip-installer.org/en/latest/requirement-format.html
