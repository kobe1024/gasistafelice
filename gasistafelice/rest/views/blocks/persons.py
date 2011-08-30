from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockWithList, ResourceBlockAction
from gasistafelice.auth import CREATE
from gasistafelice.base.models import Person

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockWithList):

    BLOCK_NAME = "persons"
    BLOCK_DESCRIPTION = _("People")
    BLOCK_VALID_RESOURCE_TYPES = ["site"] 

    def _get_resource_list(self, request):
        return request.resource.persons

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(CREATE, obj=Person):
            user_actions.append( 
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=CREATE, verbose_name=_("Add person"), 
                    url=urlresolvers.reverse('admin:base_person_add')
                )
            )

        return user_actions
        
    def _get_add_form_class(self):
        raise NotImplementedError("The add form page in use now is the admin interface page.")
