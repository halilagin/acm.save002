
import yaml
import io
#from  munch import Munch
#from collections import namedtuple
from acm.util.AcmHashObjectSerializer import AcmHashObjectSerializer
import json

class AcmConfigManager(object):
    pass
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self.params = params
        
    def read(self):
        configFile = self.params["config.file"]
        config = None
        with open(configFile, 'r') as stream:
            y_ = yaml.load(stream) 
            #self.config = Munch( )
            #self.config = namedtuple('Struct', y_.keys())(*y_.values())
            self.config = AcmHashObjectSerializer(y_)
        
        return self.config
        
    def write(self):
        configFile = self.params["config.file"]
        with io.open(configFile, 'w', encoding='utf8') as outfile:
            yaml.dump(self.config.__dict__, outfile, default_flow_style=False, allow_unicode=True)
        
