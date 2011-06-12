# -*- coding: utf-8 -*-
"""
    tzos.models.terms
    ~~~~~~~~~~~~~~~~~

    Term models.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from dateutil.parser import parse
from time import strftime

from flask import g, Markup, render_template, url_for

from flaskext.babel import gettext as _

from werkzeug import cached_property

from tzos.extensions import db, dbxml
from tzos.models.users import User


class TermOrigin(db.Model):
    __tablename__ = 'origins'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.UnicodeText)

    parent_id = db.Column(db.Integer,
                          db.ForeignKey('origins.id', ondelete='CASCADE'))

    parent = db.relation('TermOrigin', remote_side=[id], backref='children')


class TermChange(object):

    @classmethod
    def parse(cls, value):
        """Parses a string into a TermChange object"""

        parts = value.split(u"|||")

        try:
            term_id = parts[0]
            term = parts[1]
            change_type = parts[2]
            date = parts[3]
            username = parts[4]
        except IndexError:
            return None

        return TermChange(term_id, term, change_type, date, username)


    def __init__(self, term_id, term, change_type, date, username):
        self._term_id = term_id
        self._term = term
        self._date = date
        self._username = username

        self.type = change_type

    @cached_property
    def term(self):
        return Term(self._term_id, self._term)

    @cached_property
    def author(self):
        return User.query.filter_by(username=self._username).first()

    @cached_property
    def description(self):
        desc_map = {
                'importation': _(u'Imported term <a href="%(term_url)s">%(term)s</a>.',
                    term_url=self.term.url,
                    term=self.term.term),
                'input': _(u'Added term <a href="%(term_url)s">%(term)s</a>.',
                    term_url=self.term.url,
                    term=self.term.term),
                'modification': _(u'Edited term <a href="%(term_url)s">%(term)s</a>.',
                    term_url=self.term.url,
                    term=self.term.term),
                }

        try:
            return Markup(desc_map[self.type])
        except KeyError:
            return _(u'No activity details available.')

    @cached_property
    def date(self):
        return parse(self._date)


class Term(object):

    def __init__(self, id=None, term=None):
        if id:
            self.term_id = id

        if term:
            self.term = term

        self._subject_field = []
        self._synonyms = []
        self._translations = {}

    @property
    def id(self):
        if hasattr(self, 'term_id'):
            return self.term_id

        # FIXME: check subjectField too
        qs = u'/martif/text/body/termEntry/langSet[@xml:lang="{0}"]/tig[term/string()="{1}"]/data(@id)'.format(self.language, self.term)
        result = dbxml.session.query(qs, document='tzos.xml').as_str().first()

        if result:
            self.term_id = result

        return result

    @cached_property
    def concept_id(self):

        # FIXME: check subjectField too
        qs = u'/martif/text/body/termEntry[langSet[@xml:lang="{0}"] and langSet/tig/term/string()="{1}"]/data(@id)'.format(self.language, self.term)
        return dbxml.session.query(qs, document='tzos.xml').as_str().first()

    @cached_property
    def concept_origin_display(self):

        origin = TermOrigin.query.get(self.concept_origin)
        origin_list = [origin.name]

        while origin.parent_id:
            origin = TermOrigin.query.get(origin.parent_id)
            origin_list.insert(0, origin.name)

        return Markup(u' » '.join(origin_list))

    @cached_property
    def originating_person_display(self):

        display_name = self.originating_person

        if display_name.startswith(u"_"):
            username = display_name[1:]
            user = User.query.filter_by(username=username).first()

            if user:
                if user.display_name:
                    dn = user.display_name
                else:
                    dn = user.username

                html = Markup(u'<a href="{0}">{1}</a>'.format(user.url, dn))
                display_name = html

        return display_name


    def _get_subject_field(self):
        return self._subject_field

    def _set_subject_field(self, value):
        if isinstance(value, list):
            self._subject_field = value
        else:
            for part in value.split(u";"):
                if part:
                    self._subject_field.append(part)

    subject_field = property(_get_subject_field, _set_subject_field)

    def _get_synonyms(self):
        return self._synonyms

    def _set_synonyms(self, value):
        for part in value.split(u";;;"):
            if part:
                id, term = part.split(u";", 1)
                syn = Term(id=id, term=term)
                self._synonyms.append(syn)

    synonyms = property(_get_synonyms, _set_synonyms)

    def _get_translations(self):
        return self._translations

    def _set_translations(self, value):
        for part in value.split(u";;;"):
            if part:
                lang, id, term = part.split(u";", 2)
                trans = Term(id=id, term=term)
                self._translations.setdefault(lang, []).append(trans)

    translations = property(_get_translations, _set_translations)

    def _url(self, _external=False):
        return url_for('terms.detail',
                       id=self.id,
                       _external=_external)

    @cached_property
    def url(self):
        return self._url()

    @cached_property
    def permalink(self):
        return self._url(True)

    def exists(self):
        """Returns True if the current term exists in the DB."""

        return self.id is not None

    def has_langset(self, langcode):
        """Returns True if the current term has a langSet for langcode."""
        qs = u'/martif/text/body/termEntry[@id="{0}"]/langSet[@xml:lang="{1}"]'. \
            format(self.concept_id, langcode)
        result = dbxml.session.query(qs, document='tzos.xml').as_str().first()

        return result is not None

    def is_public(self):
        """Returns True if the current term has an elementWorkingStatus
        with a value of `workingElement` or higher."""

        if not hasattr(self, 'working_status'):
            qs = u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="elementWorkingStatus"]/string()'.format(self.id)
            self.working_status = dbxml.session.query(qs).as_str().first()
        if not self.working_status:
            return False

        return self.working_status != u"starterElement" and \
               self.working_status != u"importedElement" and \
               self.working_status != u"archiveElement"

    def is_consolidated(self):
        """Returns True if the current term has an elementWorkingStatus
        with a value of `consolidatedElement` or higher."""

        if not hasattr(self, 'working_status'):
            qs = u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="elementWorkingStatus"]/string()'.format(self.id)
            self.working_status = dbxml.session.query(qs).as_str().first()
        if not self.working_status:
            return False

        return self.working_status != u"starterElement" and \
               self.working_status != u"importedElement" and \
               self.working_status != u"workingElement"

    def is_mine(self):
        """Returns True if the term's `origintatingPerson` is the same
        as the user who committed the term."""

        if not hasattr(self, 'originating_person'):
            qs = u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="originatingPerson"]/string()'.format(self.id)
            self.originating_person = dbxml.session.query(qs).as_str().first()
        if self.originating_person is None:
            return False

        return self.originating_person == self.owner()

    # FIXME: optimize this with a property
    def owner(self):
        """Returns the term owner, ie the username who first inserted
        this term."""

        qs = u'//tig[@id="{0}" and (transacGrp/transac[@type="transactionType"]/string()="origination" or transacGrp/transac[@type="transactionType"]/string()="importation" or transacGrp/transac[@type="transactionType"]/string()="input")]/transacGrp/transacNote[@type="responsibility"]/string()'.format(self.id)
        result = dbxml.session.query(qs).as_str().first()

        if result is not None:
            return result

        return u""

    def populate(self):
        """Populates current term's fields by querying fields by id."""

        fields = [
            ('term', u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/term/string()'),
            ('language', u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../data(@xml:lang)'),
            ('concept_origin',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="conceptOrigin"]/string()'),
            ('subject_field',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../../descrip[@type="subjectField"]/string()'),
            ('working_status',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="elementWorkingStatus"]/string()'),
            ('originating_person',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="originatingPerson"]/string()'),
            ('definition',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../descrip[@type="definition"]/string()'),
            ('context',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/descrip[@type="context"]/string()'),
            ('example',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/descrip[@type="example"]/string()'),
            ('explanation',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/descrip[@type="explanation"]/string()'),
            ('entry_source',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="entrySource"]/string()'),
            ('cross_reference',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/ref[@type="crossReference"]/string()'),
            ('product_subset',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="productSubset"]/string()'),

            ('normative_authorization',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/termNote[@type="normativeAuthorization"]/string()'),
            ('normative_authorization_org',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/termNote[@type="normativeAuthorization"]/data(@target)'),
            ('subordinate_concept_generic',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../../descrip[@type="subordinateConceptGeneric"]/string()'),
            ('superordinate_concept_generic',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../../descrip[@type="superordinateConceptGeneric"]/string()'),
            ('antonym_concept',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../../descrip[@type="antonymConcept"]/string()'),
            ('related_concept',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/../../descrip[@type="relatedConcept"]/string()'),
            ('part_of_speech',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/termNote[@type="partOfSpeech"]/string()'),
            ('term_type',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/termNote[@type="termType"]/string()'),
            ('administrative_status',
             u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/termNote[@type="administrativeStatus"]/string()'),
        ]

        for key, qs in fields:
            result = dbxml.session.query(qs.format(self.id),
                                          document='tzos.xml').as_str().first()
            setattr(self, key, result)

    def insert(self):
        """Inserts the current term to the DB."""

        ctx = {
            'date': strftime('%Y-%m-%d %H:%M:%S%z'),
            'username': g.user.username,
            'term_id': dbxml.session.generate_id('term'),
            'subject_field': self.subject_field
            }
        ctx.update(self.__dict__)

        if hasattr(self, 'cross_reference') and self.cross_reference:
            xref_term = Term(term=self.cross_reference)
            xref_id = xref_term.id

            ctx.update({'xref_id': xref_id})

        if hasattr(self, 'syntrans') and self.syntrans:
            syntrans_term = Term(term=self.syntrans_term)
            syntrans_term.language = self.syntrans_language

            if syntrans_term.has_langset(self.language):

                template_name = 'xml/new_term.xml'
                where = u'/martif/text/body/termEntry[@id="{0}"]/langSet[@xml:lang="{1}"]'.format(syntrans_term.concept_id, self.language)

            else:

                template_name = 'xml/new_langset.xml'
                where = u'/martif/text/body/termEntry[@id="{0}"]'.format(syntrans_term.concept_id)


        else:

            ctx.update({'concept_id': dbxml.session.generate_id('concept')})
            template_name = 'xml/new_concept.xml'
            where = u'/martif/text/body'

        xml = render_template(template_name, **ctx)

        if dbxml.session.insert_as_first(xml, where, document='tzos.xml'):
            self.term_id = ctx['term_id']
            return True

        return False

    def update(self, field, value):
        """Updates current term's DB data with the object's data."""

        fields_map = {
            'concept_origin':
             u'//tig[@id="{0}"]/admin[@type="conceptOrigin"]',
            'subject_field':
             u'//tig[@id="{0}"]/../../descrip[@type="subjectField"]',
            'working_status':
             u'//tig[@id="{0}"]/admin[@type="elementWorkingStatus"]',
            'originating_person':
             u'//tig[@id="{0}"]/admin[@type="originatingPerson"]',
            'definition':
             u'//tig[@id="{0}"]/../descrip[@type="definition"]',
            'context':
             u'//tig[@id="{0}"]/descrip[@type="context"]',
            'example':
             u'//tig[@id="{0}"]/descrip[@type="example"]',
            'explanation':
             u'//tig[@id="{0}"]/descrip[@type="explanation"]',
            'entry_source':
             u'//tig[@id="{0}"]/admin[@type="entrySource"]',
            'product_subset':
             u'//tig[@id="{0}"]/admin[@type="productSubset"]',
            'subordinate_concept_generic':
             u'//tig[@id="{0}"]/../../descrip[@type="subordinateConceptGeneric"]',
            'superordinate_concept_generic':
             u'//tig[@id="{0}"]/../../descrip[@type="superordinateConceptGeneric"]',
            'antonym_concept':
             u'//tig[@id="{0}"]/../../descrip[@type="antonymConcept"]',
            'related_concept':
             u'//tig[@id="{0}"]/../../descrip[@type="relatedConcept"]',
            'part_of_speech':
             u'//tig[@id="{0}"]/termNote[@type="partOfSpeech"]',
            'term_type':
             u'//tig[@id="{0}"]/termNote[@type="termType"]',
            'administrative_status':
             u'//tig[@id="{0}"]/termNote[@type="administrativeStatus"]',
        }

        try:
            qs = fields_map[field]

            old = qs.format(self.id)

            if isinstance(value, list):
                value = u";".join(value)

            if dbxml.session.replace_value(old, value):
                # Update object's value as well
                setattr(self, field, value)

                return True

            return False
        except KeyError:
            return False
