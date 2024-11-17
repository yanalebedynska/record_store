from django.core.exceptions import ObjectDoesNotExist

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        """Отримати всі об'єкти."""
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        """Отримати об'єкт за ID."""
        try:
            return self.model.objects.get(pk=obj_id)
        except ObjectDoesNotExist:
            return None

    def create(self, data):
        """Створити об'єкт."""
        return self.model.objects.create(**data)

    @staticmethod
    def update(obj, data):
        """Оновити об'єкт."""
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    @staticmethod
    def delete(obj):
        """Видалити об'єкт."""
        obj.delete()


    def read_all(self):
        return self.model.objects.all()