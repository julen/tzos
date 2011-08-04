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

    Atzerapenak ekiditeko, komenigarria da datu-basearen babeskopia egitea
    eta kopiako fitxategiak kargatzea ingurune errealean. Babeskopiak egiten
    direnean azken log fitxategia gordetzen da soilik eta aplikazioaren
    hasieratzea azkarragoa da.
