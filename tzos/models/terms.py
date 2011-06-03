# -*- coding: utf-8 -*-
"""
    tzos.models.terms
    ~~~~~~~~~~~~~~~~~

    Term models.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from time import strftime

from flask import g, Markup, render_template, url_for

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


class Term(object):

    def __init__(self, id=None, term=None):
        if id:
            self.term_id = id

        if term:
            self.term = term

        self._subject_field = []
        self._synonyms = []

    @property
    def id(self):
        if hasattr(self, 'term_id'):
            return self.term_id

        qs = u'//tig[term/string()="{0}"]/data(@id)'.format(self.term)
        result = dbxml.get_db().query(qs).as_str().first()

        if result:
            self.term_id = result

        return result

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
        for part in value.split(u";"):
            if part:
                syn = Term(term=part)
                self._synonyms.append(syn)

    synonyms = property(_get_synonyms, _set_synonyms)

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

        if not self.id:
            return False

        qs = u'//tig[@id="{0}"]'.format(self.id)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return True

        return False

    def has_langset(self, langcode):
        """Returns True if the current term has a langSet for langcode."""
        qs = u'//langSet[@xml:lang="{0}" and ..//term[string()="{1}"]]'. \
            format(langcode, self.term)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return True

        return False

    def is_public(self):
        """Returns True if the current term has an elementWorkingStatus
        with a value of `workingElement` or higher."""

        if not hasattr(self, 'working_status'):
            qs = u'//tig[@id="{0}"]/admin[@type="elementWorkingStatus"]/string()'.format(self.id)
            self.working_status = dbxml.get_db().query(qs).as_str().first()
        if not self.working_status:
            return False

        return self.working_status != "starterElement" and \
               self.working_status != "importedElement" and \
               self.working_status != "archiveElement"

    def is_consolidated(self):
        """Returns True if the current term has an elementWorkingStatus
        with a value of `consolidatedElement` or higher."""

        if not hasattr(self, 'working_status'):
            qs = u'//tig[@id="{0}"]/admin[@type="elementWorkingStatus"]/string()'.format(self.id)
            self.working_status = dbxml.get_db().query(qs).as_str().first()
        if not self.working_status:
            return False

        return self.working_status != "starterElement" and \
               self.working_status != "importedElement" and \
               self.working_status != "workingElement"

    def is_mine(self):
        """Returns True if the term's `origintatingPerson` is the same
        as the user who committed the term."""

        if not hasattr(self, 'originating_person'):
            qs = u'//tig[@id="{0}"]/admin[@type="originatingPerson"]/string()'.format(self.id)
            self.originating_person = dbxml.get_db().query(qs).as_str().first()
        if self.originating_person is None:
            return False

        return self.originating_person == self.owner()

    # FIXME: optimize this with a property
    def owner(self):
        """Returns the term owner, ie the username who first inserted
        this term."""

        qs = u'//tig[@id="{0}" and (transacGrp/transac[@type="transactionType"]/string()="origination" or transacGrp/transac[@type="transactionType"]/string()="importation" or transacGrp/transac[@type="transactionType"]/string()="input")]/transacGrp/transacNote[@type="responsibility"]/string()'.format(self.id)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return result

        return u""

    def populate(self):
        """Populates current term's fields by querying fields by id."""

        fields = [
            ('term', u'//tig[@id="{0}"]/term/string()'),
            ('language', u'//tig[@id="{0}"]/../data(@xml:lang)'),
            ('concept_origin',
             u'//tig[@id="{0}"]/admin[@type="conceptOrigin"]/string()'),
            ('subject_field',
             u'//tig[@id="{0}"]/../../descrip[@type="subjectField"]/string()'),
            ('working_status',
             u'//tig[@id="{0}"]/admin[@type="elementWorkingStatus"]/string()'),
            ('originating_person',
             u'//tig[@id="{0}"]/admin[@type="originatingPerson"]/string()'),
            ('definition',
             u'//tig[@id="{0}"]/../descrip[@type="definition"]/string()'),
            ('context',
             u'//tig[@id="{0}"]/descrip[@type="context"]/string()'),
            ('example',
             u'//tig[@id="{0}"]/descrip[@type="example"]/string()'),
            ('explanation',
             u'//tig[@id="{0}"]/descrip[@type="explanation"]/string()'),
            ('entry_source',
             u'//tig[@id="{0}"]/admin[@type="entrySource"]/string()'),
            ('cross_reference',
             u'//tig[@id="{0}"]/ref[@type="crossReference"]/string()'),
            ('product_subset',
             u'//tig[@id="{0}"]/admin[@type="productSubset"]/string()'),

            ('normative_authorization',
             u'//tig[@id="{0}"]/termNote[@type="normativeAuthorization"]/string()'),
            ('normative_authorization_org',
             u'//tig[@id="{0}"]/termNote[@type="normativeAuthorization"]/data(@target)'),
            ('subordinate_concept_generic',
             u'//tig[@id="{0}"]/../../descrip[@type="subordinateConceptGeneric"]/string()'),
            ('superordinate_concept_generic',
             u'//tig[@id="{0}"]/../../descrip[@type="superordinateConceptGeneric"]/string()'),
            ('antonym_concept',
             u'//tig[@id="{0}"]/../../descrip[@type="antonymConcept"]/string()'),
            ('related_concept',
             u'//tig[@id="{0}"]/../../descrip[@type="relatedConcept"]/string()'),
            ('part_of_speech',
             u'//tig[@id="{0}"]/termNote[@type="partOfSpeech"]/string()'),
            ('term_type',
             u'//tig[@id="{0}"]/termNote[@type="termType"]/string()'),
            ('administrative_status',
             u'//tig[@id="{0}"]/termNote[@type="administrativeStatus"]/string()'),
        ]

        for key, qs in fields:
            result = dbxml.get_db().query(qs.format(self.id)).as_str().first()
            setattr(self, key, result)

    def insert(self):
        """Inserts the current term to the DB."""

        ctx = {
            'orig_person': self.originating_person,
            'date': strftime('%Y-%m-%d'),
            'username': g.user.username,
            'term_id': dbxml.get_db().generate_id('term'),
            }
        ctx.update(self.__dict__)

        if hasattr(self, 'cross_reference') and self.cross_reference:
            xref_term = Term(term=self.cross_reference)
            xref_id = xref_term.id

            ctx.update({'xref_id': xref_id})

        if hasattr(self, 'syntrans') and self.syntrans:
            syntrans_term = Term(term=self.syntrans_term)

            if syntrans_term.has_langset(self.language):
                template_name = 'xml/new_term.xml'
                where = u'//langSet[@xml:lang="{0}"]/tig[../..//tig[@id="{1}"]][1]' \
                    .format(self.language, syntrans_term.id)
            else:
                template_name = 'xml/new_langset.xml'
                where = u'//langSet[..//tig[@id="{0}"]][1]'.format(syntrans_term.id)
        else:
            ctx.update({'concept_id': dbxml.get_db().generate_id('concept')})
            template_name = 'xml/new_concept.xml'
            where = u'//body'

            # XXX: Ugly to repeat code here but necessary for now
            xml = render_template(template_name, **ctx)

            if dbxml.get_db().insert_as_first(xml, where):
                self.term_id = ctx['term_id']
                return True

            return False

        xml = render_template(template_name, **ctx)

        if dbxml.get_db().insert_before(xml, where):
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
                value = ";".join(value)

            if dbxml.get_db().replace_value(old, value):
                # Update object's value as well
                setattr(self, field, value)

                return True

            return False
        except KeyError:
            return False
