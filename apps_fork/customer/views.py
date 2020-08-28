from oscar.apps.customer.views import ProfileView as CoreProfileView
from oscar.core.loading import get_model

Partner = get_model("partner", "Partner")



class ProfileView(CoreProfileView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_partner'] = self.is_partner

        return ctx
        
    @property
    def is_partner(self):
        if not Partner.objects.filter(users=self.request.user):
            return False
        else:
            return True

        

