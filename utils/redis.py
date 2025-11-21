from django.core.cache import cache


class Redis:

    @classmethod
    def get_key(cls, key):
        return cache.get(key)

    @classmethod
    def set_key(cls, key, value, minutes=0, hours=0):
        seconds = minutes * 60 + hours * 3600 if (minutes or hours) else None
        return cache.set(key, value, seconds)

    @classmethod
    def delete_key(cls, key):
        return cache.delete(key)
