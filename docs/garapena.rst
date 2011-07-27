Garapena
========

Garapenaren inguruko xehetasunak, nondik norakoak, arkitektura, hartutako
erabakiak eta bestelakoak biltzen dira hemen.

Erabilitako teknologia
----------------------

Ezer ukitzen hasi aurretik, komeni da jakitea TZOS garatzeko mota
desberdineko hainbat teknologia erabili direla. Honen arabera, beharrezko
ingurunearen ezaugarriak modu batekoak edo bestekoak izango dira.

Aplikazioa nagusiki `Python`_ programazio-lengoaiaz idatzita dago, web
garapena erraztera zuzendutako `Flask`_ `framework`\a erabiliz. Flask-ek eremu
egonkor bat eskaintzen du horren gainean nahi ditugun piezekin aplikazioak
idazteko. Ohiko atazetarako `hedapenak`_ ere badauzka (datu-baseen atzipenerako,
inprimakien tratamendurako, erabiltzaile-saioen kudeaketarako...), eta
horietako batzuk ere erabili dira TZOS garatzeko.

Aldi berean, `Werkzeug`_ izeneko tresna multzo baten gainean dago eraikita Flask.
Tresna multzo honek Python munduko `WSGI`_ estandarra inplementatzen du

Aplikazioaren aurkezpena lantzeko Flask-ek dakarren `Jinja2 txantiloi-motorra`_
erabili da.

Azpi-azpian ordea `Berkeley DB-XML datu-base natiboa`_ dago, terminologiarako
bereziki prestatuta dagoen :abbr:`TBX (Term-Base eXchange)` formatua baita
TZOSen oinarria. DB-XMLk Python-erako `binding`\ak ditu eta datu-basean galderak
egiteko `XQuery lengoaia`_ erabiltzen da.

Modu paraleloan SQL datu-base bat ere erabiltzen da. Berez, azpian
`SQLAlchemy`_ liburutegi eta :abbr:`ORM (Object-Relational Mapper)`\a erabiltzen
denez, abstrakzio-geruza baten gainean egiten da lan eta atzean egon daitekeen
:abbr:`DBKS (Datu-Base Kudeaketa Sistema)`\arekiko independentea da. Halere,
garapenerako `SQLite`_ eta ingurune errealetarako `MySQL`_ erabiltzea
gomendatzen da.

Internazionalizazioa eta lokalizazioa `GNUren gettext tresnak`_ erabiliz
burutzen da nagusiki, `Babel`_ paketearen laguntzaz.

.. _Python: http://python.org/
.. _Flask: http://flask.pocoo.org/
.. _hedapenak: http://flask.pocoo.org/extensions/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _WSGI: http://wsgi.org/wsgi/
.. _Jinja2 txantiloi-motorra: http://jinja.pocoo.org/
.. _Berkeley DB-XML datu-base natiboa:
    http://www.oracle.com/us/products/database/berkeley-db/xml/index.html
.. _XQuery lengoaia: http://www.w3.org/TR/xquery/
.. _GNUren gettext tresnak: http://www.gnu.org/software/gettext/
.. _SQLAlchemy: http://sqlalchemy.org/
.. _SQLite: http://sqlite.org/
.. _MySQL: http://mysql.com/
.. _Babel: http://babel.edgewall.org/

Arkitektura
-----------

Aplikazioak ingurune erreal batean hartuko luken itxura ondorengoa da:

.. figure:: /_static/arkitektura.png

    Arkitektura orokorra.

Apache web zerbitzariak Internet bidez bezeroek egiten dituzten eskaerei
erantzuten die. Eskaeren erantzuna lortzeko, Apachek `mod_wsgi` prozesuarengan
uzten du ardura; honek aplikazioaren instantziak dituzten hainbat hari izan
ditzake martxan.

WSGI estandarraren bitartez komunikatzen dira Apacheren `mod_wsgi` modulua eta
erabilera orokorreko Werkzeug liburutegia. Werkzeugen oinarritzen denez Flask
eta TZOSek zuzenean Flask erabiltzen duenez, modu gardenean lan egiten da
zerbitzaritik datozen eskaeren gainean.

`View`, `Model`, `Template` patroia
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Eskaera bakoitzak bere berezitasunak ditu eta URLen araberako diskriminazioa
egiten da: URL bakoitza ikuspegi edo `view` batekin dago lotuta. Parekatzea
eta `URLen bideratzea`_ adierazpen erregularren bidez burutzen da.

Ikuspegi bakoitzak eskaeraren araberako parametroak jaso, eragiketak burutu
—beharrezko izanez gero datuen geruzara joz, hau da, modeloetara—, emaitza
txantiloi bidez errendatu eta erantzuna bueltatzen du.

Eragiketak burutzerako orduan behar bereziak sor daitezke, bai datuen mailan
edo bestelakoen tratamenduan (erabiltzaile-saioak, cookie-ak...) eta
horretarako Flasken gehigarriak erabiltzen dira nagusiki.

Hortaz, hiru zati berezitu garbi nabarmendu daitezke:

Ikuspegiak (`View`)
    Eskaerak URLen arabera ikuspegi jakinetara bidaltzen dira.
Modeloak (`Model`)
    Ikuspegiek deiak burutzen dituzte modeloen gainean, datuak eskuratuz,
    eraldatuz, txertatuz... erantzunaren irteera izango diren datuak lortuz.
Txantiloiak (`Template`)
    Datuak txantiloietara pasatzen dira, prozesatu eta errendatutakoa emaitza
    gisa bueltatzen da.

.. _URLen bideratzea: http://werkzeug.pocoo.org/docs/routing/


