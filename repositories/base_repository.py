from django.core.exceptions import ObjectDoesNotExist

class BaseRepository:
    _model = None  # Захищений атрибут для моделі

    def get_all(self):
        """Отримати всі записи моделі"""
        return self._model.objects.all()


    def create(self, **kwargs):
        """Створити новий запис"""
        return self._model.objects.create(**kwargs)


    def get_by_id(self, pk):
        """Захищений метод для пошуку по ID"""
        try:
            return self._model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None


    def delete_by_id(self, pk):
        """Видалити запис по ID"""
        try:
            instance = self._model.objects.get(pk=pk)
            instance.delete()
            return instance
        except ObjectDoesNotExist:
            return None


    def read_all(self):
        return self._model.objects.all()


    def update(self, pk, **kwargs):
        """Оновити запис по ID"""
        try:
            instance = self._model.objects.get(pk=pk)
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except ObjectDoesNotExist:
            return None