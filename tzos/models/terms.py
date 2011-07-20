# -*- coding: utf-8 -*-
"""
    tzos.models.terms
    ~~~~~~~~~~~~~~~~~

    Term models.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime, timedelta
from dateutil.parser import parse
from functools import wraps
from time import strftime
import unicodedata

from flask import g, Markup, render_template, url_for

from flaskext.babel import gettext as _

from werkzeug import cached_property

from tzos.extensions import db, dbxml
from tzos.models.translations import Translation
from tzos.models.users import User


class TermOrigin(db.Model):
    __tablename__ = 'origins'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.UnicodeText)

    parent_id = db.Column(db.Integer,
                          db.ForeignKey('origins.id', ondelete='CASCADE'))

    parent = db.relationship('TermOrigin', remote_side=[id], backref='children')


class TermSource(db.Model):
    __tablename__ = 'sources'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.UnicodeText)


class TermSubject(db.Model):
    __tablename__ = 'subjectfields'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    code = db.Column('id', db.Integer, autoincrement=False, primary_key=True)

    parent_id = db.Column(db.Integer,
                          db.ForeignKey('subjectfields.id', ondelete='CASCADE'))

    parent = db.relationship('TermSubject', remote_side=[code],
            backref=db.backref('children', lazy='dynamic'))

    trans_id = db.Column(db.Integer,
                         db.ForeignKey('translations.auto_id',
                             ondelete='CASCADE'),
                         primary_key=True)

    translations = db.relationship('Translation', backref='termsubject')

    @classmethod
    def root_code(cls, code):
        """Returns the code of the parent element that is located on the
        root of TermSubject represented by `code`."""

        term_subject = cls.query.filter(TermSubject.code==code).first()

        if not term_subject:
            return None

        while term_subject.parent_id is not None:
            term_subject = term_subject.parent

        return term_subject.code

    @classmethod
    def root_codes(cls, code):
        """Returns a list of codes of the parent and sibling elements that
        are located near the TermSubject represented by `code`."""

        term_subject = cls.query.filter(TermSubject.code==code).first()

        if not term_subject:
            return None

        codes = [unicode(term_subject.code)]

        while term_subject.parent_id is not None:

            siblings = self.query \
                    .filter((TermSubject.parent_id==term_subject.parent_id) &
                            (TermSubject.code!=term_subject.code)) \
                    .all()

            for sibling in siblings:
                codes.append(unicode(sibling.code))

            term_subject = term_subject.parent

        # We return a set because we don't want duplicated entries
        return set(codes)


    def children_translations(self, locale):
        return self.children \
                .join('translations') \
                .filter((TermSubject.parent_id==self.code) &
                        (Translation.locale==locale)) \
                                .order_by('text').all()


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


def working_status(f):
    """A decorator to retrieve the Term's working status in case it's
    not defined yet."""

    @wraps(f)
    def decorator(obj, *args, **kwargs):
        if not hasattr(obj, 'working_status'):
            qs = u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/admin[@type="elementWorkingStatus"]/string()'.format(obj.id)
            obj.working_status = dbxml.session.query(qs).as_str().first()
        if not obj.working_status:
            return False

        return f(obj, *args, **kwargs)

    return decorator


class Term(object):

    class TermLocked(Exception):
        pass

    @classmethod
    def parse(cls, value):
        """Parses a string into a Term object."""

        if not value:
            return None

        parts = value.split(u"|||")

        term = Term(parts[0], parts[2], parts[1])

        term.concept_origin = parts[3]
        term.subject_field = parts[4]
        term.originating_person = parts[5]
        term.definition = parts[6]
        term.context = parts[7]
        term.example = parts[8]
        term.explanation = parts[9]
        term.entry_source = parts[10]
        term.cross_reference = parts[11]
        term.product_subset = parts[12]
        term.normative_authorization = parts[13]
        term.normative_authorization_org = parts[14]
        term.subordinate_concept_generic = parts[15]
        term.superordinate_concept_generic = parts[16]
        term.antonym_concept = parts[17]
        term.related_concept = parts[18]
        term.part_of_speech = parts[19]
        term.term_type = parts[20]
        term.administrative_status = parts[21]
        term.synonyms = parts[22]
        term.translations = parts[23]
        term.working_status = parts[24]
        term.owner = parts[25]
        term.sortkey = parts[26]
        try:
            # When the last string is empty, we need to treat it specially
            term.edit_lock = parts[27]
        except IndexError:
            term.edit_lock = None

        return term

    def __init__(self, id=None, term=None, language=None):
        if id:
            self._id = id

        if term:
            self.term = term

        if language:
            self.language = language

        self._subject_field = []
        self._synonyms = []
        self._raw_synonyms = []
        self._translations = {}
        self._raw_translations = {}
        self._lock = None

    @property
    def id(self):
        if hasattr(self, '_id'):
            return self._id

        # FIXME: check subjectField too
        qs = u'/martif/text/body/termEntry/langSet[@xml:lang="{0}"]/tig[term/string()="{1}"]/data(@id)'.format(self.language, self.term)
        result = dbxml.session.query(qs, document='tzos.xml').as_str().first()

        if result:
            self._id = result

        return result

    def _get_concept_id(self, txn=None, commit=True):

        # FIXME: check subjectField too
        qs = u'/martif/text/body/termEntry[langSet[@xml:lang="{0}"] and langSet/tig/term/string()="{1}"]/data(@id)'.format(self.language, self.term)
        return dbxml.session.query(qs, document='tzos.xml', txn=txn, commit=commit).as_str().first()

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

    @cached_property
    def subject_field_display(self):

        sf_list = []

        for field in self.subject_field:

            sfield = TermSubject.query \
                    .join('translations') \
                    .filter((TermSubject.code==field) &
                            (Translation.locale==g.ui_lang)).first()

            tmp = [sfield.translations.text]

            while sfield.parent_id:
                sfield = sfield.parent
                tmp.insert(0, sfield.translations.text)

            sf_list.append(Markup(u' » '.join(tmp)))

        return sorted(sf_list)

    def _get_subject_field(self):
        return self._subject_field

    def _set_subject_field(self, value):
        if isinstance(value, list):
            self._subject_field = value
        else:
            for part in value.split(u";"):
                if part and part not in self._subject_field:
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

    @property
    def raw_synonyms(self):
        return self._raw_synonyms

    def append_raw_synonym(self, value):

        if isinstance(value, list):
            for term in value:
                syn = self.minimal_clone(term.strip(), self.language)
                self._raw_synonyms.append(syn)
        else:
            syn = self.minimal_clone(value.strip(), self.language)
            self._raw_synonyms.append(syn)

    def _get_translations(self):
        return self._translations

    def _set_translations(self, value):
        for part in value.split(u";;;"):
            if part:
                lang, id, term = part.split(u";", 2)
                trans = Term(id=id, term=term)
                self._translations.setdefault(lang, []).append(trans)

    translations = property(_get_translations, _set_translations)

    @property
    def raw_translations(self):
        return self._raw_translations

    def append_raw_translation(self, lang, value):

        if isinstance(value, list):
            for term in value:
                trans = self.minimal_clone(term.strip(), lang)
                self._raw_translations.setdefault(lang, []).append(trans)
        else:
            trans = self.minimal_clone(value.strip(), lang)
            self._raw_translations.setdefault(lang, []).append(trans)

    def _get_lock(self):
        return self._lock

    def _set_lock(self, lock_str):
        if lock_str:
            uid, expires = lock_str.split(u"-", 1)
            self._lock = {'uid': int(uid), 'expires': expires}
        else:
            self._lock = None

    edit_lock = property(_get_lock, _set_lock)

    @property
    def lock_time(self):
        return self.edit_lock.setdefault('expires', None)

    @property
    def locked_by(self):
        return self.edit_lock.setdefault('uid', None)

    @property
    def locked(self):

        # No lock exists
        if self.edit_lock is None:
            return False

        uid = self.locked_by
        expires = parse(self.lock_time)
        now = datetime.now()

        # Not expired but current user holds the lock
        if uid == g.user.id and \
           expires >= now:
            return False

        # Lock expired
        if expires < now:
            self.unlock()
            return False

        return True

    def lock(self, timeout=15):
        """Locks the current term for edition.

        The lock will be held for the current user for `timeout`
        minutes. After that time the lock will be reset unless the user
        reloads the editing page.

        If the term about to be edited is already locked, `Term.TermLocked`
        exception is raised.
        """

        if self.locked:
            raise self.TermLocked()

        expires = datetime.now() + timedelta(minutes=timeout)
        lock_str = "%d-%s" % (g.user.id, expires.isoformat())
        self.lock = lock_str

        qs = '''
        let $tig := collection($collection)/martif/text/body/termEntry/langSet[@xml:lang="%s"]/tig[@id="%s"]
        let $lock := attribute lock { "%s" }
        return if (exists($tig/@lock)) then
            replace node $tig/@lock with $lock
            else
            insert node $lock into $tig
        ''' % (self.language, self.id, lock_str)
        dbxml.session.insert_raw(qs.encode('utf-8'))

    def unlock(self):
        """Removes the current term's edition locks from the DB, letting
        the way free for new edits.
        """

        self.edit_lock = None

        qs = 'delete node collection($collection)/martif/text/body/termEntry/langSet/tig[@id="{0}"]/@lock'.format(self.id)
        dbxml.session.insert_raw(qs.encode('utf-8'))

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

    def normalize(self):
        """Normalizes the give text for using in sortKey elements."""

        # Remove accents
        nkfd_form = unicodedata.normalize('NFKD', self.term)
        term = u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

        # Lowercase term
        term = term.lower()

        # Remove conflictive characters
        rm_chars = (u"'", u'"', u'`', u'-', u'«', u'»', u'/')
        for char in rm_chars:
            term = term.replace(char, u'')

        return term

    def exists(self):
        """Returns True if the current term exists in the DB."""

        return self.id is not None

    def minimal_clone(self, term, language):
        """Returns a new Term object with the minimal set of
        required fields cloned."""

        t = Term(term=term, language=language)

        t.subject_field = self.subject_field
        t.syntrans = True
        t.syntrans_term = self.term
        t.syntrans_language = self.language
        t.concept_origin = self.concept_origin
        t.originating_person = self.originating_person
        t.transac_type = self.transac_type
        t.working_status = self.working_status

        return t

    def check_collision(self, txn=None, commit=True):
        """If a collision happens, a list with the terms which are
        present in the DB will be returned. An empty list will be
        returned otherwise.

        There's a collision if there's a match in
        - the term itself,
        - the language, and
        - one of the parent subject fields (a subject field on the root)
        """

        qs = """
        import module namespace term = "http://tzos.net/term" at "term.xqm";

        for $tig in collection($collection)/martif/text/body/termEntry/langSet[@xml:lang="{0}"]/tig
        where term:is_public($tig) and
            term:term($tig) = "{1}" and
            (let $fields := tokenize(term:subject_field($tig), ";")
            return some $f in $fields satisfies $f = $sfields)
        return term:values($tig, false())
        """.format(self.language.encode('utf-8'),
                   self.term.replace(u'"', u'""').encode('utf-8'))

        root_codes = list(set([unicode(TermSubject.root_code(c)) \
                for c in self.subject_field]))
        ctx = {'sfields': root_codes}

        results = dbxml.session.raw_query(qs, ctx, txn=txn, commit=commit). \
                as_callback(Term.parse).all()

        return results

    def has_langset(self, langcode, txn=None, commit=True):
        """Returns True if the current term has a langSet for langcode."""
        qs = u'/martif/text/body/termEntry[@id="{0}"]/langSet[@xml:lang="{1}"]'. \
            format(self._get_concept_id(txn, commit), langcode)
        result = dbxml.session.query(qs, document='tzos.xml', txn=txn, commit=commit). \
                as_str().first()

        return result is not None

    @property
    @working_status
    def is_public(self):
        """Returns True if the current term has an elementWorkingStatus
        with a value of `workingElement` or higher."""

        return self.working_status != u"starterElement" and \
               self.working_status != u"importedElement" and \
               self.working_status != u"archiveElement"

    @property
    @working_status
    def is_consolidated(self):
        """Returns True if the current term has an elementWorkingStatus
        with a value of `consolidatedElement` or higher."""

        return self.working_status != u"starterElement" and \
               self.working_status != u"importedElement" and \
               self.working_status != u"workingElement"

    @property
    @working_status
    def is_unreviewed(self):
        """Returns True if the current term has an elementWorkingStatus
        with a value of `starterElement` or `importedElement`."""

        return self.working_status == u"starterElement" or \
               self.working_status == u"importedElement"

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


    def insert_all(self, emulate=False, force=False):
        """Inserts the current term and the equivalent terms stored
        in the object to the DB."""

        class Namespace(): pass

        ns = Namespace()
        ns.collision = False
        ns.error = False

        objects = []
        results = []

        def _insert_term(t, txn):

            objs = t.check_collision(txn=txn, commit=False)

            if objs and not force:
                results.append((t, 'warning'))
                ns.collision = True
            else:
                if t.insert(emulate, txn=txn, commit=False):
                    results.append((t, 'success'))
                else:
                    results.append((t, 'error'))
                    ns.error = True

            return objs

        def _insert_single(t, txn):
            obj = _insert_term(t, txn)
            objects.extend(obj)

        # Enclose inserting all terms within a single transaction
        txn = dbxml.session.manager.createTransaction()

        _insert_single(self, txn)

        for syn in self.raw_synonyms:
            _insert_single(syn, txn)

        for lang, items in self.raw_translations.iteritems():
            for term in items:
                _insert_single(term, txn)

        if ns.collision:
            st = u"collision"
        elif ns.error:
            st = u"error"
        else:
            st = u"success"

        # Finally try to commit the transaction
        try:
            if emulate or ns.collision or ns.error:
                txn.abort()
            else:
                txn.commit()
        except Exception:
            st = u"error"
            txn.abort()

        return st, results, objects


    def insert(self, emulate=False, txn=None, commit=True):
        """Inserts the current term to the DB."""

        if not hasattr(self, 'sortkey'):
            self.sortkey = self.normalize()

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

            if syntrans_term.has_langset(self.language, txn=txn, commit=commit):
                template_name = 'xml/new_term.xml'
                where = u'/martif/text/body/termEntry[@id="{0}"]/langSet[@xml:lang="{1}"]'.format(syntrans_term._get_concept_id(txn, commit), self.language)

            else:

                template_name = 'xml/new_langset.xml'
                where = u'/martif/text/body/termEntry[@id="{0}"]'.format(syntrans_term._get_concept_id(txn, commit))


        else:

            ctx.update({'concept_id': dbxml.session.generate_id('concept')})
            template_name = 'xml/new_concept.xml'
            where = u'/martif/text/body'

        xml = render_template(template_name, **ctx)

        if dbxml.session.insert_as_first(xml, where,
                                         document='tzos.xml',
                                         txn=txn, commit=commit):
            self._id = ctx['term_id']
            return True

        return False

    def update(self, field, value):
        """Updates current term's DB data with the object's data."""

        fields_map = {
            # FIXME: should check for collisions if term is edited
            'term':
            u'/martif/text/body/termEntry/langSet/tig[@id="{0}"]/term',
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
