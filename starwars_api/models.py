from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError
import six
import requests


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
        
        JUDITH - we need to add code here to check that the 'resource_id'
        exists, i.e. we need to handle the error cases in the test_models file
        """
    
        resource_name = cls.__name__.lower()
        try:
            resp = getattr(api_client, 'get_' + resource_name)(resource_id)
        
        except SWAPIClientError():
            
            return
        
        else:
            data = cls(resp)
            return data

    @classmethod
    def all(cls):
    
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        
        """
        resource_name = cls.__name__.lower()
        return BaseQuerySet(cls, resource_name)



class People(BaseModel):
    """Representing a single person """

class Films(BaseModel):
    """Representing a single film"""


class BaseQuerySet(object):
    def __init__(self, cls, resource_name):
        self.res_name = resource_name
        self.cls = cls
        self.resp = getattr(api_client, 'get_'+resource_name)()
        self.retrieved_elems = self.resp['results']
        self.next_elem = 0
        self.next_page = 2
        # so now self.resp is dictionary, with all resources in self.resp['results']
        # individual records accessed by resource_id, i.e. self.resp['results'][resource_id]
        # self.resp.count is the total number of records for this resource
        # self.resp.next is the URL of the next page (or null if this is last page)
        # self.resp.previous is URL of the previous page (or null if this is first page)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        if self.next_elem > (len(self.retrieved_elems)-1):
            
            try:
                self.resp = getattr(api_client, 'get_'+self.res_name)(**{'page': self.next_page})
            
            except:
                raise StopIteration
            
            else:
                self.retrieved_elems = self.resp['results']     # convert data to objects and store
                self.next_page += 1
                self.next_elem = 0
                
        """ THIS COMMENTED CODE EXECUTES BUT DOESN'T HANDLE ERRORS CORRECTLY
            if self.next_page == 2:    #self.resp['next'] is null:   # condition - error retrieving:
                raise StopIteration
            else:
                #         resp = self.api_client.get_people(**{'page': 2})
                self.resp = getattr(api_client, 'get_'+self.res_name)("**{'page': "+str(self.next_page)+"}")
                self.retrieved_elems = self.resp['results']     # convert data to objects and store
                self.next_page += 1
                self.next_elem = 0
        """        
        next_data = self.retrieved_elems[self.next_elem]      # get next elem
        self.next_elem += 1                                   # increase position of next elem
    
        return self.cls(next_data)


    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        return self.resp['count']


class PeopleQuerySet(BaseQuerySet):
    pass


class FilmsQuerySet(BaseQuerySet):
    pass
