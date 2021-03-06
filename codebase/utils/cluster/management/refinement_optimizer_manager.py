from codebase.utils.cluster.general import get_opt

class RefinementOptimizerManager:

    def __init__(self, config, network_manager):

        self.config = config

        heads = network_manager.heads
        self.heads_optimizer = get_opt(config.opt)(heads.parameters(), lr=config.lr, weight_decay=config.wd)

    def fix_lr(self, optimizer, lr):
        '''
        Sets a learning rate in the optimizer
        :param optimizer: the optimizer to which to set the learning rate
        :param lr: the learning rate to set
        :return:
        '''
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
            return

        raise Exception("No 'lr' field found in the optimizer")

    def load(self, state_dict):
        '''
        Loads state from dictionary. The dictionary will contain all keys returned by calls to get_state

        :param state_dict:
        :return:
        '''
        self.heads_optimizer.load_state_dict(state_dict["heads_optimizer"])
        # Loading state overrides learning rate so we set it to the current value specified by the user
        self.fix_lr(self.heads_optimizer, self.config.lr)

    def get_state(self):
        '''
        Gets the state dictionary representing the current state of the optimizers
        :return:
        '''
        state_dict = {}

        state_dict["heads_optimizer"] = self.heads_optimizer.state_dict()

        return state_dict