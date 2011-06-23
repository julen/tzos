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

    corrector = User()
    corrector.username = u'corrector'
    corrector.password = u'corrector'
    corrector.email = u'corrector@tzos.net'
    corrector.role = User.CORRECTOR
    corrector.display_name = u'Default corrector'

    member = User()
    member.username = u'member'
    member.password = u'member'
    member.email = u'member@tzos.net'
    member.role = User.MEMBER
    member.display_name = u'Default member'

    db.session.add(admin)
    db.session.add(supervisor)
    db.session.add(corrector)
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


SUBJECT_FIELDS = [
        (11, {u'en': u'Logic',
              u'eu': u'Logika'}, [
            (1101, {u'en': u'Application of logic',
                    u'eu': u'Logikaren aplikazioak'}),
            (1102, {u'en': u'Deductive logic',
                    u'eu': u'Logika deduktiboa'}),
            (1103, {u'en': u'General logic',
                    u'eu': u'Logika orokorra'}),
            (1104, {u'en': u'Inductive logic',
                    u'eu': u'Logika induktiboa'}),
            (1105, {u'en': u'Methodology',
                    u'eu': u'Metodologia'}),
            (1199, {u'en': u'Other specialities relating to logic',
                    u'eu': u'Logikarekin lotutako beste espezialitate batzuk'}),
            ]),

        (12, {u'en': u'Mathematics',
              u'eu': u'Matematika'}, [
            (1201, {u'en': u'Algebra',
                    u'eu': u'Aljebra'}),
            (1202, {u'en': u'Analysis and functional analysis',
                    u'eu': u'Analisia eta Analisi Funtzionala'}),
            (1203, {u'en': u'Computer Sciences',
                    u'eu': u'Konputazio Zientziak'}),
            (1204, {u'en': u'Geometry',
                    u'eu': u'Geometria'}),
            (1205, {u'en': u'Number Theory',
                    u'eu': u'Zenbaki Teoria'}),
            (1206, {u'en': u'Numerical analysis',
                    u'eu': u'Zenbakizko Analisia'}),
            (1207, {u'en': u'Operations research',
                    u'eu': u'Ikerkuntza Eragilea'}),
            (1208, {u'en': u'Probability',
                    u'eu': u'Probabilitatea'}),
            (1209, {u'en': u'Statistics',
                    u'eu': u'Estatistika'}),
            (1210, {u'en': u'Topology',
                    u'eu': u'Topologia'}),
            (1299, {u'en': u'Other mathematical specialities',
                    u'eu': u'Matematikaren bestelako espezialitateak'}),
            ]),

        (22, {u'en': u'Physics',
              u'eu': u'Fisika'}, [
            (2201, {u'en': u'Acoustics',
                    u'eu': u'Akustika'}),
            (2202, {u'en': u'Electro-magnetism',
                    u'eu': u'Elektromagnetismoa'}),
            (2203, {u'en': u'Electronics',
                    u'eu': u'Elektronika'}),
            (2204, {u'en': u'Fluids (physics of)',
                    u'eu': u'Fluidoen Fisika'}),
            (2205, {u'en': u'Mechanics',
                    u'eu': u'Mekanika'}),
            (2206, {u'en': u'Molecular physics',
                    u'eu': u'Fisika Molekularra'}),
            (2207, {u'en': u'Nuclear physics',
                    u'eu': u'Fisika Atomiko eta Nuklearra'}),
            (2208, {u'en': u'Nucleonics',
                    u'eu': u'Nukleonika'}),
            (2209, {u'en': u'Optics',
                    u'eu': u'Optika'}),
            (2210, {u'en': u'Physical chemistry',
                    u'eu': u'Kimika Fisikoa'}),
            (2211, {u'en': u'Solid state physics',
                    u'eu': u'Egoera Solidoaren Fisika'}),
            (2212, {u'en': u'Theoretical physics',
                    u'eu': u'Fisika Teorikoa'}),
            (2213, {u'en': u'Thermodynamics',
                    u'eu': u'Termodinamika'}),
            (2214, {u'en': u'Units and constants',
                    u'eu': u'Unitateak eta Konstanteak'}),
            (2290, {u'en': u'High energy physics',
                    u'eu': u'Energia Altuko Fisika'}),
            (2299, {u'en': u'Other physical specialities',
                    u'eu': u'Fisikaren bestelako espezialitateak'}),
            ]),

        (23, {u'en': u'Chemistry',
              u'eu': u'Kimika'}, [
            (2301, {u'en': u'Analytical chemistry',
                    u'eu': u'Kimika Analitikoa'}),
            (2302, {u'en': u'Biochemistry',
                    u'eu': u'Biokimika'}),
            (2303, {u'en': u'Inorganic chemistry',
                    u'eu': u'Kimika Inorganikoa'}),
            (2304, {u'en': u'Macromolecular chemistry',
                    u'eu': u'Makromolekulen Kimika'}),
            (2305, {u'en': u'Nuclear chemistry',
                    u'eu': u'Kimika Nuklearra'}),
            (2306, {u'en': u'Organic chemistry',
                    u'eu': u'Kimika Organikoa'}),
            (2307, {u'en': u'Physical chemistry',
                    u'eu': u'Kimika Fisikoa'}),
            (2399, {u'en': u'Other chemical specialities',
                    u'eu': u'Kimikaren bestelako espezialitateak'}),
            ]),

        (24, {u'en': u'Life sciences',
              u'eu': u'Biziaren Zientziak'}, [
            (2401, {u'en': u'Animal Biology (Zoology)',
                    u'eu': u'Animalien Biologia (Zoologia)'}),
            (2402, {u'en': u'Anthropology (physical)',
                    u'eu': u'Antropologia (fisikoa)'}),
            (2403, {u'en': u'Biochemistry',
                    u'eu': u'Biokimika'}),
            (2404, {u'en': u'Biomathematics',
                    u'eu': u'Biomatematika'}),
            (2405, {u'en': u'Biometrics',
                    u'eu': u'Biometria'}),
            (2406, {u'en': u'Biophysics',
                    u'eu': u'Biofisika'}),
            (2407, {u'en': u'Cell biology',
                    u'eu': u'Biologia Zelularra'}),
            (2408, {u'en': u'Ethology',
                    u'eu': u'Etologia'}),
            (2409, {u'en': u'Genetics',
                    u'eu': u'Genetika'}),
            (2410, {u'en': u'Human biology',
                    u'eu': u'Giza Biologia'}),
            (2411, {u'en': u'Human physiology',
                    u'eu': u'Giza Fisiologia'}),
            (2412, {u'en': u'Immunology',
                    u'eu': u'Immunologia'}),
            (2413, {u'en': u'Insect biology',
                    u'eu': u'Intsektuen Biologia (Entomologia)'}),
            (2414, {u'en': u'Microbiology',
                    u'eu': u'Mikrobiologia'}),
            (2415, {u'en': u'Molecular biology',
                    u'eu': u'Biologia Molekularra'}),
            (2416, {u'en': u'Palaeontology',
                    u'eu': u'Paleontologia'}),
            (2417, {u'en': u'Plant Biology (Botany)',
                    u'eu': u'Landareen Biologia (Botanika)'}),
            (2418, {u'en': u'Radiobiology',
                    u'eu': u'Erradiobiologia'}),
            (2419, {u'en': u'Symbiosis',
                    u'eu': u'Sinbiosia'}),
            (2420, {u'en': u'Virology',
                    u'eu': u'Birologia'}),
            (2490, {u'en': u'Neurosciences',
                    u'eu': u'Neurozientziak'}),
            (2499, {u'en': u'Other biological specialities',
                    u'eu': u'Biologiaren bestelako espezialitateak'}),
            ]),

        (25, {u'en': u'Earth and Space Sciences',
              u'eu': u'Lurraren eta Espazioaren Zientziak'}, [
            (2501, {u'en': u'Atmospheric sciences',
                    u'eu': u'Atmosferaren Zientziak'}),
            (2502, {u'en': u'Climatology',
                    u'eu': u'Klimatologia'}),
            (2503, {u'en': u'Geochemistry',
                    u'eu': u'Geokimika'}),
            (2504, {u'en': u'Geodesy',
                    u'eu': u'Geodesia'}),
            (2505, {u'en': u'Geography',
                    u'eu': u'Geografia'}),
            (2506, {u'en': u'Geology',
                    u'eu': u'Geologia'}),
            (2507, {u'en': u'Geophysics',
                    u'eu': u'Geofisika'}),
            (2508, {u'en': u'Hydrology',
                    u'eu': u'Hidrologia'}),
            (2509, {u'en': u'Meteorology',
                    u'eu': u'Meteorologia'}),
            (2510, {u'en': u'Oceanography',
                    u'eu': u'Ozeanografia'}),
            (2511, {u'en': u'Soil Science',
                    u'eu': u'Lurzoruaren Zientziak (Edafologia)'}),
            (2512, {u'en': u'Space Sciences',
                    u'eu': u'Espazioaren Zientziak'}),
            (2599, {u'en': u'Other Earth, Space or Environmental specialities',
                    u'eu': u'Lurraren eta Espazioaren edo INgurunearen bestelako espezialitateak'}),
            ]),

        (32, {u'en': u'Medical Sciences',
              u'eu': u'Osasun Zientziak'}, [
            (3201, {u'en': u'Clinical sciences',
                    u'eu': u'Zientzia Klinikoak'}),
            (3202, {u'en': u'Epidemiology',
                    u'eu': u'Epidemiologia'}),
            (3203, {u'en': u'Forensic medicine',
                    u'eu': u'Medikuntza Forensea'}),
            (3204, {u'en': u'Occupational medicine',
                    u'eu': u'Lan Medikuntza'}),
            (3205, {u'en': u'Internal medicine',
                    u'eu': u'Barne Medikuntza'}),
            (3206, {u'en': u'Nutritional sciences',
                    u'eu': u'Elikadura Zientziak'}),
            (3207, {u'en': u'Pathology',
                    u'eu': u'Patologia'}),
            (3208, {u'en': u'Pharmacodynamics',
                    u'eu': u'Farmakodinamika'}),
            (3209, {u'en': u'Pharmacology',
                    u'eu': u'Farmakologia'}),
            (3210, {u'en': u'Preventive medicine',
                    u'eu': u'Prebentzio medikuntza'}),
            (3211, {u'en': u'Psychiatry',
                    u'eu': u'Psikiatria'}),
            (3212, {u'en': u'Public health',
                    u'eu': u'Osasun Publikoa'}),
            (3213, {u'en': u'Surgery',
                    u'eu': u'Kirurgia'}),
            (3214, {u'en': u'Toxicology',
                    u'eu': u'Toxikologia'}),
            (3299, {u'en': u'Other medical specialities',
                    u'eu': u'Medikuntzaren bestelako espezialitateak'}),
            ]),

        (33, {u'en': u'Technological Sciences',
              u'eu': u'Zientzia Teknologikoak'}, [
            (3301, {u'en': u'Aeronautical technology and engineering',
                    u'eu': u'Ingeniaritza eta Teknologia Aeronautikoak'}),
            (3302, {u'en': u'Biochemical technology',
                    u'eu': u'Teknologia Biokimikoa'}),
            (3303, {u'en': u'Chemical technology and engineering',
                    u'eu': u'Ingeniaritza eta Teknologia Kimikoak'}),
            (3304, {u'en': u'Computer technology',
                    u'eu': u'Ordenagailuen Teknologia'}),
            (3305, {u'en': u'Construction technology',
                    u'eu': u'Eraikuntzaren Teknologia'}),
            (3306, {u'en': u'Electrical technology and engineering',
                    u'eu': u'Ingeniaritza eta Teknologia Elektrikoak'}),
            (3307, {u'en': u'Electronic technology',
                    u'eu': u'Teknologia Elektronikoa'}),
            (3308, {u'en': u'Environmental technology and engineering',
                    u'eu': u'Ingurumenaren Ingeniaritza eta Teknologia'}),
            (3309, {u'en': u'Food technology',
                    u'eu': u'Elikagaien Teknologia'}),
            (3310, {u'en': u'Industrial technology',
                    u'eu': u'Industria Teknologia'}),
            (3311, {u'en': u'Instrumentation technology',
                    u'eu': u'Instrumentazio Teknologia'}),
            (3312, {u'en': u'Materials technology',
                    u'eu': u'Materialen Teknologia'}),
            (3313, {u'en': u'Mechanical engineering and technology',
                    u'eu': u'Teknologia eta Ingeniaritza Mekanikoak'}),
            (3314, {u'en': u'Medical technology',
                    u'eu': u'Medikuntza Teknologia'}),
            (3315, {u'en': u'Metallurgical technology',
                    u'eu': u'Metalurgiaren Teknologia'}),
            (3316, {u'en': u'Metal products technology',
                    u'eu': u'Produktu Metalikoen Teknologia'}),
            (3317, {u'en': u'Motor vehicle technology',
                    u'eu': u'Ibilgailu Motordunen Teknologia'}),
            (3318, {u'en': u'Mining technology',
                    u'eu': u'Mehatze Teknologia'}),
            (3319, {u'en': u'Naval techonology',
                    u'eu': u'Ontzigintzaren Teknologia'}),
            (3320, {u'en': u'Nuclear technology',
                    u'eu': u'Teknologia Nuklearra'}),
            (3321, {u'en': u'Petroleum and coal technology',
                    u'eu': u'Ikatzaren eta Petrolioaren Teknologia'}),
            (3322, {u'en': u'Power technology',
                    u'eu': u'Energiaren Teknologia'}),
            (3323, {u'en': u'Railway technology',
                    u'eu': u'Tren Sistemen Teknologia'}),
            (3324, {u'en': u'Space technology',
                    u'eu': u'Espazioaren Teknologia'}),
            (3325, {u'en': u'Telecommunications technology',
                    u'eu': u'Telekomunikazioen Teknologia'}),
            (3326, {u'en': u'Textile technology',
                    u'eu': u'Ehungintzaren Teknologia'}),
            (3327, {u'en': u'Transportation systems technology',
                    u'eu': u'Garraio Sistemen Teknologia'}),
            (3328, {u'en': u'Unit operations technology',
                    u'eu': u'Prozesu Teknologikoak'}),
            (3329, {u'en': u'Urban planning',
                    u'eu': u'Hirigintza'}),
            (3399, {u'en': u'Other technological specialities',
                    u'eu': u'Teknologiaren bestelako espezialitateak'}),
            ]),

        (51, {u'en': u'Anthropology',
              u'eu': u'Antropologia'}, [
            (5101, {u'en': u'Cultural anthropology',
                    u'eu': u'Kulturaren Antropologia'}),
            (5102, {u'en': u'Ethnography and Ethnology',
                    u'eu': u'Etnografia eta Etnologia'}),
            (5103, {u'en': u'Social anthropology',
                    u'eu': u'Gizarte Antropologia'}),
            (5199, {u'en': u'Other anthropological specialities',
                    u'eu': u'Antropologiaren bestelako espezialitateak'}),
            ]),

        (53, {u'en': u'Economic Sciences',
              u'eu': u'Ekonomia Zientziak'}, [
            (5301, {u'en': u'Domestic fiscal policy and public finance',
                    u'eu': u'Zerga Politika eta Ogasun Publiko Nazionalak'}),
            (5302, {u'en': u'Econometrics',
                    u'eu': u'Ekonometria'}),
            (5303, {u'en': u'Economic accounting',
                    u'eu': u'Ekonomia Kontabilitatea'}),
            (5304, {u'en': u'Economic activity',
                    u'eu': u'Ekonomia Jarduerak'}),
            (5305, {u'en': u'Economic systems',
                    u'eu': u'Ekonomia Sistemak'}),
            (5306, {u'en': u'Economics of technological change',
                    u'eu': u'Aldaketa Teknologikoaren Ekonomia'}),
            (5307, {u'en': u'Economic theory',
                    u'eu': u'Ekonomiaren Teoria'}),
            (5308, {u'en': u'General economics',
                    u'eu': u'Ekonomia Orokorra'}),
            (5309, {u'en': u'Industrial organization and public policy',
                    u'eu': u'Industria Antolakuntza eta Zuzendaritza'}),
            (5310, {u'en': u'International economics',
                    u'eu': u'Nazioarteko Ekonomia'}),
            (5311, {u'en': u'Organization and management of enterprises',
                    u'eu': u'Enpresen Antolakuntza eta Zuzendaritza'}),
            (5312, {u'en': u'Sectorial economics',
                    u'eu': u'Ekonomia Sektoriala'}),
            (5399, {u'en': u'Other economics specialities',
                    u'eu': u'Ekonomiaren bestelako espezialitateak'}),
            ]),

        (56, {u'en': u'Juridical Sciences & Law',
              u'eu': u'Zientzia Juridikoak eta Zuzenbidea'}, [
            (5601, {u'en': u'Canon law',
                    u'eu': u'Zuzenbide Kanonikoa'}),
            (5602, {u'en': u'General theory and methods',
                    u'eu': u'Teoria eta metodo Orokorrak'}),
            (5603, {u'en': u'International law',
                    u'eu': u'Nazioarteko Zuzenbidea'}),
            (5604, {u'en': u'Legal organization',
                    u'eu': u'Antolakuntza Juridikoa'}),
            (5605, {u'en': u'National law and legislation',
                    u'eu': u'Legegintza eta Lege Nazionalak'}),
            (5699, {u'en': u'Other juridical specialities',
                    u'eu': u'Bestelako espezialitate Juridikoak'}),
            ]),

        (57, {u'en': u'Linguistics',
              u'eu': u'Hizkuntzalaritza'}, [
            (5701, {u'en': u'Applied linguistics',
                    u'eu': u'Hizkuntzalaritza Aplikatua'}),
            (5702, {u'en': u'Diachronic linguistics',
                    u'eu': u'Hizkuntzalaritza Diakronikoa'}),
            (5703, {u'en': u'Linguistic geography',
                    u'eu': u'Geografia Linguistikoa'}),
            (5704, {u'en': u'Linguistic theory',
                    u'eu': u'Teoria Linguistikoa'}),
            (5705, {u'en': u'Synchronic linguistics',
                    u'eu': u'Hizkuntzalaritza Sinkronikoa'}),
            (5799, {u'en': u'Other linguistic specialities',
                    u'eu': u'Hizkuntzalaritzaren bestelako espezialitateak'}),
            ]),

        (58, {u'en': u'Pedagogy',
              u'eu': u'Pedagogia'}, [
            (5801, {u'en': u'Educational theory and methods',
                    u'eu': u'Hezkuntza Teoria eta Metodoak'}),
            (5802, {u'en': u'Organization and planning of education',
                    u'eu': u'Hezkuntzaren Antolakuntza eta Planifikazioa'}),
            (5803, {u'en': u'Teacher training and employment',
                    u'eu': u'Irakasleen Prestakuntza eta Enplegua'}),
            (5899, {u'en': u'Other pedagogical specialities',
                    u'eu': u'Pedagogiaren bestelako espezialitateak'}),
            ]),

        (61, {u'en': u'Psychology',
              u'eu': u'Psikologia'}, [
            (6101, {u'en': u'Abnormal psychology',
                u'eu': u'Patologia'}),
            (6102, {u'en': u'Adolescent and child psychology',
                u'eu': u'Haurren eta Nerabeen Psikologia'}),
            (6103, {u'en': u'Counselling and guidance',
                u'eu': u'Aholkularitza eta Laguntza'}),
            (6104, {u'en': u'Educational psychology',
                u'eu': u'Psikopedagogia'}),
            (6105, {u'en': u'Evaluation and measurement in psychology',
                u'eu': u'Ebaluazioa eta Diagnostikoa Psikologian'}),
            (6106, {u'en': u'Experimental psychology',
                u'eu': u'Psikologia Esperimentala'}),
            (6107, {u'en': u'General psychology',
                u'eu': u'Psikologia Orokorra'}),
            (6108, {u'en': u'Geriatric psychology',
                u'eu': u'Zahartzaroaren Psikologia'}),
            (6109, {u'en': u'Occupational and personnel psychology',
                u'eu': u'Industria Psikologia'}),
            (6110, {u'en': u'Parapsychology',
                u'eu': u'Parapsikologia'}),
            (6111, {u'en': u'Personality',
                u'eu': u'Nortasuna'}),
            (6112, {u'en': u'Psychological study of social issues',
                u'eu': u'Gizarte Gaien Azterketa Psikologikoa'}),
            (6113, {u'en': u'Psychopharmacology',
                u'eu': u'Psikofarmakologia'}),
            (6114, {u'en': u'Social psychology',
                u'eu': u'Gizarte Psikologia'}),
            (6199, {u'en': u'Other psychological specialities',
                u'eu': u'Psikologiaren bestelako espezialitateak'}),
            ]),

        (71, {u'en': u'Ethics',
              u'eu': u'Etika'}, [
            (7101, {u'en': u'Classical ethics',
                    u'eu': u'Etika Klasikoa'}),
            (7102, {u'en': u'Ethics of individuals',
                    u'eu': u'Gizabanakoen Etika'}),
            (7103, {u'en': u'Group ethics',
                    u'eu': u'Talde Etika'}),
            (7104, {u'en': u'Prospective ethics',
                    u'eu': u'Etika Prospektiboa'}),
            (7199, {u'en': u'Other specialities relating to ethics',
                    u'eu': u'Etikaren bestelako espezialitateak'}),
            ]),

        (72, {u'en': u'Philosophy',
              u'eu': u'Filosofia'}, [
            (7201, {u'en': u'Philosophy of knowledge',
                    u'eu': u'Ezagutzaren Filosofia'}),
            (7202, {u'en': u'Philosophical anthropology',
                    u'eu': u'Antropologia Filosofikoa'}),
            (7203, {u'en': u'General philosophy',
                    u'eu': u'Filosofia Orokorra'}),
            (7204, {u'en': u'Philosophical systems',
                    u'eu': u'Sistema Filosofikoak'}),
            (7205, {u'en': u'Philosophy of science',
                    u'eu': u'Zientziaren Filosofia'}),
            (7206, {u'en': u'Philosophy of nature',
                    u'eu': u'Naturaren Filosofia'}),
            (7207, {u'en': u'Social philosophy',
                    u'eu': u'Gizarte Filosofia'}),
            (7208, {u'en': u'Philosophical doctrines',
                    u'eu': u'Doktrina Filosofikoak'}),
            (7299, {u'en': u'Other philosophical specialities',
                    u'eu': u'Filosofiaren bestelako espezialitateak'}),
            ]),

]



def _import_sfields(field, parent_id=None):

    if field and isinstance(field, tuple):
        code = field[0]
        translations = field[1]
        try:
            rest = field[2]
        except IndexError:
            rest = None

        print u"Adding subject field: {0}, parent: {1}". \
                format(code, parent_id)

        for locale, text in translations.iteritems():

            trans = Translation()
            trans.id = code
            trans.locale = locale
            trans.text = text

            db.session.add(trans)
            db.session.commit()

            print u"Translation added: {0} ({1})". \
                    format(text, locale)


            # Now we can store the subject field
            sf = TermSubject()
            sf.code = code
            sf.trans_id = trans.auto_id

            if parent_id:
                sf.parent_id = parent_id

            db.session.add(sf)
            db.session.commit()

        # If there's more to import, go ahead
        if rest and isinstance(rest, list):
            for field in rest:
                _import_sfields(field, sf.code)


def import_sfields():
    """Imports initial subject fields."""

    for field in SUBJECT_FIELDS:
        _import_sfields(field)
