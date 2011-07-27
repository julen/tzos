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
