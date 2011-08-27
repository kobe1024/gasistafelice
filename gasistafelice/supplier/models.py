"""These models include information about Products, Suppliers, Producers.

These are fundamental DES data to rely on. They represent market offering.

Models here rely on base model classes.

Definition: `Vocabolario - Fornitori <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#Fornitori>`__ (ITA only)
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from history.models import HistoricalRecords

from gasistafelice.base.const import SUPPLIER_FLAVOUR_LIST, ALWAYS_AVAILABLE
from gasistafelice.base.models import Resource, PermissionResource, Person, Place
from gasistafelice.base.fields import CurrencyField
from gasistafelice.des.models import DES

from gasistafelice.auth import SUPPLIER_REFERRER
from gasistafelice.auth.utils import register_parametric_role

class Supplier(models.Model, PermissionResource):
    """An actor having a stock of Products for sale to the DES."""

    name = models.CharField(max_length=128) 
    seat =  models.ForeignKey(Place, null=True, blank=True)
    vat_number =  models.CharField(max_length=128, unique=True, null=True) #TODO: perhaps a custom field needed here ? (for validation purposes)
    website =  models.URLField(verify_exists=True, blank=True)
    referrer_set = models.ManyToManyField(Person, through="SupplierReferrer") 
    flavour = models.CharField(max_length=128, choices=SUPPLIER_FLAVOUR_LIST, default=SUPPLIER_FLAVOUR_LIST[0][0])
    certifications = models.ManyToManyField('Certification', null=True, blank=True)

    des = models.ManyToManyField(DES, null=True, blank=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.name

    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.pk)

    @property
    def supplier(self):
        return self

    @property
    def referrers(self):
        return self.referrer_set.all()

    @property
    def stocks(self):
        return self.stock_set.all()

    # the set of products provided by this Supplier to every GAS
    @property
    def product_catalog(self):
        return [s.product for s in SupplierStock.objects.filter(supplier=self)]

    def setup_roles(self):
    #    # register a new `SUPPLIER_REFERRER` Role for this Supplier
         register_parametric_role(name=SUPPLIER_REFERRER, supplier=self)

    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv   


class SupplierReferrer(models.Model, PermissionResource):
    supplier = models.ForeignKey(Supplier)
    person = models.ForeignKey(Person)
    job_title = models.CharField(max_length=256, blank=True)
    job_description = models.TextField(blank=True)
    
    history = HistoricalRecords()

    
    def setup_roles(self):
        # automatically add a new SupplierReferrer to the `SUPPLIER_REFERRER` Role
        user = self.person.user
        #FIXME: ValueError: Cannot assign "(<Role: SUPPLIER_REFERRER>, False)": "ParamRole.role" must be a "Role" instance.
        #role = register_parametric_role(name=SUPPLIER_REFERRER, supplier=self.supplier)
        #role.add_principal(user)     
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
    
class Certification(models.Model, PermissionResource):
    name = models.CharField(max_length=128, unique=True) 
    description = models.TextField(blank=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.name
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

class ProductCategory(models.Model, PermissionResource):
    # Proposal: the name is in the form MAINCATEGORY::SUBCATEGORY
    # like sourceforge categories
    name = models.CharField(max_length=128, unique=True, blank=False)
    description = models.TextField(blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = _("Product categories")

    def __unicode__(self):
        return self.name
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

class ProductMU(models.Model, PermissionResource):
    """Measurement unit for a Product."""
    # Implemented as a separated entity like GasDotto software.
    # Each SupplierReferrer has to be able to create its own measurement units.
    
    name = models.CharField(max_length=32, unique=True, blank=False)
    symbol = models.CharField(max_length=5, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.symbol
    
    class Meta():
        verbose_name="measurement unit"
        verbose_name_plural="measurement units"
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv
    
class Product(models.Model, PermissionResource):

    # COMMENT: some producer don't have product codification. 
    # That's why uuid could be blank AND null. See save() method
    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, verbose_name='UUID', help_text=_("Product code"))
    producer = models.ForeignKey(Supplier, related_name="produced_product_set")
    # Resource API
    category = models.ForeignKey(ProductCategory, null=True, blank=True, related_name="product_set")
    mu = models.ForeignKey(ProductMU, blank=True, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    
    history = HistoricalRecords()
    
    def __unicode__(self):
        return self.name

    @property
    def referrers(self):
        return self.producer.referrers
    
    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

    def save(self, *args, **kw):
        # If uuid is blank, make it NULL
        if not self.uuid:
            self.uuid = None
        return super(Product, self).save(*args, **kw)

    # Resource API
    #def categories(self):
    #    # A product belongs to one category
    #    return self.category

    # Resource API
    #@property
    #def suppliers(self):

class SupplierStock(models.Model, PermissionResource):
    """A Product that a Supplier offers in the DES marketplace.
        
       Includes price, order constraints and availability information.          
    """

    # Resource API
    supplier = models.ForeignKey(Supplier, related_name="stock_set")
    # Resource API
    product = models.ForeignKey(Product, related_name="stock_set")
    price = CurrencyField()
    code = models.CharField(max_length=128, null=True, blank=True, help_text=_("Product supplier identifier"))
    amount_available = models.PositiveIntegerField(default=ALWAYS_AVAILABLE)
    ## constraints posed by the Supplier on orders issued by *every* GAS
    # minimum amount of Product units a GAS is able to order 
    #COMMENT: minimum amount of Product units a GASMember is able to order 
    order_minimum_amount = models.PositiveIntegerField(null=True, blank=True)
    # increment step (in Product units) for amounts exceeding minimum; 
    # useful when a Product ships in packages containing multiple units.
    order_step = models.PositiveSmallIntegerField(null=True, blank=True)
    #TODO: Field for Product units per box
    # how the Product will be delivered
    delivery_terms = models.TextField(null=True, blank=True) #FIXME: find a better name for this attribute 

    history = HistoricalRecords()

    class Meta:
        unique_together = (('code', 'supplier'),)
    
    def __unicode__(self):
        return "%s (by %s)" % (self.product, self.supplier)

    @property
    def producer(self):
        return self.product.producer
    
    @property
    def availability(self):
        return bool(self.amount_available)

    @property        
    def local_grants(self):
        rv = (
              # permission specs go here
              )     
        return rv

    def save(self, *args, **kwargs):
        # if `code` is set to an empty string, set it to `None`, instead, before saving,
        # so it's stored as NULL in the DB, avoiding integrity issues.
        if not self.code:
            self.code = None
        super(SupplierStock, self).save(*args, **kwargs)


    # Resource API
    #@property
    #def suppliers(self):

class SupplierProductCategory(models.Model):
    """Map supplier categories to product categories with an optional alias.

    This is useful to know WHICH categories a suppplier CAN sell,
    and so limiting the choice in product selections."""

    category = models.ForeignKey(ProductCategory)
    supplier = models.ForeignKey(Supplier)
    alias = models.CharField(verbose_name=_('Alternative name'), max_length=128, blank=True)

    @property
    def name(self):
        return self.alias or self.category.name
 
    def __unicode__(self):
        return self.name

