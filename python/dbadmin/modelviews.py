
from flask_admin.contrib import sqla


class UserView(sqla.ModelView):
    column_display_pk = True
    form_columns = (
        'name', 'intro', 'email', 'phone')
    column_list = (
        'name', 'intro', 'email', 'phone')
    column_searchable_list = ('name', )


class GroupView(sqla.ModelView):
    column_display_pk = True
    column_list = ('name', 'intro', 'period', 'admin')
    form_columns = ('name', 'intro', 'period', 'admin')
    column_searchable_list = ('name', )


class RelGroupUserView(sqla.ModelView):
    column_display_pk = True
    column_list = ('group', 'user', 'period')
    form_columns = ('group', 'user', 'period')
