Konfigurazioa
=============

Konfigurazio-fitxategi bidez burutzen da TZOS aplikazioaren konfigurazioa.
Garapeneko ingurunean ``tzos/config.py`` da fitxategi hau.

Dena den, ingurune errealetarako beste fitxategi bat erabiltzea gomendatzen da
eta ``TZOS_CONFIG`` ingurune-aldagaian zehaztea konfigurazio-fitxategi
berrirako bide osoa. WSGI konfigurazio-fitxategian ezar daiteke
ingurune-aldagaia, adibidez::

    os.environ['TZOS_CONFIG'] = '/path/to/tzos/production_config.py'

.. note::

    Aplikazioa ingurune erreal batean ezartzeko prozesua Fabric bidez burutzen
    bada, `fabfile`\ak behar bezala ezarriko du ingurune-aldagaia.


Konfigurazio-gakoak
-------------------

.. include:: konfigurazio-gakoak.rst.inc

Mantentze-lanak
---------------

Badira aintzat hartu beharreko zenbait ohar aplikazioa modu egokian mantendu
nahi bada.

Gehiegizko log fitxategiak
    Berkeley DBaren inguruneko log fitxategiak pilatzen direnean, aplikazioaren
    hasieratzean atzerapenak sor daitezke.

    Atzerapenak ekiditeko, ziurtatu ``DBXML_LOG_AUTOREMOVE``
    konfigurazio-gakoaren balioa ``True`` gisa ezarrita dagoela. Beharrezkoak
    ez diren log fitxategiak ezabatuko ditu honek automatikoki.

    Log zaharrak alboratzeko beste modu bat babeskopiak egitea eta kopiak
    kargatzea da. Babeskopiak egitean azken log fitxategia gordetzen da soilik.

`Cache` zaharkitua
    TZOSen `cache`\a erabiltzen da zenbait tokitan, datu-basera egin litezkeen
    galdera errepikakor eta erredundateak saihesteko, batez ere.
    Erabiltzaile-mailen arabera ere funtzionaltasuna aktibatu/desaktibatu
    egiten da: erabiltzaile anonimoek `cache`\ko edukiak ikusiko dituzte
    askotan.

    `Cache`\a oro har ``CACHE_DEFAULT_TIMEOUT`` ezarpenak zehaztutako segundoak
    pasa ondoren berritzen da (hasierako orrian, adibidez) baina gerta liteke
    `cache`\a eskuz garbitzeko beharra izatea. Horrelako kasuetan, Memcached
    zerbitzaria berrabiarazi behar da.

.. code-block:: bash

    sudo /etc/init.d/memcached restart
