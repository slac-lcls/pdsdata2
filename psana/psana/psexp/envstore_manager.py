from psana.psexp.envstore import EnvStore
from psana.dgram import Dgram

class EnvStoreManager(object):
    """ Manages envStore.
    Stores list of envStores (created according to given keywords e.g 'epics')
    and update the stores with list of views.
    """
    stores = {}
    
    def __init__(self, configs, *args):
        self.configs = configs
        for arg in args:
            self.stores[arg] = EnvStore(configs, arg)
    
    def update_by_event(self, evt):
        if not evt:
            return
        for i, d in enumerate(evt._dgrams):
            for key, val in d.__dict__.items():
                if key in self.stores:
                    self.stores[key].add_to(d, i)

    def update_by_views(self, views):
        if not views:
            return
        for i in range(len(views)):
            view = bytearray(views[i])
            offset = 0
            while offset < memoryview(view).shape[0]:
                d = Dgram(view=view, config=self.configs[i], offset=offset)
                for key, val in d.__dict__.items():
                    if key in self.stores:
                        self.stores[key].add_to(d, i)
                    
                offset += d._size
                    
    def alg_from_variable(self, variable_name):
        for alg, store in self.stores.items():
            found_alg = store.alg_from_variable(variable_name)
            if found_alg:
                return found_alg
        return None

    def get_info(self, alg):
        store = self.stores[alg]
        variables = store.env_variables[alg]
        info = {}
        for var in variables:
            info[(var, alg)] = alg
        return info
    


        
        