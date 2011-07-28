Ondorengo konfigurazio-gakoak daude eskura TZOS aplikazioan. TZOSi
eta Flask-DBXMLri dagozkien balioak bakarrik zerrendatzen dira hemen.
Gainontzekoen konfigurazio-balioetarako begiratu Flask hedapen bakoitzaren
dokumentazioa.


.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

Orokorrak
^^^^^^^^^

=============================== =========================================
``TZOS_DEFAULT_DICT_LANG``      Besterik ezean glosategian hautatuta
                                egongo den hizkuntza. Bi karaktereko
                                hizkuntza-kodea jarri behar da hemen eta
                                kontuan izan hiztegiaren hizkuntzak
                                XML datu-basean egon behar duela.
``TZOS_REGISTER_WHITELIST``     Adierazpen erregular honek TZOSen izena
                                ematerako orduan mugatuko dituen helbide
                                elektronikoak zehazten ditu.
                                Adierazpen erregular bat baino gehiago
                                idatz daitezke tuplan elementu gehiago
                                sartuz. Tupla hutsa edo ``None`` balioa
                                ezartzen bada, ez da inolako egiaztapenik
                                egingo eta edozein helbide elektronikok
                                izango du izena emateko aukera.
                                Besterik ezean ``None`` balioa du.
``TZOS_ACTIVATION_DAYS``        Erabiltzaile-kontuak aktibatu arte gehienez
                                ere igaro daitezkeen egun kopurua.
                                Egun kopuru hau igarotzen bada eta kontua
                                oraindik aktibatzeke badago, `iraungita`
                                dagoela pentsatuko da eta erabiltzaile-izen
``TZOS_MAX_UPLOADS``            Inportazioak egiterakoan, gehienez ere igo
                                ahal izango den `kontzeptu` kopurua.
                                CSV fitxategien kasuan lerro kopuruarekin bat
                                etorriko da balio hau.
=============================== =========================================

Biltegiratzea, datu-baseak
^^^^^^^^^^^^^^^^^^^^^^^^^^

=============================== =========================================
``TZOS_DB_HOME``                Fitxategi-sisteman datu-baseek daukaten
                                kokapenaren bide absolutua. SQL
                                datu-baseen kasuan, SQLiteri bakarrik
                                eragiten dio ezarpen honek.
``TZOS_BKP_HOME``               Fitxategi-sisteman babeskopiak gordetzeko
                                erabiliko den direktorioaren bide
                                absolutua.
=============================== =========================================

MySQL
`````

=============================== =========================================
``TZOS_MYSQL_HOST``             MySQL datu-basea dagoen ostalari-izena.
``TZOS_MYSQL_DBNAME``           TZOSerako erabiliko den MySQL
                                datu-basearen izena.
``TZOS_MYSQL_USERNAME``         MySQL datu-basearen erabiltzaile-izena.
``TZOS_MYSQL_PASSWORD``         MySQL datu-basearen pasahitza.
=============================== =========================================

DBXML
`````

=============================== =========================================
``DBXML_ENV``                   Fitxategi-sisteman DBXML inguruneak
                                (log fitxategiak + kontainerra) daukan
                                kokapenaren bide absolutua.
``DBXML_DATABASE``              Fitxategi-sisteman DBXML kontainer edo
                                datu-baseak daukan kokapenaren bide
                                absolutua.
                                Besterik ezean ``default.dbxml`` erabiliko
                                da.
``DBXML_BASE_URI``              DBXMLk erabil litzakeen XQuery moduluak
                                bilatuko diren kokapenaren bide absolutua,
                                URI gisa. ``file://`` bidez hasi behar du
                                konfigurazio-balio honek.
``DBXML_CACHESIZE_GB``          DBXMLk erabiliko duen `cache`\aren
                                tamaina, GBtan.
``DBXML_CACHESIZE_BYTES``       DBXMLk erabiliko duen `cache`\aren
                                tamaina, Byte-tan.
``DBXML_MAX_LOCKS``             DBXMLren blokeo-mekanismoak erabiliko
                                dituen `lock` kopuru maximoa.
                                Argibide gehiagorako begiratu Berkeley
                                DBren dokumentazioa.
``DBXML_MAX_LOCKERS``           DBXMLren blokeo-mekanismoak erabiliko
                                dituen `locker` kopuru maximoa.
                                Argibide gehiagorako begiratu Berkeley
                                DBren dokumentazioa.
``DBXML_MAX_OBJECTS``           DBXMLren blokeo-mekanismoak erabiliko
                                dituen `object` kopuru maximoa.
                                Argibide gehiagorako begiratu Berkeley
                                DBren dokumentazioa.
=============================== =========================================