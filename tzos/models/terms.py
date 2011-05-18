# -*- coding: utf-8 -*-
"""
    tzos.models.terms
    ~~~~~~~~~~~~~~~~~

    Term models.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from time import strftime

from flask import g, render_template

from tzos.extensions import dbxml

class Term(object):

    def __init__(self, id=None, term=None):
        if id:
            self.term_id = id

        if term:
            self.term = term

    @property
    def id(self):
        if hasattr(self, 'term_id'):
            return self.term_id

        qs = "//term[string()='{0}']/data(@id)".format(self.term)
        result = dbxml.get_db().query(qs).as_str().first()

        if result:
            self.term_id = result

        return result

    def exists(self):
        """Returns True if the current term exists in the DB."""

        if not self.id:
            return False

        qs = "//term[@id='{0}']".format(self.id)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return True

        return False

    def has_langset(self, langcode):
        """Returns True if the current term has a langSet for langcode."""
        qs = '//langSet[@xml:lang="{0}" and ..//term[string()="{1}"]]'. \
            format(langcode, self.term)
        result = dbxml.get_db().query(qs).as_str().first()

        if result is not None:
            return True

        return False

    def populate(self):
        """Populates current term's fields by querying fields by id."""

        fields = [
            ('term', '//term[@id="{0}"]/string()'),
            ('language', '//term[@id="{0}"]/../langSet/@xml:lang'),
            ('concept_origin',
             '//term[@id="{0}"]/../admin[@type="conceptOrigin"]/string()'),
            #conceptOrigin missing

            ('subject_field',
             '//term[@id="{0}"]/../../../descrip[@type="subjectField"]/string()'),
            ('working_status',
             '//term[@id="{0}"]/../admin[@type="elementWorkingStatus"]/string()'),
            ('originating_person',
             '//term[@id="{0}"]/../admin[@type="originatingPerson"]/string()'),
            ('definition',
             '//term[@id="{0}"]/../../descrip[@type="definition"]/string()'),
            ('context',
             '//term[@id="{0}"]/../descrip[@type="context"]/string()'),
            ('example',
             '//term[@id="{0}"]/../descrip[@type="example"]/string()'),
            ('explanation',
             '//term[@id="{0}"]/../descrip[@type="explanation"]/string()'),
            ('entry_source',
             '//term[@id="{0}"]/../admin[@type="entrySource"]/string()'),
            ('cross_reference',
             '//term[@id="{0}"]/../ref[@type="crossReference"]/string()'),
            ('product_subset',
             '//term[@id="{0}"]/../admin[@type="productSubset"]/string()'),

            ('normative_authorization',
             '//term[@id="{0}"]/../termNote[@type="normativeAuthorization"]/string()'),
            ('normative_authorization_org',
             '//term[@id="{0}"]/../termNote[@type="normativeAuthorization"]/data(@target)'),
            ('subordinate_concept_generic',
             '//term[@id="{0}"]/../../../descrip[@type="subordinateConceptGeneric"]/string()'),
            ('superordinate_concept_generic',
             '//term[@id="{0}"]/../../../descrip[@type="superordinateConceptGeneric"]/string()'),
            ('antonym_concept',
             '//term[@id="{0}"]/../../../descrip[@type="antonymConcept"]/string()'),
            ('related_concept',
             '//term[@id="{0}"]/../../../descrip[@type="relatedConcept"]/string()'),
            ('part_of_speech',
             '//term[@id="{0}"]/../termNote[@type="partOfSpeech"]/string()'),
            ('term_type',
             '//term[@id="{0}"]/../termNote[@type="termType"]/string()'),
        ]

        for key, qs in fields:
            result = dbxml.get_db().query(qs.format(self.id)).as_str().first()
            setattr(self, key, result)

    def insert(self):
        """Inserts the current term to the DB."""

        ctx = {
            'orig_person': self.originating_person if self.not_mine else g.user.username,
            'date': strftime('%Y-%m-%d %H:%M:%S%z'),
            'username': g.user.username,
            'term_id': dbxml.get_db().generate_id('term'),
            }
        ctx.update(self.__dict__)

        if self.cross_reference:
            xref_term = Term(term=self.cross_reference)
            xref_id = xref_term.id

            ctx.update({'xref_id': xref_id})

        if self.syntrans:
            syntrans_term = Term(term=self.syntrans_term)

            if syntrans_term.has_langset(self.language):
                template_name = 'xml/new_term.xml'
                where = '//langSet[@xml:lang="{0}"]/tig[../..//term[@id="{1}"]][1]' \
                    .format(self.language, syntrans_term.id)
            else:
                template_name = 'xml/new_langset.xml'
                where = '//langSet[..//term[@id="{0}"]][1]'.format(syntrans_term.id)
        else:
            ctx.update({'concept_id': dbxml.get_db().generate_id('concept')})
            template_name = 'xml/new_concept.xml'
            where = '//termEntry[1]'

        xml = render_template(template_name, **ctx)

        if dbxml.get_db().insert_before(xml, where):
            self.term_id = ctx['term_id']
            return True

        return False
