from rest_framework.serializers import ModelSerializer
from talon.models import Branch, Organization, Talon


class BranchGetSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']


class OrganizationGetSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']


class TalonCreateSerializer(ModelSerializer):
    class Meta:
        model = Talon
        fields = '__all__'


class TalonUpdateSerializer(ModelSerializer):
    class Meta:
        model = Talon
        fields = '__all__'
