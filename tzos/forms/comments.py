# -*- coding: utf-8 -*-
"""
    tzos.forms.comments
    ~~~~~~~~~~~~~~~~~~~

    Comments' forms.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.wtf import Form, HiddenField, TextAreaField, SubmitField, required
from flaskext.babel import lazy_gettext as _


class CommentForm(Form):

    term_id = HiddenField(validators=[
                          required(message=_("Term id is required."))])

    comment = TextAreaField(validators=[
                            required(message=_("Comment is required."))])

    submit = SubmitField(_("Save"))
