# -*- coding: utf-8 -*-
"""
    tzos.fixtures
    ~~~~~~~~~~~~~

    Default application data

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from tzos.extensions import db
from tzos.models import TermOrigin, User

def install():
    """Installs the initial fixtures in the database."""

    create_initial_users()

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
            ["Giza Anatomia I, Giza Anatomia II", "Psikologia", "Neurologia", "Mikrobiologia Medikoa I", "Erradiologia eta Medikuntza Fisiko Orokorrak", "Farmakologia Klinikoa", "Farmakologia Klinikoa", "Biofisika Medikua/Fisiologia Orokorra", "Histologia Orokorra/Histologia Berezia", "Zelulen Biologia"],
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
