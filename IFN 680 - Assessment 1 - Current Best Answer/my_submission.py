'''

2017 IFN680 Assignment

Instructions: 
    - You should implement the class PatternPosePopulation

'''

import numpy as np
import matplotlib.pyplot as plt


import pattern_utils
import population_search
import os
import logging
#------------------------------------------------------------------------------

class PatternPosePopulation(population_search.Population):
    '''
    
    '''
    def __init__(self, W, pat):
        '''
        Constructor. Simply pass the initial population to the parent
        class constructor.
        @param
          W : initial population
        '''
        self.pat = pat
        super().__init__(W)
    
    def evaluate(self):
        '''
        Evaluate the cost of each individual.
        Store the result in self.C
        That is, self.C[i] is the cost of the ith individual.
        Keep track of the best individual seen so far in 
            self.best_w 
            self.best_cost 
        @return 
           best cost of this generation            
        
        '''
        self.best_w = self.W[0].copy()
        for i in range(len(self.C)):#for every element in the hight of the matrix
            self.C[i], temp = self.pat.evaluate(self.distance_image,self.W[i,:])  # Evalueate pattern with params W against distance image to get value C[i]
            if self.best_cost > self.C[i]: # If a new best cost is found
                self.best_cost = self.C[i]
                self.best_w = self.W[i].copy()
            #print(temp)
        
        return self.best_cost
        	# INSERT YOUR CODE HERE

    def mutate(self):
        '''
        Mutate each individual.
        The x and y coords should be mutated by adding with equal probability 
        -1, 0 or +1. That is, with probability 1/3 x is unchanged, with probability
        1/3 it is decremented by 1 and with the same probability it is 
        incremented by 1.
        The angle should be mutated by adding the equivalent of 1 degree in radians.
        The mutation for the scale coefficient is the same as for the x and y coords.
        @post:
          self.W has been mutated.
        '''
        #generate array of random -1 to 1, in shape of W
#        mutations = np.random.choice([-1., 0., 1.], self.W.shape)
        mutations = np.random.choice([-1., 0., 1.], self.W.shape, p=[1/3, 1/3, 1/3])
        # convert theta column to radians
        mutations[:,2] *= np.pi/180
        # Add mutation values to W
        self.W += mutations         
                
    def set_distance_image(self, distance_image):
        self.distance_image = distance_image

#------------------------------------------------------------------------------        

def initial_population(region, scale = 10, pop_size=20):
    '''
    
    '''        
    # initial population: exploit info from region
    rmx, rMx, rmy, rMy = region
    W = np.concatenate( (
                 np.random.uniform(low=rmx,high=rMx, size=(pop_size,1)) ,
                 np.random.uniform(low=rmy,high=rMy, size=(pop_size,1)) ,
                 np.random.uniform(low=-np.pi,high=np.pi, size=(pop_size,1)) ,
                 np.ones((pop_size,1))*scale
                 #np.random.uniform(low=scale*0.9, high= scale*1.1, size=(pop_size,1))
                        ), axis=1)    
    return W

