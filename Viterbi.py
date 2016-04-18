'''
Brendan Frick	bjf062
Shlok Amin	saq665
'''
class viterbi:
    '''
        Run viterbi algorithm to solve for markov chains
        Example from website on Piazza resources

        Run with:
            v = viterbi()
            v.label(v.data)
        
    '''

    def __init__(self):
            '''
                Initialize to website example for a Markov model
            '''

            self.states = ['Sunny','Cloudy','Rainy']
            self.features = ['word']
            self.priors = {'Sunny' : 0.333, 'Cloudy' : 0.333, 'Rainy' : 0.333} # pi = prior probs
            self.transition = {'Sunny' : {'Sunny' : .5, 'Cloudy' : .25, 'Rainy' : .25}, 'Cloudy' : {'Sunny' : .375, 'Cloudy' : .125, 'Rainy' : .375},'Rainy' : {'Sunny' : .125, 'Cloudy' : .675, 'Rainy' : .375}}
            self.evidence = {'Sunny' : {"word" : {'Dry' : .6, "Dryish" : .2, "Damp" : .15, "Soggy": .05}},'Cloudy' : {"word" : {'Dry' : .25, "Dryish" : .25, "Damp" : .25, "Soggy": .25}},'Rainy' : {"word" : {'Dry' : .05, "Dryish" : .1, "Damp" : .35, "Soggy": .5}}}

            self.data = ["Dry","Soggy","Dryish","Soggy","Dry","Soggy"]
            
    def label( self, data ):
            ''' Find the most likely labels for the sequence of data
                This is an implementation of the Viterbi algorithm'''
            result = []

            
            n = len(data)
            if n == 0:
                print "No data"
                return []

            delta = {}
            # Find starting state probability (NO transition)
            for state in self.states:
                #Calculate change in probability
                delta[state] = self.priors[state] * self.evidence[state]['word'][data[0]]
            

            pre = []
            max_state = None

            ## Run through all instances in data
            for index in range(1, n):
                delta_new = {} ## The probability value for the current state
                pre_state = {} ## The state before this based on max delta_new

                ## Find the next state
                for state_to in self.states:
                    max_prob = 0
                    max_state = None

                    ## Find the highest probability next state based on transition probability and evidence(delta) of next state
                    for state_from in self.states:
                        prob = delta[state_from] * self.transition[state_from][state_to] #Define probability of moving from current state to next state
                        if prob > max_prob:
                            max_prob = prob
                            max_state = state_from
                    ## Save the transition prob to next state * evidence of said state (will use to calculate max probability of the next state movement
                    delta_new[state_to] = max_prob * self.evidence[state_to]['word'][data[index]] # Save probability of state to key state (factoring in feature scores)
                    pre_state[state_to] = max_state #Save most probable pre-state
                delta = delta_new # Set next state
                pre.append(pre_state) # Add to pre states

            max_state = None
            max_prob = 0
            #Find max state for last state
            for state in self.states:
                if delta[state] > max_prob:
                    max_prob = delta[state]
                    max_state = state

            if max_state is None:
                return []

            ## Go to end and trace back by pulling from pre
            ## i.e.: Finding the most probable path to the last state
            result = [max_state]
            for index in xrange(n-1, 0, -1):
                max_state = pre[index - 1][max_state]
                result.insert(0, max_state)
                
            return result
