class CommonServices:
    @staticmethod
    def create_slag(obj):
        slug = obj.name.strip()
        slug = slug.lower()
        return slug.replace(' ', '-')
