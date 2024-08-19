from rest_framework.serializers import ModelSerializer,ReadOnlyField,CharField
from .models import Task
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','password']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'])
        return user
    
class TaskSerializer(ModelSerializer):
    username1 = ReadOnlyField(source='username.username')
    class Meta:
        model = Task
        fields = ['id','title','description','priority','status','username1']