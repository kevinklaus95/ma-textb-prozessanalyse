# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accounts(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=132)
    description = models.CharField(max_length=132)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts'


class Acos(models.Model):
    parent_id = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    foreign_key = models.IntegerField(blank=True, null=True)
    alias = models.CharField(max_length=255, blank=True, null=True)
    lft = models.IntegerField(blank=True, null=True)
    rght = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acos'


class Aros(models.Model):
    parent_id = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    foreign_key = models.IntegerField(blank=True, null=True)
    alias = models.CharField(max_length=255, blank=True, null=True)
    lft = models.IntegerField(blank=True, null=True)
    rght = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aros'


class ArosAcos(models.Model):
    aro_id = models.IntegerField()
    aco_id = models.IntegerField()
    field_create = models.CharField(db_column='_create', max_length=2)  # Field renamed because it started with '_'.
    field_read = models.CharField(db_column='_read', max_length=2)  # Field renamed because it started with '_'.
    field_update = models.CharField(db_column='_update', max_length=2)  # Field renamed because it started with '_'.
    field_delete = models.CharField(db_column='_delete', max_length=2)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'aros_acos'
        unique_together = (('aro_id', 'aco_id'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Budgets(models.Model):
    valid_from = models.DateTimeField()
    valid_till = models.DateTimeField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    offset = models.DecimalField(max_digits=9, decimal_places=2)
    budgettype_id = models.IntegerField()
    project_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets'


class Budgettypes(models.Model):
    name = models.CharField(max_length=32)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgettypes'


class Cars(models.Model):
    manufacturer = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    license = models.CharField(max_length=10)
    user_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'


class Clientcontacts(models.Model):
    firstname = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    email = models.CharField(max_length=100)
    client_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientcontacts'


class ClientcontactsProjects(models.Model):
    clientcontact_id = models.IntegerField()
    project_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'clientcontacts_projects'


class Clients(models.Model):
    firstname = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    birthday = models.DateField()
    az = models.CharField(max_length=30)
    debitnumber = models.IntegerField()
    admission = models.DateField()
    address = models.CharField(max_length=128)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    email = models.CharField(max_length=100)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clients'


class Costcenters(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=132)
    created = models.DateTimeField()
    modiefied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'costcenters'


class Customercontacts(models.Model):
    addressform = models.CharField(max_length=32)
    firstname = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    fax = models.CharField(max_length=32)
    email = models.CharField(max_length=100)
    customer_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customercontacts'


class Customers(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=32)
    telefon = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    email = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customers'


class CustomersWorkgroups(models.Model):
    customer_id = models.IntegerField()
    workgroup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'customers_workgroups'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Docprints(models.Model):
    date = models.DateField()
    received = models.IntegerField()
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'docprints'


class Expenses(models.Model):
    name = models.CharField(max_length=32)
    date = models.DateField()
    costs = models.DecimalField(max_digits=16, decimal_places=4)
    comment = models.TextField()
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'expenses'


class Groups(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Guardians(models.Model):
    honor = models.CharField(max_length=10)
    surname = models.CharField(max_length=32)
    company = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    email = models.CharField(max_length=100)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guardians'


class Hours(models.Model):
    start = models.DateTimeField()
    stop = models.DateTimeField()
    timediff = models.DecimalField(max_digits=9, decimal_places=2)
    valid = models.IntegerField()
    comment = models.TextField()
    reflection = models.TextField()
    participant = models.TextField()
    project_id = models.IntegerField()
    task_id = models.IntegerField()
    user_id = models.IntegerField()
    workinghour_id = models.IntegerField()
    wolophase_id = models.IntegerField()
    wolotask_id = models.IntegerField()
    created_by = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hours'


class I18N(models.Model):
    locale = models.CharField(max_length=6)
    model = models.CharField(max_length=255)
    foreign_key = models.IntegerField()
    field = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'i18n'


class Leaders(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'leaders'


class Monthreports(models.Model):
    date = models.DateField()
    user_id = models.IntegerField()
    vacation = models.DecimalField(max_digits=9, decimal_places=2)
    sick = models.DecimalField(max_digits=9, decimal_places=2)
    other = models.DecimalField(max_digits=9, decimal_places=2)
    kilometer = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monthreports'


class Paragraphs(models.Model):
    name = models.CharField(max_length=10)
    sgb = models.CharField(db_column='SGB', max_length=11)  # Field name made lowercase.
    account_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paragraphs'


class ParagraphsProjects(models.Model):
    paragraph_id = models.IntegerField()
    project_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'paragraphs_projects'


class Posts(models.Model):
    user_id = models.IntegerField()
    ticket_id = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class Projects(models.Model):
    az = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    comment = models.TextField()
    client_id = models.IntegerField()
    customer_id = models.IntegerField()
    customercontact_id = models.IntegerField()
    guardian_id = models.IntegerField()
    leader = models.IntegerField()
    coleader = models.IntegerField()
    cocoleader = models.IntegerField()
    weekly_offset = models.DecimalField(max_digits=9, decimal_places=2)
    workgroup_id = models.IntegerField()
    paragraph_id = models.IntegerField()
    deleted = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'projects'


class ProjectsTasks(models.Model):
    project_id = models.IntegerField()
    task_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'projects_tasks'


class ProjectsUsers(models.Model):
    project_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'projects_users'


class ProjectsWorkgroups(models.Model):
    project_id = models.IntegerField()
    workgroup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'projects_workgroups'


class Sams(models.Model):
    secret = models.CharField(max_length=20, blank=True, null=True)
    scode = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField()
    valence = models.IntegerField(blank=True, null=True)
    arousal = models.IntegerField(blank=True, null=True)
    dominance = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sams'


class Tasks(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tasks'


class TasksWorkgroups(models.Model):
    task_id = models.IntegerField()
    workgroup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tasks_workgroups'


class Tickets(models.Model):
    user_id = models.IntegerField()
    text = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    priority = models.IntegerField()
    percent = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tickets'


class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    fax = models.CharField(max_length=32)
    address = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    group_id = models.IntegerField()
    workgroup_id = models.IntegerField()
    workinghour_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersWorkgroups(models.Model):
    user_id = models.IntegerField()
    workgroup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users_workgroups'


class Versions(models.Model):
    version_number = models.CharField(max_length=10)
    date = models.DateField()
    comment = models.TextField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versions'


class Widgets(models.Model):
    name = models.CharField(max_length=100)
    part_no = models.CharField(max_length=12, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'widgets'


class Workgroups(models.Model):
    name = models.CharField(max_length=32)
    comment = models.TextField()
    costcenter_id = models.IntegerField()
    deleted = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'workgroups'


class Workinghours(models.Model):
    name = models.CharField(max_length=32)
    day = models.DecimalField(max_digits=9, decimal_places=2)
    targethours = models.DecimalField(max_digits=9, decimal_places=2)
    week = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'workinghours'
