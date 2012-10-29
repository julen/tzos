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
garapena erraztera zuzendutako `Flask`_ `micro framework`\a erabiliz.
Flask-ek eremu egonkor bat eskaintzen du horren gainean nahi ditugun
piezekin aplikazioak idazteko. Ohiko atazetarako `hedapenak`_ ere badauzka
(datu-baseen atzipenerako, inprimakien tratamendurako, erabiltzaile-saioen
kudeaketarako...), eta horietako batzuk ere erabili dira TZOS garatzeko.

Aldi berean, `Werkzeug`_ izeneko tresna multzo baten gainean dago eraikita
Flask. Tresna multzo honek Python munduko `WSGI`_ estandarra inplementatzen
du eta honen bitartez burutzen du komunikazioa web zerbitzariekin.

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

Azkenik, dokumentazio hau `Sphinx`_ tresnaren laguntzaz dago sortuta.

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
.. _Sphinx: http://sphinx.pocoo.org/

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

.. _vmt-patroia:

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

Direktorio-egitura
^^^^^^^^^^^^^^^^^^

Aplikazioak direktorio-egitura oso zehatzean biltzen du kode guztia eta
erraza da modulu edo funtzionaltasun konkretuak aurkitzea kode barruan.

Laburbilduta, hau litzateke direktorio-egituraren maila goreneko ikuspegi
orokorra::

    backups/
    bootstrap/
    configs/
    docs/
    tzos/

Egituraren goi-mailan aplikazioaren instalazioarekin, konfigurazioarekin eta
mantentze-lanekin lotutako kontuak daude. Dokumentazioa ere aurki daiteke.

Bertako ``manage.py`` `script`\a ezinbestekoa da garapenerako, integratutako
web zerbitzaria baitauka eta egindako kode-aldaketak automatikoki birkargatzen
ditu. Oro har ``python manage.py runserver`` izango da erabili nahi den
komandoa garapenerako zerbitzaria abiarazteko.

Maila honetan, halaber, itzultzeko kateak erauzi, batu eta konpilatzeko
``gettext.sh`` `script`\a dago. Hiru eragiketa sinple onartzen dira:

    * ``./gettext.sh extract`` komandoarekin azken itzulpenak erauzten dira.
      Emaitza ``tzos/translations/messages.pot`` txantiloian uzten da.
    * ``./gettext.sh update`` komandoak, azken txantiloia dagoeneko dauden
      itzulpenekin batzen du.
    * ``./gettext.sh compile`` komandoak itzulpenak konpilatzen ditu
      aplikazioak erabiltzeko moduko formatura.

Mamia ordea ``tzos/`` direktorioaren barruan dago, bertan biltzen baita
aplikazioaren iturburu-kodea::

    tzos/
        dbs/
            dbxml/
        forms/
        models/
        static/
            img/
        templates/
            account/
            admin/
            emails/
            errors/
            glossary/
            macros/
            search/
            terms/
            user/
            xml/
        translations/
            en/
                LC_MESSAGES/
            eu/
                LC_MESSAGES/
        views/
        xquery/

Azter dezagun direktorio bakoitza banan bana:

``dbs/``
    Aplikazioaren datu-baseak biltegiratzen dira hemen. Garapen-ingurunean,
    SQLite datu-basea ere hemen egongo da kokatuta. ``dbxml/``
    azpidirektorioan DB-XMLren ingurunea dago halaber.

``forms/``
    Inprimakien eta inprimakietan erabil daitezkeen eremuen definizioak.
    Gogoratu inprimakien kudeaketarako WTForms liburutegia erabiltzen dela
    Flask-WTFren bitartez.

    Aplikazioaren modulu bakoitzeko fitxategi bana dago: ``account.py``,
    ``admin.py``, ``comments.py``...

``models/``
    Modeloen definizioak.

    Modelo gehienak SQLAlchemyko modeloen azpiklase gisa daude inplementatua
    (Flask-SQLAlchemy-ko ``db.Model`` heredatuz, zehazki). Salbuespenak
    ``Term`` eta ``TermChange`` modulu bereziak dira.

    Aplikazioaren modulu bakoitzeko fitxategi bana dago: ``account.py``,
    ``admin.py``, ``comments.py``...

``static/``
    Aplikazioaren eduki estatikoak. Irudiak, CSS estilo-orriak eta JavaScript
    fitxategiak aurki daitezke hemen.

    Produkzio-inguruneetan, CSS eta JavaScript fitxategiak batu egiten dira
    Flask-Assets erabilita, sareko latentzia minimizatzeko asmoz. Horrela,
    hainbat fitxategi bakarrean biltzen dira.

    `Asset` edo baliabide estatikoen multzoak kodean definitzen dira,
    ``application.py`` fitxategiko ``configure_assets()`` metodoan.

    Aplikazioko irudiak `sprite` modura daude, fitxategi bakarrean
    (``sprite.png``). Horrela irudi bakarra erabiltzen da eta latentzia
    minimizatzen da aldi berean.
    Salbuespena Fancybox `plugin`\aren irudiak dira; hauek bere horretan
    biltegiratzen dira.

