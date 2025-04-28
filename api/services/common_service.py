class CommonService:
    """
    A service class that provides common utility functions.
    """

    model = None

    @classmethod
    def query(cls, cols, reverse=None, order_by=None, **kwargs):
        """
        Query the database with the given parameters.
        """
        return cls.model.query(cols, reverse=reverse, order_by=order_by, **kwargs)


    @classmethod
    def get_all(cls,

