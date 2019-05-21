'''
Created on May 7, 2019

@author: Jordan
'''


class MonteCarlo(object):
    
    '''
    The Limited Depth Monte Carlo Tree Search. Takes a root node in its 
    constructor as the first node in the tree. 
    '''
    def __init__(self, root):
        self.initial_node = root
    
    '''
    Perform simulations up until the given limit supplied as a parameter. 
    For each iteration select a node to expand based on the UCT formula,
    Expand that node, 
    Then perform a rollout until a terminal state or 
    the required depth has been reached.
    Finally, backpropogates the results through the tree and 
    selects the best action after all simulations have been completed. 
    '''
    def best_action(self, num_simulations):
        
        for sim in range(0, num_simulations):
            selected_node = self.expand_tree()
            simulation_result = selected_node.rollout()
            selected_node.backpropogate(simulation_result)

        best_choice_node = self.initial_node.best_child(c_param = 0)
        return best_choice_node.generated_by
    
    '''
    Traverse through the tree to a node that has not been fully expanded, 
    Prioritising the best child at each level of the tree to traverse. 
    '''
    def traverse(self):
        node = self.initial_node
        while node.has_children() and node.untried_actions == []:
            node = node.best_child(c_param = 0.7)
        return node
    
    '''
    Expands the tree at the current node if it has not been fully expanded. 
    '''
    def expand_tree(self):
        current_node = self.traverse()
        if current_node.fully_expanded() == False:
            return current_node.expand()
        else:
            return current_node