from rest_framework import serializers
from uuid import UUID
from datetime import datetime
from collections import OrderedDict

class RawQuerySerializer(serializers.Serializer):
    def generate_fields(self, data):
        get_fields_ordered = list(OrderedDict.fromkeys(self.get_fields()))  # Fields specified in 'get_fields'
        meta_exclude = self.get_meta_exclude()  # Fields to be excluded from Meta

        if not data:
            return []

        # Get the fields from the 'Meta' class or from the first data dictionary
        model_fields = self.get_meta_fields() or list(data[0].keys())

        for model_field in model_fields:
            # if model_field not in list(data[0].keys()):
            #     raise serializers.ValidationError(f"Field '{model_field}' is not present in the provided data.")

            if model_field not in get_fields_ordered and model_field not in meta_exclude:
                # Determine the field type based on the data type in the first dictionary
                field_type = serializers.CharField()

                # Mapping between Python types and Django model field types
                type_mapping = {
                    int: serializers.IntegerField,
                    float: serializers.FloatField,
                    str: serializers.CharField,
                    bool: serializers.BooleanField,
                    UUID: serializers.UUIDField,
                    datetime: serializers.DateTimeField,
                    list: serializers.ListField,
                    dict: serializers.DictField,
                    # Add more mappings as needed
                }

                python_type = type(data[0][model_field])
                if python_type in type_mapping:
                    field_type = type_mapping[python_type]()

                self.fields[model_field] = field_type
                
        # Remove fields that are not in get_fields_ordered and not in meta_exclude
        for get_field in get_fields_ordered:
            if get_field not in model_fields and get_field not in meta_exclude:
                del self.fields[get_field]

        # Check for fields in meta_exclude that are not in the data
        for except_field in meta_exclude:
            if except_field not in model_fields:
                raise serializers.ValidationError(f"Field '{except_field}' is listed in meta_exclude but not present in the provided data.")

        return model_fields

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.generate_fields(data)

    def get_meta_fields(self):
        # Check if the 'Meta' attribute exists in the class and has the 'fields' attribute
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'fields'):
            return self.Meta.fields
        else:
            return None

    def get_meta_exclude(self):
        # Check if the 'Meta' attribute exists in the class and has the 'exclude' attribute
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'exclude'):
            return self.Meta.exclude
        else:
            return []

    def the_update_fields(self, instance):
        updated_values = {}
        if hasattr(self, 'update_fields') and callable(getattr(self, 'update_fields', None)):
            if instance is not None:
                updated_fields = self.update_fields(getField=lambda field_name, default=None: instance.get(field_name, default))
                for field, updated_value in OrderedDict(updated_fields).items():
                    updated_values[field] = updated_value
        return updated_values
    
    def the_bind_relations(self, instance):
        updated_values = {}
        if hasattr(self, 'bind_relations') and callable(getattr(self, 'bind_relations', None)):
            if instance is not None:
                updated_fields = self.bind_relations(getField=lambda field_name, default=None: instance.get(field_name, default))
                for field, updated_value in OrderedDict(updated_fields).items():
                    updated_values[field] = updated_value
        return updated_values
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        updated_fields = self.the_update_fields(instance)
        
        for field, value in OrderedDict(updated_fields).items():
            representation[field] = value
            
        for field, value in OrderedDict(self.the_bind_relations(instance)).items():
            representation[field] = value
            
        return representation
