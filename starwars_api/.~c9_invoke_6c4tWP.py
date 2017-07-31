from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError
import six

api_client = SWAPIClient()

class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        self.json_data=json_data
        for key, value in six.iteritems(json_data):
            setattr(self, str(key), value)

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        Judith: I think this method should read the data and have a way to page
        until the end of count: 
        Then it should append the results from each page 
        """
        for ind, value in enumerate(self.json_data):
        for ind, value in enumerate(self.json_data):
          while ind <self.jason_data["count"]:
             next_page=requests.get(self.json_data["next"])
             

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        pass


class People(BaseModel):
    """Representing a single person"""
    
    
    pass


class Films(BaseModel):
    """Representing a single film"""
    pass


class BaseQuerySet(object):

    def __init__(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        pass

    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        pass


class PeopleQuerySet(BaseQuerySet):
    pass


class FilmsQuerySet(BaseQuerySet):
    pass
