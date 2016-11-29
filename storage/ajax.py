'''
Created on 21/ott/2015

@author: Andrea
'''

import json
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def sayhello(request):
    return json.dumps({'message': 'Hello World'})
