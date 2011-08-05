# -*- coding: utf-8 -*-
"""
    tzos.views.admin
    ~~~~~~~~~~~~~~~~

    Administration views

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
import os

from flask import Module, current_app, flash, g, make_response, redirect, \
        render_template, request, send_from_directory, url_for

from flaskext.babel import gettext as _, lazy_gettext as _l
from flaskext.wtf import required, TextField

from tzos.extensions import cache, db, dbxml
from tzos.forms import AddLanguagesForm, AddTermOriginForm, AddTermSourceForm, \
        AddTermSubjectForm, BackupForm, DeleteUploadForm, EditTermOriginForm, \
        EditTermSourceForm, EditTermSubjectForm, ExportForm, \
        ModifyUserPermissionForm
from tzos.helpers import get_dict_langs, get_origins_dropdown, \
        get_sfields_dropdown
from tzos.models import Term, TermOrigin, TermSource, TermSubject, TermUpload, \
        Translation, User
from tzos.permissions import admin as admin_permission

admin = Module(__name__)


def _gen_users_form():

    form = ModifyUserPermissionForm()
    form.user.choices = [(u.id, u.username) for u in \
        User.query.filter(User.username!=g.user.username)
                  .order_by('username')]

    return form


def _gen_origins_form(form_cls, **kwargs):

    form = form_cls(**kwargs)

    form.parent_id.choices = get_origins_dropdown()

    return form


def _gen_sfields_form(form_cls, sfields=[], **form_args):

    class F(form_cls):
        pass

    langs = Translation.query.values(db.distinct(Translation.locale))

    for values in langs:
        code = values[0]
        field_name = u'name-{0}'.format(code)
        field_label = _l(u'Name (%(lang)s)', lang=code)
        setattr(F, field_name, TextField(field_label,
            validators=[required(message=_(u"Name is required."))]))

    form = F(**form_args)

    form.parent_id.choices = get_sfields_dropdown(g.ui_lang)

    # If passed, set data
    for sf in sfields:
        form.parent_id.data = sf.parent_id
        form.code.data = sf.code
        getattr(form, "name-%s" % sf.translations.locale).data = sf.translations.text

    return form


def _gen_export_form(form_cls, **kwargs):

    form = form_cls(**kwargs)

    form.lang.choices = get_dict_langs()
    form.subject_field.choices = get_sfields_dropdown(g.ui_lang)
    form.concept_origin.choices = get_origins_dropdown()

    return form


@admin.route('/')
@admin_permission.require(401)
def settings():

    users = User.query.filter(User.role > User.MEMBER) \
                      .order_by('-role', 'username')
    origins = TermOrigin.query.filter(TermOrigin.parent_id==None) \
                              .order_by('name').all()
    sfields = TermSubject.query \
            .join('translations') \
            .filter((TermSubject.parent_id==None) &
                    (Translation.locale==g.ui_lang)) \
            .order_by('text').all()
    sources = TermSource.query.order_by('name').all()
    uploads = TermUpload.query.all()

    try:
        bkp_home = current_app.config['TZOS_BKP_HOME']
        bkp_ext = u'.tar.bz2'
        bkps = [f for f in os.listdir(bkp_home) if f.lower().endswith(bkp_ext)]
        bkps = sorted(bkps, reverse=True)
    except OSError:
        bkps = []

    users_form = _gen_users_form()
    langs_form = AddLanguagesForm()
    origins_form = _gen_origins_form(AddTermOriginForm)
    sources_form = AddTermSourceForm()
    sfields_form = _gen_sfields_form(AddTermSubjectForm)
    export_form = _gen_export_form(ExportForm)
    backup_form = BackupForm()

    ctx = {'users': users, 'origins': origins, 'sfields': sfields,
            'sources': sources, 'uploads': uploads, 'bkps': bkps,
            'users_form': users_form, 'langs_form': langs_form,
            'origins_form': origins_form, 'sources_form': sources_form,
            'sfields_form': sfields_form, 'export_form': export_form,
            'backup_form': backup_form }
    return render_template("admin/settings.html", **ctx)

@admin.route('/users/', methods=('POST',))
@admin_permission.require(401)
def users():

    form = _gen_users_form()

    if form and form.validate_on_submit():
        user = User.query.filter_by(id=form.user.data).first_or_404()

        user.role = form.role.data
        db.session.commit()

        flash(_(u"Permissions for ‘%(user)s’ have been updated.",
                user=user.username), "success")
    else:
        flash(_(u"Error while updating permissions."), "error")

    return redirect(url_for("admin.settings"))

@admin.route('/languages/', methods=('POST',))
@admin_permission.require(401)
def languages():

    form = AddLanguagesForm()

    if form and form.validate_on_submit():

        qs = '''
        let $lang := collection($collection)/TBXXCS/languages/langInfo[langCode[string()="{0}"]]
        let $xml :=
            <langInfo>
                <langCode>{0}</langCode><langName>{1}</langName>
           </langInfo>
        return
            if (empty($lang)) then
                insert node $xml as last into collection($collection)/TBXXCS/languages
            else
                replace node $lang with $xml
        '''.format(form.code.data.encode('utf-8'),
                   form.name.data.encode('utf-8'))

        if dbxml.session.insert_raw(qs):
            # Invalidate cache
            cache.delete_memoized('get_dict_langs')

            flash(_(u"Language ‘%(lang)s’ has been added.",
                    lang=form.name.data), "success")
    else:
        flash(_(u"Error while adding language. Check the inserted "
                "values are correct."), "error")

    return redirect(url_for("admin.settings"))

@admin.route('/origin/add/', methods=('POST',))
@admin_permission.require(401)
def add_origin():

    form = _gen_origins_form(AddTermOriginForm)

    if form and form.validate_on_submit():
        origin = TermOrigin(name=form.name.data)

        if form.parent_id.data > -1:
            origin.parent_id = form.parent_id.data

        db.session.add(origin)
        db.session.commit()

        flash(_(u"Term origin ‘%(origin)s’ has been added.",
                origin=origin.name), "success")
    else:
        flash(_(u"Error while adding term origin."), "error")

    return redirect(url_for("admin.settings"))

@admin.route('/origin/edit/<int:id>/', methods=('GET','POST'))
@admin_permission.require(401)
def edit_origin(id):

    origin = TermOrigin.query.get_or_404(id)
    form = _gen_origins_form(EditTermOriginForm, obj=origin)

    if form and form.validate_on_submit():

        form.populate_obj(origin)

        if form.parent_id.data > -1:
            origin.parent_id = form.parent_id.data
        else:
            origin.parent_id = None

        db.session.commit()

        flash(_(u"Term origin ‘%(origin)s’ has been edited.",
                origin=origin.name), "success")

        return redirect(url_for("admin.settings"))

    return render_template("admin/edit_origin.html", form=form,
                                                     origin=origin)


@admin.route('/source/add/', methods=('POST',))
@admin_permission.require(401)
def add_source():

    form = AddTermSourceForm()

    if form and form.validate_on_submit():
        source = TermSource(name=form.name.data)

        db.session.add(source)
        db.session.commit()

        flash(_(u"Term source ‘%(source)s’ has been added.",
                source=source.name), "success")
    else:
        flash(_(u"Error while adding term source."), "error")

    return redirect(url_for("admin.settings"))

@admin.route('/source/edit/<int:id>/', methods=('GET','POST'))
@admin_permission.require(401)
def edit_source(id):

    source = TermSource.query.get_or_404(id)
    form = EditTermSourceForm(obj=source)

    if form and form.validate_on_submit():

        form.populate_obj(source)

        db.session.commit()

        flash(_(u"Term source ‘%(source)s’ has been edited.",
                source=source.name), "success")

        return redirect(url_for("admin.settings"))

    return render_template("admin/edit_source.html", form=form,
                                                     source=source)


@admin.route('/subject/add/', methods=('POST',))
@admin_permission.require(401)
def add_sfield():

    form = _gen_sfields_form(AddTermSubjectForm)

    if form.validate_on_submit():

        if form.parent_id.data > -1:
            parent_id = form.parent_id.data
        else:
            parent_id = None

        # Add translations
        for field in form:

            if u"name-" in field.name:
                locale = field.name.rsplit(u'-', 1)[1]
                text = field.data
                code = form.code.data

                trans = Translation()
                trans.id = code
                trans.locale = locale
                trans.text = text

                db.session.add(trans)
                db.session.commit()

                # Now we can store the subject field
                sf = TermSubject()
                sf.code = code
                sf.trans_id = trans.auto_id

                if parent_id:
                    sf.parent_id = parent_id

                db.session.add(sf)
                db.session.commit()

        flash(_(u"Term subject ‘%(code)d’ has been added.",
                code=sf.code), "success")
    else:
        flash(_(u"Error while adding subject field. Check the inserted "
                "values are correct."), "error")

    return redirect(url_for("admin.settings"))


@admin.route('/subject/edit/<int:id>/', methods=('GET','POST'))
@admin_permission.require(401)
def edit_sfield(id):

    if request.method == 'GET':
        sfields = TermSubject.query \
                .join('translations') \
                .filter(TermSubject.code==id).all()
    else:
        sfields = []

    form = _gen_sfields_form(EditTermSubjectForm, sfields=sfields)

    if form.validate_on_submit():

        if form.parent_id.data > -1:
            parent_id = form.parent_id.data
        else:
            parent_id = None

        # Iterate over translations and update them
        translations = [f for f in form if u"name-" in f.name]
        for field in translations:

            locale = field.name.rsplit(u'-', 1)[1]
            translation = Translation.query.filter(
                    db.and_(Translation.id==id,
                            Translation.locale==locale)).first()
            translation.text = field.data
            subject = TermSubject.query.get((id, translation.auto_id))
            subject.parent_id = parent_id

        db.session.commit()

        flash(_(u"Term subject ‘%(code)s’ has been edited.",
                code=id), "success")

        return redirect(url_for("admin.settings"))

    return render_template("admin/edit_sfield.html", form=form)


@admin.route('/export/', methods=('POST',))
@admin_permission.require(401)
def export():

    form = ExportForm()

    if form and form.validate_on_submit():

        result = dbxml.session.query('/martif').as_str().first()

        rv = make_response(result)
        rv.content_type = 'application/octet-stream'
        rv.mimetype = 'application/xml'
        rv.headers['Content-Disposition'] = 'attachment; filename=tzos.tbx'

        return rv

    else:

        flash(_(u"Error validating form. You may want to reload the page."),
                "error")

    return redirect(url_for("admin.settings"))


@admin.route('/backup/', methods=('POST',))
@admin_permission.require(401)
def backup():

    form = BackupForm()

    if form and form.validate_on_submit():
        import subprocess
        from time import strftime

        bkp_home = current_app.config['TZOS_BKP_HOME']
        db_home = current_app.config['TZOS_DB_HOME']
        mysql_uname = current_app.config['TZOS_MYSQL_USERNAME']
        mysql_pass = current_app.config['TZOS_MYSQL_PASSWORD']
        mysql_db = current_app.config['TZOS_MYSQL_DBNAME']
        fname = 'tzos_backup_{0}'.format(strftime('%Y%m%d_%H%M'))

        cmd = """
        mkdir -p {0}/{2}/dbxml {0}/{2}/sql;
        db_hotbackup -h {1}/dbxml/ -b {0}/{2}/dbxml/;
        mysqldump --opt --user={3} --password={4} {5} > {0}/{2}/sql/tzos.sql;
        cd {0}; tar cfj {2}.tar.bz2 {2}/;
        rm -rf {2}; cd -;
        """.format(bkp_home, db_home, fname, mysql_uname, mysql_pass, mysql_db)

        try:
            p = subprocess.Popen(cmd, cwd=db_home, shell=True)
            p.wait()

            flash(_(u"Backup done successfully."), "success")
        except OSError:
            flash(_(u"OS error while trying to make the backup."),
                    "error")
        except ValueError:
            flash(_(u"Invalid arguments passed to the backup command."),
                    "error")


    else:

        flash(_(u"Error validating form. You may want to reload the page."),
                "error")

    return redirect(url_for("admin.settings"))


@admin.route('/backup/<path:filename>')
@admin_permission.require(401)
def download_backup(filename):
    return send_from_directory(current_app.config['TZOS_BKP_HOME'],
                               filename, as_attachment=True)


@admin.route('/upload/<int:id>')
@admin_permission.require(401)
@cache.cached()
def view_upload(id):

    upload = TermUpload.query.get_or_404(id==id)

    delete_form = DeleteUploadForm()

    terms = upload.get_terms()

    if request.is_xhr:
        template_filename = 'admin/view_upload_content.html'
    else:
        template_filename = 'admin/view_upload.html'

    return render_template(template_filename, terms=terms,
                                              delete_form=delete_form,
                                              upload_id=id)


@admin.route('/upload/<int:id>/delete/', methods=('POST',))
@admin_permission.require(401)
def delete_upload(id):

    upload = TermUpload.query.get_or_404(id==id)

    if upload.delete_terms():
        flash(u"Terms deleted successfully.", "success")
    else:
        flash(u"Failed to delete terms.", "error")

    db.session.commit()

    return redirect(url_for("admin.settings"))
