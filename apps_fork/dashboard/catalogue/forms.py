from django import forms
from apps_fork.catalogue.models import Product
from oscar.apps.dashboard.catalogue import forms as Coreforms
from django.core import exceptions


class ProductForm(forms.ModelForm):
    FIELD_FACTORIES = {
        "text": Coreforms._attr_text_field,
        "richtext": Coreforms._attr_textarea_field,
        "integer": Coreforms._attr_integer_field,
        "boolean": Coreforms._attr_boolean_field,
        "float": Coreforms._attr_float_field,
        "date": Coreforms._attr_date_field,
        "datetime": Coreforms._attr_datetime_field,
        "option": Coreforms._attr_option_field,
        "multi_option": Coreforms._attr_multi_option_field,
        "entity": Coreforms._attr_entity_field,
        "numeric": Coreforms._attr_numeric_field,
        "file": Coreforms._attr_file_field,
        "image": Coreforms._attr_image_field,
    }

    class Meta:
        model = Product
        fields = ['title', 'upc',  'description', 'partner', 'is_public', 'is_discountable', 'structure']
        widgets = {'structure': forms.HiddenInput()}

    def __init__(self, product_class, data=None, parent=None, partner=None, *args, **kwargs):
        self.set_initial(product_class, parent, kwargs)
        super().__init__(data, *args, **kwargs)

        # add partner to product instance
        # if staff can choose partner
        # if partner, cannot chose another partner
        if partner is not None:
            self.instance.partner = partner
            del self.fields['partner']


        if parent:
            self.instance.parent = parent
            # We need to set the correct product structures explicitly to pass
            # attribute validation and child product validation. Note that
            # those changes are not persisted.
            self.instance.structure = Product.CHILD
            self.instance.parent.structure = Product.PARENT

            self.delete_non_child_fields()
        else:
            # Only set product class for non-child products
            self.instance.product_class = product_class
        self.add_attribute_fields(product_class, self.instance.is_parent)

        if 'title' in self.fields:
            self.fields['title'].widget = forms.TextInput(
                attrs={'autocomplete': 'off'})

    def set_initial(self, product_class, parent, kwargs):
        """
        Set initial data for the form. Sets the correct product structure
        and fetches initial values for the dynamically constructed attribute
        fields.
        """
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        self.set_initial_attribute_values(product_class, kwargs)
        if parent:
            kwargs['initial']['structure'] = Product.CHILD

    def set_initial_attribute_values(self, product_class, kwargs):
        """
        Update the kwargs['initial'] value to have the initial values based on
        the product instance's attributes
        """
        instance = kwargs.get('instance')
        if instance is None:
            return
        for attribute in product_class.attributes.all():
            try:
                value = instance.attribute_values.get(
                    attribute=attribute).value
            except exceptions.ObjectDoesNotExist:
                pass
            else:
                kwargs['initial']['attr_%s' % attribute.code] = value

    def add_attribute_fields(self, product_class, is_parent=False):
        """
        For each attribute specified by the product class, this method
        dynamically adds form fields to the product form.
        """
        for attribute in product_class.attributes.all():
            field = self.get_attribute_field(attribute)
            if field:
                self.fields['attr_%s' % attribute.code] = field
                # Attributes are not required for a parent product
                if is_parent:
                    self.fields['attr_%s' % attribute.code].required = False

    def get_attribute_field(self, attribute):
        """
        Gets the correct form field for a given attribute type.
        """
        return self.FIELD_FACTORIES[attribute.type](attribute)

    def delete_non_child_fields(self):
        """
        Deletes any fields not needed for child products. Override this if
        you want to e.g. keep the description field.
        """
        for field_name in ['description', 'is_discountable', 'title']:
            if field_name in self.fields:
                del self.fields[field_name]

    def _post_clean(self):
        """
        Set attributes before ModelForm calls the product's clean method
        (which it does in _post_clean), which in turn validates attributes.
        """
        self.instance.attr.initiate_attributes()
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attr_%s' % attribute.code
            # An empty text field won't show up in cleaned_data.
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.code, value)
        super()._post_clean()
