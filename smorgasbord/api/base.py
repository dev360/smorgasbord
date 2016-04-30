#coding=utf-8
from restless.models import serialize
from restless.modelviews import DetailEndpoint as BaseDetailEndpoint, ListEndpoint as BaseListEndpoint, Endpoint as BaseEndpoint


__all__ = ['serialize', 'DetailEndpoint', 'ListEndpoint', 'Endpoint']



class DetailEndpoint(BaseDetailEndpoint):
    pass



class ListEndpoint(BaseListEndpoint):
    pass



class Endpoint(BaseEndpoint):
    pass


