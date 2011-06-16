# -*- coding: utf-8 -*-
"""
    tzos.fixtures
    ~~~~~~~~~~~~~

    Default application data

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from tzos.extensions import db
from tzos.models import TermSubject, TermOrigin, Translation, User

def install():
    """Installs the initial fixtures in the database."""

    create_initial_users()
    import_origins()
    import_sfields()

def create_initial_users():
    admin = User()
    admin.username = u'admin'
    admin.password = u'admin'
    admin.email = u'admin@tzos.net'
    admin.role = User.ADMIN
    admin.display_name = u'Default Administrator'

    supervisor = User()
    supervisor.username = u'supervisor'
    supervisor.password = u'supervisor'
    supervisor.email = u'supervisor@tzos.net'
    supervisor.role = User.MODERATOR
    supervisor.display_name = u'Default supervisor'

    member = User()
    member.username = u'member'
    member.password = u'member'
    member.email = u'member@tzos.net'
    member.role = User.MEMBER
    member.display_name = u'Default member'

    db.session.add(admin)
    db.session.add(supervisor)
    db.session.add(member)
    db.session.commit()


ORIGINS = {

    "Zientzia eta Teknologia Fakultatea": {
        "Kimika":
            ["Kimika Fisikoaren Oinarriak", "Kimika Analitikoa", "Kromatografia eta antzeko teknikak", "Kimika Organikoaren Oinarriak", "Materialen Zientziak"],
        "Ingenieritza Kimikoa":
            ["Industri Kimika", "Ingeniaritza Kimikoa"],
        "Geologia":
            ["Hidrogeologia"],
        "Biologia":
            ["Bioestatistika", "Zoologia", "Zoogeografia", "Zitologia eta Histologia", "Entomologia", "Metodo eta teknikak biologia zelularrean"],
        "Matematika":
            ["Topologia", "Kalkulu diferentziala eta integrala-I", "Talde Teoria", "Azterketa funtzionala"],
        "Fisika":
            ["Elektromagnetismoa-II", "Metodo Matematikoak", "Optika"],
    },

    "Farmazia Fakultatea": {
        "Farmazia":
            ["Biokimika", "Fisiopatologia", "Giza Anatomia", "Legeria eta Deontologia", "Fisika", "Fisiologia", "Farmazi Teknologia", "Osasun Publikoa", "Mikrobiologia", "Farmazi Kimika", "Kimika Analitikoa", "Farmakologia I"],
        "Dietetika":
            ["Garapenaren eta Kirolaren Biokimika eta Fisiologia", "Elikadura-Deontologia eta Legeria", "Elikadura-Kalitatea", "Talde Sukaldaritza", "Giza Elikadura", "Osasun Publikoa", "Sistema Immunea eta Elikadura", "Elikagaien Mikrobiologia eta Higienea"],
        "Ingurumen Zientziak":
            ["Ingurumen Kaltearen Balioespena", "Ingurugiro Ingeniaritzaren Oinarriak", "Landare Biologia", "Osasun Publikoa"],
    },

    "Medikuntza eta Odontologia Fakultatea": {
        "Medikuntza":
            ["Giza Anatomia I, Giza Anatomia II", "Psikologia", "Neurologia", "Mikrobiologia Medikoa I", "Erradiologia eta Medikuntza Fisiko Orokorrak", "Farmakologia Klinikoa", "Biofisika Medikua/Fisiologia Orokorra", "Histologia Orokorra/Histologia Berezia", "Zelulen Biologia"],
        "Odontologia":
            ["Giza Anatomia I, Giza Anatomia II", "Fisiologia eta Nutrizioa", "Epidemiologia"],
        "Biokimika":
            ["Immunologia"],
        "Farmazia":
            ["Farmazia Klinikoa eta Farmakoterapia"],
    },

    "Donostiako Enpresa Eskola": {
        "Enpresen Administrazio eta Zuzendaritzako Gradua":
            ["Ekonomiarako Sarrera I: Mikroekonomiaren Oinarriak", "Kontabilitaterako sarrera"],
        "Enpresen Zuzendaritza eta Administrazioko Lizentziatura":
            ["Merkataritza Zuzendaritza: Erabakiak"],
        "Enpresa Zientzien Diplomatura":
            ["Enpresaren Soziologia"],
    },

}


def _import_origins(origin, value=None, parent_id=None):

    if origin:
        to = TermOrigin(name=unicode(origin))

        if parent_id:
            to.parent_id = parent_id

        db.session.add(to)
        db.session.commit()

        print u"New term origin added: {0} ({1}, parent: {2})". \
                format(to.name, to.id, to.parent_id)

    if value:
        if isinstance(value, dict):
            for k, v in value.iteritems():
                _import_origins(k, v, to.id)
        elif isinstance(value, list):
            for v in value:
                _import_origins(v, None, to.id)

def import_origins():
    """Imports initial term origins."""

    for k, v in ORIGINS.iteritems():
        _import_origins(k, v)


SUBJECT_FIELDS = {
    'en': {
        u'11;Logic': [
            u'1101;Application of logic',
            u'1102;Deductive logic',
            u'1103;General logic',
            u'1104;Inductive logic',
            u'1105;Methodology',
            u'1199;Other specialities relating to logic'
            ],

        u'12;Mathematics': [
            u'1201;Algebra',
            u'1202;Analysis and functional analysis',
            u'1203;Computer Sciences',
            u'1204;Geometry',
            u'1205;Number Theory',
            u'1206;Numerical analysis',
            u'1207;Operations research',
            u'1208;Probability',
            u'1209;Statistics',
            u'1210;Topology',
            u'1299;Other mathematical specialities',
            ],

        u'22;Physics': [
            u'2201;Acoustics',
            u'2202;Electro-magnetism',
            u'2203;Electronics',
            u'2204;Fluids (physics of)',
            u'2205;Mechanics',
            u'2206;Molecular physics',
            u'2207;Nuclear physics',
            u'2208;Nucleonics',
            u'2209;Optics',
            u'2210;Physical chemistry',
            u'2211;Solid state physics',
            u'2212;Theoretical physics',
            u'2213;Thermodynamics',
            u'2214;Units and constants',
            u'2290;High energy physics',
            u'2299;Other physical specialities',
            ],

        u'23;Chemistry': [
            u'2301;Analytical chemistry',
            u'2302;Biochemistry',
            u'2303;Inorganic chemistry',
            u'2304;Macromolecular chemistry',
            u'2305;Nuclear chemistry',
            u'2306;Organic chemistry',
            u'2307;Physical chemistry',
            u'2399;Other chemical specialities',
            ],

        u'24;Life sciences': [
                u'2401;Animal Biology (Zoology)',
                u'2402;Anthropology (physical)',
                u'2403;Biochemistry',
                u'2404;Biomathematics',
                u'2405;Biometrics',
                u'2406;Biophysics',
                u'2407;Cell biology',
                u'2408;Ethology',
                u'2409;Genetics',
                u'2410;Human biology',
                u'2411;Human physiology',
                u'2412;Immunology',
                u'2413;Insect biology',
                u'2414;Microbiology',
                u'2415;Molecular biology',
                u'2416;Palaeontology',
                u'2417;Plant Biology (Botany)',
                u'2418;Radiobiology',
                u'2419;Symbiosis',
                u'2420;Virology',
                u'2490;Neurosciences',
                u'2499;Other biological specialities',
                ],

        u'25;Earth and Space Sciences': [
                u'2501;Atmospheric sciences',
                u'2502;Climatology',
                u'2503;Geochemistry',
                u'2504;Geodesy',
                u'2505;Geography',
                u'2506;Geology',
                u'2507;Geophysics',
                u'2508;Hydrology',
                u'2509;Meteorology',
                u'2510;Oceanography',
                u'2511;Soil Science',
                u'2512;Space Sciences',
                u'2599;Other Earch, Space or Environmental specialities',
                ],

        u'32;Medical Sciences': [
                u'3201;Clinical sciences',
                u'3202;Epidemiology',
                u'3203;Forensic medicine',
                u'3204;Occupational medicine',
                u'3205;Internal medicine',
                u'3206;Nutritional sciences',
                u'3207;Pathology',
                u'3208;Pharmacodynamics',
                u'3209;Pharmacology',
                u'3210;Preventive medicine',
                u'3211;Psychiatry',
                u'3212;Public health',
                u'3213;Surgery',
                u'3214;Toxicology',
                u'3299;Other medical specialities',
                ],

        u'33;Technological Sciences': [
                u'3301;Aeronautical technology and engineering',
                u'3302;Biochemical technology',
                u'3303;Chemical technology and engineering',
                u'3304;Computer technology',
                u'3305;Construction technology',
                u'3306;Electrical technology and engineering',
                u'3307;Electronic technology',
                u'3308;Environmental technology and engineering',
                u'3309;Food technology',
                u'3310;Industrial technology',
                u'3311;Instrumentation technology',
                u'3312;Materials technology',
                u'3313;Mechanical engineering and technology',
                u'3314;Medical technology',
                u'3315;Metallurgical technology',
                u'3316;Metal products technology',
                u'3317;Motor vehicle technology',
                u'3318;Mining technology',
                u'3319;Naval techonology',
                u'3320;Nuclear technology',
                u'3321;Petroleum and coal technology',
                u'3322;Power technology',
                u'3323;Railway technology',
                u'3324;Space technology',
                u'3325;Telecommunications technology',
                u'3326;Textile technology',
                u'3327;Transportation systems technology',
                u'3328;Unit operations technology',
                u'3329;Urban planning',
                u'3399;Other technological specialities',
                ],

        u'51;Anthropology': [
                u'5101;Cultural anthropology',
                u'5102;Ethnography and Ethnology',
                u'5103;Social anthropology',
                u'5199;Other anthropological specialities',
                ],

        u'53;Economic Sciences': [
                u'5301;Domestic fiscal policy and public finance',
                u'5302;Econometrics',
                u'5303;Economic accounting',
                u'5304;Economic activity',
                u'5305;Economic systems',
                u'5306;Economics of technological change',
                u'5307;Economic theory',
                u'5308;General economics',
                u'5309;Industrial organization and public policy',
                u'5310;International economics',
                u'5311;Organization and management of enterprises',
                u'5312;Sectorial economics',
                u'5399;Other economics specialities',
                ],

        u'56;Juridical Sciences & Law': [
                u'5601;Canon law',
                u'5602;General theory and methods',
                u'5603;International law',
                u'5604;Legal organization',
                u'5605;National law and legislation',
                u'5699;Other juridical specialities',
                ],

        u'57;Linguistics': [
                u'5701;Applied linguistics',
                u'5702;Diachronic linguistics',
                u'5703;Linguistic geography',
                u'5704;Linguistic theory',
                u'5705;Synchronic linguistics',
                u'5799;Other linguistic specialities',
                ],

        u'58;Pedagogy': [
                u'5801;Educational theory and methods',
                u'5802;Organization and planning of education',
                u'5803;Teacher training and employment',
                u'5899;Other pedagogical specialities',
                ],

        u'61;Psychology': [
                u'6101;Abnormal psychology',
                u'6102;Adolescent and child psychology',
                u'6103;Counselling and guidance',
                u'6104;Educational psichology',
                u'6105;Evaluation and measurement in psychology',
                u'6106;Experimental psychology',
                u'6107;General psychology',
                u'6108;Geriatric psychology',
                u'6109;Occupational and personnel psychology',
                u'6110;Parapsychology',
                u'6111;Personality',
                u'6112;Psychological study of social issues',
                u'6113;Psychopharmacology',
                u'6114;Social psychology',
                u'6199;Other psychological specialities',
                ],

        u'71;Ethics': [
                u'7101;Classical ethics',
                u'7102;Ethics of individuals',
                u'7103;Group ethics',
                u'7104;Prospective ethics',
                u'7199;Other specialities relating to ethics',
                ],

        u'72;Philosophy': [
                u'7201;Philosophy of knowledge',
                u'7202;Philosophical anthropology',
                u'7203;General philosophy',
                u'7204;Philosophical systems',
                u'7205;Philosophy of science',
                u'7206;Philosophy of nature',
                u'7207;Social philosophy',
                u'7208;Philosophical doctrines',
                u'7299;Other philosophical specialities',
                ],

    },
}



def _import_sfields(field, locale, value=None, parent_id=None):

    if field:
        code, text = field.split(u';', 1)

        # First store subject field
        sf = TermSubject()
        sf.code = code

        if parent_id:
            sf.parent_id = parent_id

        db.session.add(sf)
        db.session.commit()

        # Add translation
        trans = Translation()
        trans.id = sf.code
        trans.locale = locale
        trans.text = text

        db.session.add(trans)
        db.session.commit()

        # Finally set translation id
        sf.trans_id = trans.auto_id

        db.session.add(sf)
        db.session.commit()

        print u"New subject field added: {0} ({1}, parent: {2})". \
                format(trans.text, sf.code, sf.parent_id)

    if value:
        if isinstance(value, dict):
            for k, v in value.iteritems():
                _import_sfields(k, locale, v, sf.code)
        elif isinstance(value, list):
            for v in value:
                _import_sfields(v, locale, None, sf.code)


def import_sfields():
    """Imports initial subject fields."""

    for locale, items in SUBJECT_FIELDS.iteritems():
        for k, v in items.iteritems():
            print "Importing subject fields for", locale
            _import_sfields(k, locale, v)