``templates/``
    Jinja formatuko HTML txantiloiak.

    Oinarri gisa ``layout.html`` txantiloi nagusia erabiltzen da eta
    gainontzeko moduluen txantiloiak hau heredatzen dute. Horrela, itxura
    uniformea lortzen da, kodea errepikatzeko beharrik gabe.

    Aplikazioaren modulu bakoitzaren txantiloiak direktorio bereiztuetan
    gordetzen dira, salbuespen batzuekin:

    * ``emails/`` direktorioan posta elektroniko bidez bidaliko diren mezuen
      txantiloiak daude.
    * ``errors/`` direktorioan aplikazioaren erroreen ondorioz erakutsiko
      diren txantiloiak daude: HTTP 404, 401, 501... erroreentzako txantiloiak
      dira.
    * ``xml/`` direktorioan XML datu-basean gordeko den XMLa sortzeko
      txantiloi lagungarriak daude.
    * `frontend` moduluaren txantiloiak direktorioaren goiko mailan daude,
      aparteko direktoriorik gabe: ``contact.html``, ``dict.html`` eta
      ``index.html``.

    Azkenik, ``macros/`` direktorioan Jinja txantiloietan erabil daitezkeen
    `macro` edo txantiloi-zati berrerabilgarriak daude. Funtzioak bailiran
    definitzen dira eta HTML kodea itzultzen dute beti.

``translation/``
    Aplikazioaren itzulpen estatikoak :abbr:`PO (Portable Object)` formatuan.

    Hizkuntza bakoitzak bere azpidirektorioan dauka eta ``LC_MESSAGES``
    direktorioan daude itzulpen-fitxategiak (konpilatuak eta konpilatu gabeak).

``views/``
    Aplikazioaren bistak.

    Modulu bakoitzak bere bisten fitxategia dauka. URL eta bisten arteko
    erlazioa bisten definizioan zehazten da. Adibidez::

        from flask import Module

        example = Module(__name__)

        @example.route('/example/<int:id>/')
        def hello(id):
            return "Kaixo mundua, %d naiz!" % (id)

    Aplikazioaren modulu bakoitzeko fitxategi bana dago: ``account.py``,
    ``admin.py``, ``comments.py``...

``xquery/``
    XQuery galderetan inporta daitezkeen moduluak.

    Finean ``term.xqm`` modulua bakarrik dago hemen eta terminoekin lan
    egin eta ataza errepikakorrak sinplifikatzeko funtzio lagungarriak
    ditu.

    XQuery kodean direktorio honetako moduluak inportatu nahi badira,
    TZOSen konfigurazio-fitxategiko ``DBXML_BASE_URI`` gakoaren balioak
    direktorio honetara zuzendu behar du.

    Gero, moduluak XQuery kodean inportatu nahi badira, nahikoa da
    ondorengoa egitea:

    .. code-block:: xqy

        import module namespace term = "http://tzos.net/term" at "term.xqm";

Python / XQuery elkarrekintza
-----------------------------

Python osagaiak besterik ez daude :ref:`vmt-patroia`\n eta, nahiz eta
Flask-DBXMLren laguntza izan DBXMLrekiko kudeaketa sinplifikatzeko, ez dago
modu sinple eta zuzenik XML datuak Python objektuei lotzeko. Horregatik,
Python objektuak sortu ahal izateko XQuery galderen bidez beharrezko
informazio guztia pilatzen da eta formatu jakin bateko `string`\a bueltatzen
da, hortik abiatuta Python objektua sortzeko.

Aplikazioaren zatirik handienean terminoak tartean daudenez, ``Term`` klasea
da erabilpenik handiena duen klasea. Honen `classmethod` bat arduratzen da
(``Term.parse`` zehazki) XQuery bidez pasa dakiokeen `string`\a banatu eta
zatiak atributuei esleitzeaz.

Ekintza hau XQuery galderaren emaitza bati aplikatzeko, Flask-DBXMLren
``as_callback()`` funtzioari pasatzen zaio atributu gisa. Halere, kontuan izan
behar da XQuery galderak ``term:values($tig)`` funtzio berezia itzuli behar
duela, honek sortzen baitu gero ``Term.parse``\k ulertuko duen karaktere-katea.

Adibidez, ondorengo XQuery galderak euskarazko termino publiko guztiak
eskuratuko lituzke:

.. code-block:: xqy

    import module namespace term = "http://tzos.net/term" at "term.xqm";

    for $tig in collection($collection)/martif/text/body/termEntry/langSet[@xml:lang="eu"]/tig
    where term:is_public($tig)
    order by term:sortkey($tig) ascending, term:term($tig) ascending
    return term:values($tig, false())

Eta ``Term`` motako objektu bihurtzeko, ondorengo kodea erabil daiteke
bistatik (demagun galdera ``qs`` aldagaian dagoela)::

    from tzos.extensions import dbxml
    from tzos.models import Term

    terms = dbxml.session.raw_query(qs).as_callback(Term.parse).all()
