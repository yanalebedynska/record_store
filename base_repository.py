from django.core.exceptions import ObjectDoesNotExist

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        try:
            return self.model.objects.get(pk=obj_id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)


    @staticmethod
    def update(obj, data):
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    @staticmethod
    def delete(obj):
        obj.delete()


    def read_all(self):
        return self.model.objects.all()