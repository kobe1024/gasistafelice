# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import lib.fields.models
import gf.base.utils
import gf.gas.models.base
from decimal import Decimal
import gf.base.models
from django.conf import settings
import django.core.validators

from gf.gas.workflow_data import workflow_dict

def create_workflows(apps, schema_editor):
    for name, w in workflow_dict.items():
        w.register_workflow()
    return

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('permissions', '__first__'),
        ('des', '0001_initial'),
        ('workflows', '__first__'),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_workflows),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(help_text='when the order will be delivered by supplier', verbose_name='date')),
                ('place', models.ForeignKey(related_name='delivery_set', verbose_name='place', to='base.Place', help_text='where the order will be delivered by supplier')),
            ],
            options={
                'verbose_name': 'delivery',
                'verbose_name_plural': 'deliveries',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='GAS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='name')),
                ('id_in_des', models.CharField(help_text='GAS unique identifier in the DES. Example: CAMERINO--> CAM', unique=True, max_length=8, verbose_name='GAS code')),
                ('logo', models.ImageField(null=True, upload_to=gf.base.utils.get_resource_icon_path, blank=True)),
                ('description', models.TextField(help_text='Who are you? What are yours specialties?', verbose_name='description', blank=True)),
                ('membership_fee', lib.fields.models.CurrencyField(decimal_places=4, default=Decimal('0'), max_digits=10, blank=True, help_text='Membership fee for partecipating in this GAS', verbose_name='membership fee')),
                ('birthday', models.DateField(help_text='When this GAS is born', null=True, verbose_name='birthday', blank=True)),
                ('vat', models.CharField(help_text='VAT number', max_length=11, verbose_name='VAT', blank=True)),
                ('fcc', models.CharField(help_text='Fiscal code card', max_length=16, verbose_name='Fiscal code card', blank=True)),
                ('website', models.URLField(null=True, verbose_name='web site', blank=True)),
                ('association_act', models.FileField(upload_to=gf.base.utils.get_association_act_path, null=True, verbose_name='association act', blank=True)),
                ('intent_act', models.FileField(upload_to=gf.base.utils.get_intent_act_path, null=True, verbose_name='intent act', blank=True)),
                ('note', models.TextField(verbose_name='notes', blank=True)),
            ],
            options={
                'ordering': ('-birthday',),
                'verbose_name_plural': 'GAS',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='GASActivist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info_title', models.CharField(max_length=256, blank=True)),
                ('info_description', models.TextField(blank=True)),
                ('gas', models.ForeignKey(verbose_name='gas', to='gas.GAS')),
                ('person', models.ForeignKey(verbose_name='person', to='base.Person')),
            ],
            options={
                'verbose_name': 'GAS activist',
                'verbose_name_plural': 'GAS activists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GASConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('can_change_price', models.BooleanField(default=False, help_text='GAS can change supplier products price (i.e. to hold some funds for the GAS itself)')),
                ('order_show_only_next_delivery', models.BooleanField(default=False, help_text='GASMember can choose to filter order block among one or more orders that share the next withdrawal appointment', verbose_name='Show only next delivery')),
                ('order_show_only_one_at_a_time', models.BooleanField(default=True, help_text='GASMember can select only one open order at a time in order block', verbose_name='Select only one order at a time')),
                ('default_close_day', models.CharField(blank=True, help_text='default closing order day of the week', max_length=16, verbose_name='default close day', choices=[(b'MONDAY', 'Monday'), (b'TUESDAY', 'Tuesday'), (b'WEDNESDAY', 'Wednesday'), (b'THURSDAY', 'Thursday'), (b'FRIDAY', 'Friday'), (b'SATURDAY', 'Saturday'), (b'SUNDAY', 'Sunday')])),
                ('default_delivery_day', models.CharField(blank=True, help_text='default delivery day of the week', max_length=16, verbose_name='default delivery day', choices=[(b'MONDAY', 'Monday'), (b'TUESDAY', 'Tuesday'), (b'WEDNESDAY', 'Wednesday'), (b'THURSDAY', 'Thursday'), (b'FRIDAY', 'Friday'), (b'SATURDAY', 'Saturday'), (b'SUNDAY', 'Sunday')])),
                ('default_close_time', models.TimeField(help_text='default order closing hour and minutes', null=True, verbose_name='Default close time', blank=True)),
                ('default_delivery_time', models.TimeField(help_text='default delivery closing hour and minutes', null=True, verbose_name='Default delivery day time', blank=True)),
                ('use_withdrawal_place', models.BooleanField(default=False, help_text='If False, GAS never use concept of withdrawal place that is the default', verbose_name='Use concept of withdrawal place')),
                ('can_change_withdrawal_place_on_each_order', models.BooleanField(default=False, help_text='If False, GAS uses only one withdrawal place that is the default or if not set it is the GAS headquarter', verbose_name='can change withdrawal place on each order')),
                ('can_change_delivery_place_on_each_order', models.BooleanField(default=False, help_text='If False, GAS uses only one delivery place that is the default or if not set it is the GAS headquarter', verbose_name='can change delivery place on each order')),
                ('auto_populate_products', models.BooleanField(default=True, help_text='automatic selection of all products bound to a supplier when a relation with the GAS is activated', verbose_name='auto populate products')),
                ('use_scheduler', models.BooleanField(default=False, help_text='Enable scheduler for automatic and planned operations', verbose_name='use scheduler')),
                ('gasmember_auto_confirm_order', models.BooleanField(default=True, help_text="if checked, gasmember's orders are automatically confirmed. If not, each gasmember must confirm by himself his own orders", verbose_name='GAS members orders are auto confirmed')),
                ('is_suspended', models.BooleanField(default=False, help_text='The GAS is not available (holidays, closed). The scheduler uses this flag to operate or not some automatisms', db_index=True, verbose_name='is suspended')),
                ('suspend_datetime', models.DateTimeField(default=None, null=True, blank=True)),
                ('suspend_reason', models.TextField(default=b'', blank=True)),
                ('suspend_auto_resume', models.DateTimeField(default=None, null=True, db_index=True, blank=True)),
                ('notice_days_before_order_close', models.PositiveIntegerField(default=1, help_text='How many days before do you want your GAS receive reminder on closing orders?', null=True, verbose_name='Notice days before order close')),
                ('use_order_planning', models.BooleanField(default=False, help_text='Show order planning section when creating a new order', verbose_name='use order planning')),
                ('send_email_on_order_close', models.BooleanField(default=False, help_text='Default value for pact option to let the system send an email to supplier and gas referrer supplier as soon as an order is closed', verbose_name='default for pacts: send email on order close')),
                ('registration_token', models.CharField(default=b'', validators=[django.core.validators.RegexValidator(regex=b'\\w*\\d+\\w+\\d*|\\d*\\w+\\d+\\w*', message='The token should be at least 5 characters, and must include a cipher'), django.core.validators.MinLengthValidator(5)], max_length=32, blank=True, help_text='If set, this token can be used in the registration phase by a new user to be enabled in the software as soon as he confirms its email. So it IS IMPORTANT, to not make a blind distribution of the token, to choose a token composed of letters and numbers, and to change it each 3 months or occasionally', verbose_name='Registration token')),
                ('privacy_phone', models.CharField(default=b'gas,suppliers', max_length=24, verbose_name='Show gas members phone number to', choices=[(b'nobody', 'Nobody'), (b'gas', 'Only to GAS members'), (b'intergas', 'To every possible intergas members'), (b'des', 'To DES members'), (b'gas,suppliers', 'GAS and suppliers'), (b'intergas,suppliers', 'To every possible intergas members and suppliers'), (b'des,suppliers', 'DES and suppliers')])),
                ('privacy_email', models.CharField(default=b'gas,suppliers', max_length=24, verbose_name='Show gas members email address to', choices=[(b'nobody', 'Nobody'), (b'gas', 'Only to GAS members'), (b'intergas', 'To every possible intergas members'), (b'des', 'To DES members'), (b'gas,suppliers', 'GAS and suppliers'), (b'intergas,suppliers', 'To every possible intergas members and suppliers'), (b'des,suppliers', 'DES and suppliers')])),
                ('privacy_cash', models.CharField(default=b'gas,suppliers', max_length=24, verbose_name='Show gas members cash amount to', choices=[(b'nobody', 'Nobody'), (b'gas', 'Only to GAS members'), (b'intergas', 'To every possible intergas members'), (b'des', 'To DES members'), (b'gas,suppliers', 'GAS and suppliers'), (b'intergas,suppliers', 'To every possible intergas members and suppliers'), (b'des,suppliers', 'DES and suppliers')])),
                ('default_delivery_place', models.ForeignKey(related_name='gas_default_delivery_set', blank=True, to='base.Place', help_text='to specify if different from withdrawal place', null=True, verbose_name='default delivery place')),
                ('default_withdrawal_place', models.ForeignKey(related_name='gas_default_withdrawal_set', blank=True, to='base.Place', help_text='to specify if different from headquarter', null=True, verbose_name='default withdrawal place')),
                ('default_workflow_gasmember_order', models.ForeignKey(related_name='gmow_gasconfig_set', default=gf.gas.models.base.get_gasmember_order_default, blank=True, editable=False, to='workflows.Workflow')),
                ('default_workflow_gassupplier_order', models.ForeignKey(related_name='gsopw_gasconfig_set', default=gf.gas.models.base.get_supplier_order_default, blank=True, editable=False, to='workflows.Workflow')),
                ('gas', models.OneToOneField(related_name='config', to='gas.GAS')),
                ('intergas_connection_set', models.ManyToManyField(help_text='Choose GAS that could be chosen when an interGAS order is created', to='gas.GAS', null=True, verbose_name='possible interGAS orders with', blank=True)),
            ],
            options={
                'verbose_name': 'GAS options',
                'verbose_name_plural': 'GAS options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GASMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_in_gas', models.CharField(help_text='GAS card number', max_length=10, null=True, verbose_name='card number', blank=True)),
                ('membership_fee_payed', models.DateField(help_text='When was the last the annual quote payment', null=True, verbose_name='membership_fee_payed', blank=True)),
                ('use_planned_list', models.BooleanField(default=False, verbose_name='use_list')),
                ('is_suspended', models.BooleanField(default=False, help_text='GAS member is not active now', db_index=True, verbose_name='is suspended')),
                ('suspend_datetime', models.DateTimeField(default=None, null=True, blank=True)),
                ('suspend_reason', models.TextField(default=b'', blank=True)),
                ('suspend_auto_resume', models.DateTimeField(default=None, null=True, db_index=True, blank=True)),
                ('available_for_roles', models.ManyToManyField(related_name='gas_member_available_set', null=True, verbose_name='available for roles', to='permissions.Role', blank=True)),
                ('gas', models.ForeignKey(verbose_name='gas', to='gas.GAS')),
                ('person', models.ForeignKey(verbose_name='person', to='base.Person')),
            ],
            options={
                'ordering': ('gas__name', 'person__display_name'),
                'verbose_name': 'GAS member',
                'verbose_name_plural': 'GAS members',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='GASMemberOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordered_price', lib.fields.models.CurrencyField(verbose_name='ordered price', max_digits=10, decimal_places=4)),
                ('ordered_amount', lib.fields.models.PrettyDecimalField(verbose_name='order amount', max_digits=6, decimal_places=2)),
                ('withdrawn_amount', lib.fields.models.PrettyDecimalField(null=True, verbose_name='widthdrawn amount', max_digits=6, decimal_places=2, blank=True)),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='confirmed')),
                ('note', models.CharField(help_text='GAS member can write some short message about this product for the producer', max_length=64, null=True, verbose_name='product note', blank=True)),
            ],
            options={
                'verbose_name': 'GAS member order',
                'verbose_name_plural': 'GAS member orders',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='GASSupplierOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_start', models.DateTimeField(default=datetime.datetime.now, help_text='when the order will be opened', verbose_name='date open')),
                ('datetime_end', models.DateTimeField(help_text='when the order will be closed', null=True, verbose_name='date close', blank=True)),
                ('order_minimum_amount', lib.fields.models.CurrencyField(null=True, verbose_name='Minimum amount', max_digits=10, decimal_places=4, blank=True)),
                ('delivery_cost', lib.fields.models.CurrencyField(null=True, verbose_name='Delivery cost', max_digits=10, decimal_places=4, blank=True)),
                ('group_id', models.PositiveIntegerField(help_text='If not null this order is aggregate with orders from other GAS', null=True, verbose_name='Order group', blank=True)),
                ('invoice_amount', lib.fields.models.CurrencyField(null=True, verbose_name='invoice amount', max_digits=10, decimal_places=4, blank=True)),
                ('invoice_note', models.TextField(verbose_name='invoice number', blank=True)),
                ('delivery', models.ForeignKey(related_name='order_set', verbose_name='Delivery', blank=True, to='gas.Delivery', null=True)),
                ('delivery_referrer_person', models.ForeignKey(related_name='delivery_for_order_set', verbose_name='delivery referrer', blank=True, to='base.Person', null=True)),
            ],
            options={
                'ordering': ('datetime_end', 'datetime_start'),
                'verbose_name': 'order issued to supplier',
                'verbose_name_plural': 'orders issued to supplier',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='GASSupplierOrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maximum_amount', lib.fields.models.PrettyDecimalField(null=True, verbose_name='maximum amount', max_digits=8, decimal_places=2, blank=True)),
                ('initial_price', lib.fields.models.CurrencyField(verbose_name='initial price', max_digits=10, decimal_places=4)),
                ('order_price', lib.fields.models.CurrencyField(verbose_name='order price', max_digits=10, decimal_places=4)),
                ('delivered_price', lib.fields.models.CurrencyField(null=True, verbose_name='delivered price', max_digits=10, decimal_places=4, blank=True)),
                ('delivered_amount', lib.fields.models.PrettyDecimalField(null=True, verbose_name='delivered amount', max_digits=8, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ('gasstock__stock__supplier__name', 'gasstock__stock__supplier_category__sorting', 'gasstock__stock__product__category__name', 'gasstock__stock__product__name'),
                'verbose_name': 'gas supplier order product',
                'verbose_name_plural': 'gas supplier order products',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='GASSupplierSolidalPact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_signed', models.DateField(default=None, help_text='date of first meeting GAS-Producer', null=True, verbose_name='Date signed', blank=True)),
                ('order_minimum_amount', lib.fields.models.CurrencyField(null=True, verbose_name='Order minimum amount', max_digits=10, decimal_places=4, blank=True)),
                ('order_delivery_cost', lib.fields.models.CurrencyField(null=True, verbose_name='Order delivery cost', max_digits=10, decimal_places=4, blank=True)),
                ('order_deliver_interval', models.TimeField(null=True, verbose_name='Order delivery interval', blank=True)),
                ('order_price_percent_update', models.DecimalField(null=True, verbose_name='order price percent update', max_digits=3, decimal_places=2, blank=True)),
                ('default_delivery_day', models.CharField(blank=True, help_text='delivery week day agreement', max_length=16, verbose_name='default delivery day', choices=[(b'MONDAY', 'Monday'), (b'TUESDAY', 'Tuesday'), (b'WEDNESDAY', 'Wednesday'), (b'THURSDAY', 'Thursday'), (b'FRIDAY', 'Friday'), (b'SATURDAY', 'Saturday'), (b'SUNDAY', 'Sunday')])),
                ('default_delivery_time', models.TimeField(help_text='delivery time agreement', null=True, verbose_name='default delivery time', blank=True)),
                ('auto_populate_products', models.BooleanField(default=True, help_text='automatic population of all products bound to a supplier in gas supplier stock', verbose_name='auto populate products')),
                ('orders_can_be_grouped', models.BooleanField(default=False, help_text='If true, this supplier can aggregate orders from several GAS', verbose_name='can be InterGAS')),
                ('document', models.FileField(help_text='Document signed by GAS and Supplier', upload_to=gf.base.utils.get_pact_path, null=True, verbose_name='document', blank=True)),
                ('send_email_on_order_close', models.BooleanField(default=False, help_text='Automatically send email to supplier and gas referrer supplier as soon as an order is closed', verbose_name='send email on order close')),
                ('is_suspended', models.BooleanField(default=False, help_text='A pact can be broken or removed by one of the partner. If it is not active no orders can be done and the pact will not appear anymore in the interface. When a pact is suspended you can specify when it could be resumed', db_index=True, verbose_name='is suspended')),
                ('suspend_datetime', models.DateTimeField(default=None, null=True, blank=True)),
                ('suspend_reason', models.TextField(default=b'', blank=True)),
                ('suspend_auto_resume', models.DateTimeField(default=None, null=True, db_index=True, blank=True)),
                ('default_delivery_place', models.ForeignKey(related_name='pact_default_delivery_place_set', verbose_name='Default delivery place', blank=True, to='base.Place', null=True)),
                ('gas', models.ForeignKey(related_name='pact_set', verbose_name='GAS', to='gas.GAS')),
            ],
            options={
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='GASSupplierStock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('minimum_amount', lib.fields.models.PrettyDecimalField(default=1, verbose_name='minimum order amount', max_digits=5, decimal_places=2)),
                ('step', lib.fields.models.PrettyDecimalField(default=1, verbose_name='step of increment', max_digits=5, decimal_places=2)),
                ('pact', models.ForeignKey(related_name='gasstock_set', to='gas.GASSupplierSolidalPact')),
                ('stock', models.ForeignKey(related_name='gasstock_set', to='supplier.SupplierStock')),
            ],
            options={
                'verbose_name': 'GAS supplier stock',
                'verbose_name_plural': 'GAS supplier stocks',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(help_text='when the order will be withdrawn by GAS members')),
                ('start_time', models.TimeField(default=b'18:00', help_text='when the withdrawal will start')),
                ('end_time', models.TimeField(default=b'22:00', help_text='when the withdrawal will end')),
                ('place', models.ForeignKey(related_name='withdrawal_set', to='base.Place', help_text='where the order will be withdrawn by GAS members')),
            ],
            options={
                'verbose_name': 'wihtdrawal',
                'verbose_name_plural': 'wihtdrawals',
            },
            bases=(models.Model, gf.base.models.PermissionResource),
        ),
        migrations.AddField(
            model_name='gassuppliersolidalpact',
            name='stock_set',
            field=models.ManyToManyField(to='supplier.SupplierStock', null=True, through='gas.GASSupplierStock', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassuppliersolidalpact',
            name='supplier',
            field=models.ForeignKey(related_name='pact_set', verbose_name='Supplier', to='supplier.Supplier'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gassuppliersolidalpact',
            unique_together=set([('gas', 'supplier')]),
        ),
        migrations.AddField(
            model_name='gassupplierorderproduct',
            name='gasstock',
            field=models.ForeignKey(related_name='orderable_product_set', verbose_name='gas stock', to='gas.GASSupplierStock'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassupplierorderproduct',
            name='order',
            field=models.ForeignKey(related_name='orderable_product_set', verbose_name='order', to='gas.GASSupplierOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassupplierorder',
            name='gasstock_set',
            field=models.ManyToManyField(help_text='products available for the order', to='gas.GASSupplierStock', verbose_name='GAS supplier stock', through='gas.GASSupplierOrderProduct', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassupplierorder',
            name='pact',
            field=models.ForeignKey(related_name='order_set', verbose_name='pact', to='gas.GASSupplierSolidalPact'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassupplierorder',
            name='referrer_person',
            field=models.ForeignKey(related_name='order_set', verbose_name='order referrer', blank=True, to='base.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassupplierorder',
            name='root_plan',
            field=models.ForeignKey(default=None, to='gas.GASSupplierOrder', blank=True, help_text='Order was generated by another order', null=True, verbose_name='planned order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassupplierorder',
            name='withdrawal',
            field=models.ForeignKey(related_name='order_set', verbose_name='Withdrawal', blank=True, to='gas.Withdrawal', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gassupplierorder',
            name='withdrawal_referrer_person',
            field=models.ForeignKey(related_name='withdrawal_for_order_set', verbose_name='withdrawal referrer', blank=True, to='base.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gasmemberorder',
            name='ordered_product',
            field=models.ForeignKey(related_name='gasmember_order_set', verbose_name='order product', to='gas.GASSupplierOrderProduct'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gasmemberorder',
            name='purchaser',
            field=models.ForeignKey(related_name='gasmember_order_set', verbose_name='purchaser', to='gas.GASMember'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gasmemberorder',
            unique_together=set([('ordered_product', 'purchaser')]),
        ),
        migrations.AlterUniqueTogether(
            name='gasmember',
            unique_together=set([('person', 'gas'), ('gas', 'id_in_gas')]),
        ),
        migrations.AddField(
            model_name='gas',
            name='activist_set',
            field=models.ManyToManyField(to='base.Person', null=True, verbose_name='GAS activists', through='gas.GASActivist', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gas',
            name='contact_set',
            field=models.ManyToManyField(to='base.Contact', null=True, verbose_name='contacts', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gas',
            name='des',
            field=models.ForeignKey(verbose_name='des', to='des.DES'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gas',
            name='headquarter',
            field=models.ForeignKey(related_name='gas_headquarter_set', verbose_name='headquarter', to='base.Place', help_text='main address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gas',
            name='orders_email_contact',
            field=models.ForeignKey(related_name='gas_use_for_orders_set', blank=True, to='base.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gas',
            name='supplier_set',
            field=models.ManyToManyField(to='supplier.Supplier', through='gas.GASSupplierSolidalPact', blank=True, help_text='Suppliers bound to the GAS through a solidal pact', null=True, verbose_name='Suppliers'),
            preserve_default=True,
        ),
    ]