#------------------------------------------------------------------------------        
def test_particle_filter_search(generation,individuals, IndexPattern, times):
    '''
    Run the particle filter search on test image 1 or image 2of the pattern_utils module
    
    '''
    testname = str(times) +':'+ str(IndexPattern) + ':'+ str(generation) + ' x ' + str(individuals)    
    Testlogfile = str(times) +'-'+ str(IndexPattern) + '-'+ str(generation) + '_x_' + str(individuals)
    print(testname) 
    
    if os.path.exists('log') is False:
        os.mkdir('log')  
 
    logfile =  str(IndexPattern) + '-'+ str(generation) + '_x_' + str(individuals)+'.log'
    log_path = os.path.join('log',logfile)
    log_level = logging.DEBUG 
    log_format = '%(message)s'
    logger = logging.root
    logger.basicConfig = logging.basicConfig(format=log_format, filename=log_path, level=log_level)  
    logger.debug(testname)  


    if True:
        # use image 1
        imf, imd , pat_list, pose_list = pattern_utils.make_test_image_1(True)
        ipat = IndexPattern # index of the pattern to target
    else:
        # use image 2
        imf, imd , pat_list, pose_list = pattern_utils.make_test_image_2(True)
        ipat = 0 # index of the pattern to target
        
    # Narrow the initial search region
    pat = pat_list[ipat] #  (100,30, np.pi/3,40),
    #    print(pat)
    xs, ys = pose_list[ipat][:2]
    region = (xs-20, xs+20, ys-20, ys+20)
    scale = pose_list[ipat][3]
        
    pop_size=individuals
    W = initial_population(region, scale , pop_size)
    
    pop = PatternPosePopulation(W, pat)
    pop.set_distance_image(imd)
    
    pop.temperature = 5
    
    #Dictionary to convert pattern value to string
    patDict = {0:"Small Square",1:"Large Square",2:"Large Triangle",3:"Small Triangle"}
    
    # Create Paths for outputs
    # Creaet Output Folder
    if os.path.exists('out') is False:
        os.mkdir('out') 
     
    # Create 'Pat' Folder
    if os.path.exists('out\\'+patDict[IndexPattern]) is False:
        os.mkdir('out\\'+patDict[IndexPattern]) 
        
    # Create Gen vs Pop folder
    if os.path.exists('out\\'+patDict[IndexPattern]+'\\'+str(generation)+"x"+str(individuals)) is False:
        os.mkdir('out\\'+patDict[IndexPattern]+'\\'+str(generation)+"x"+str(individuals))
        
    Lw, Lc = pop.particle_filter_search(generation,log=True)
    
    

    
    plt.plot(Lc)
    plt.title('Cost vs generation index')	
    plt.savefig(r'out\\'+patDict[IndexPattern]+'\\'+str(generation)+'x'+str(individuals)+'\\'+str(times)+'_'+str(generation) +'x'+str(individuals)+'Cost_Vs_Generation.png')
   #plt.show()
    
    #print(pop.best_w)
    #print(pop.best_cost)
    logger.debug(pop.best_w)
    logger.debug(pop.best_cost)
        
    pattern_utils.display_solution(pat_list, 
                      pose_list, 
                      pat,
                      pop.best_w)
                      
#    pattern_utils.replay_search(pat_list, 
#                      pose_list, 
#                      pat,
#                      Lw)

   # os.rename('out', str(times)+'_'+ str(IndexPattern)+'_'+str(generation)+'_'+str(individuals)) 
    
#------------------------------------------------------------------------------        

if __name__=='__main__':
    
    
    Reverse_flag = False    
 
    
   # for i  in range(1, 3):
   #     print (str(i) + ':' + str(IndexPattern) + ':'+ str(population) + 'x' + str(generation))
   #     test_particle_filter_search(generation,population, IndexPattern,i)

    pop = [100]#,200,300,400,500] # Table of Populations to compare
    gen = [100]#,200,300,400,500] # Table of Generations to compare
    
#############################################################################################
    for pi in range(2):
        for ipop in range (len(pop)):  
            for igen in range(len(gen)):    
                for i  in range(1, 11):
                    print (str(i) + ':' + str(pi) + ':'+ str(pop[ipop]) + 'x' + str(gen[igen]))
                    test_particle_filter_search(gen[igen],pop[ipop], pi,i)

   
    
#############################################################################################

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                               CODE CEMETARY        
    
#        
#    def test_2():
#        '''
#        Run the particle filter search on test image 2 of the pattern_utils module
#        
#        '''
#        imf, imd , pat_list, pose_list = pattern_utils.make_test_image_2(False)
#        pat = pat_list[0]
#        
#        #region = (100,150,40,60)
#        xs, ys = pose_list[0][:2]
#        region = (xs-20, xs+20, ys-20, ys+20)
#        
#        W = initial_population_2(region, scale = 30, pop_size=40)
#        
#        pop = PatternPosePopulation(W, pat)
#        pop.set_distance_image(imd)
#        
#        pop.temperature = 5
#        
#        Lw, Lc = pop.particle_filter_search(40,log=True)
#        
#        plt.plot(Lc)
#        plt.title('Cost vs generation index')
#        plt.show()
#        
#        print(pop.best_w)
#        print(pop.best_cost)
#        
#        
#        
#        pattern_utils.display_solution(pat_list, 
#                          pose_list, 
#                          pat,
#                          pop.best_w)
#                          
#        pattern_utils.replay_search(pat_list, 
#                          pose_list, 
#                          pat,
#                          Lw)
#    
#    #------------------------------------------------------------------------------        
#        
    