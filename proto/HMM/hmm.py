"""
Python module for creating, training and applying hidden
Markov models to discrete or continuous observations.
Author: Michael Hamilton,  hamiltom@cs.colostate.edu
Theoretical concepts obtained from Rabiner, 1989.
"""

import numpy, pylab, time, copy
from numpy import random as rand
from numpy import linalg
from matplotlib import rc
rc('text', usetex=True)

class HMM_Classifier:
    """
    A binary hmm classifier that utilizes two hmms: one corresponding
    to the positive activity and one corresponding to the negative
    activity.
    """
    def __init__( self, **args ):
        """
        :Keywords:
          - `neg_hmm` - hmm corresponding to negative activity
          - `pos_hmm` - hmm corresponding to positive activity          
        """
        self.neg_hmm = None
        self.pos_hmm = None
        
        if 'neg_hmm' in args:
            self.neg_hmm = args[ 'neg_hmm' ]

        if 'pos_hmm' in args:
            self.pos_hmm = args[ 'pos_hmm' ]

    def classify( self, sample ):
        """
        Classification is performed by calculating the
        log odds for the positive activity.  Since the hmms
        return a log-likelihood (due to scaling)
        of the corresponding activity, the difference of
        the two log-likelihoods is the log odds.
        """
        # Scream if an hmm is missing
        if self.pos_hmm == None or self.neg_hmm == None:
            raise "pos/neg hmm(s) missing"

        pos_ll = forward( self.pos_hmm, sample, scaling=1 )[ 0 ]
        neg_ll = forward( self.neg_hmm, sample, scaling=1 )[ 0 ]
        
        # log odds by difference of log-likelihoods
        return  pos_ll - neg_ll
               

    def add_pos_hmm( self, pos_hmm ):
        """
        Add the hmm corresponding to positive
        activity.  Replaces current positive hmm, if it exists.
        """
        self.pos_hmm = pos_hmm

    def add_neg_hmm( self, neg_hmm ):
        """
        Add the hmm corresponding to negative
        activity.  Replaces current negative hmm, if it exists.
        """
        self.neg_hmm = neg_hmm

class HMM:
    """
    Creates and maintains a hidden Markov model.  This version assumes the every state can be
    reached DIRECTLY from any other state (ergodic).  This, of course, excludes the start state.
    Hence the state transition matrix, A, must be N X N .  The observable symbol probability
    distributions are represented by an N X M matrix where M is the number of observation
    symbols.  

                  |a_11 a_12 ... a_1N|                   |b_11 b_12 ... b_1M|   
                  |a_21 a_22 ... a_2N|                   |b_21 b_22 ... b_2M|
              A = | .    .        .  |               B = | .    .        .  |
                  | .         .   .  |                   | .         .   .  |
                  |a_N1 a_N2 ... a_NN|                   |b_N1 b_N2 ... b_NM|
          
           a_ij = P(q_t = S_j|q_t-1 = S_i)       b_ik = P(v_k at t|q_t = S_i)
        where q_t is state at time t and v_k is k_th symbol of observation sequence

                                  
    """
    def __init__( self, n_states=1, **args ):
        """
        :Keywords:
          - `n_states` - number of hidden states
          - `V` - list of all observable symbols
          - `A` - transition matrix
          - `B` - observable symbol probability distribution
          - `D` - dimensionality of continuous observations
          - `F` - Fixed emission probabilities for the given state ( dict: i -> numpy.array( [n_states] ),
                  where i is the state to hold fixed.
          """
    
        self.N = n_states # Number of hidden states

        # Initialize observable symbol set parameters
        self.V = args[ 'V' ] 
        self.M = len( self.V )
        self.symbol_map = dict( zip ( self.V, range( len( self.V ) )) )
            
            
        # Initialize transition probability matrix
        if 'A' in args:
            self.A = args[ 'A' ] 
            assert numpy.shape( self.A ) == ( self.N, self.N )
            
            
        else:
            # Randomly initialize matrix and normalize so sum over a row = 1
            raw_A = rand.uniform( size = self.N * self.N ).reshape( ( self.N, self.N ) )
            self.A = ( raw_A.T / raw_A.T.sum( 0 ) ).T  
            if n_states == 1:
                self.A.reshape( (1,1) )

        # Initialize observable symbol probability distributions
        if 'B' in args:
            self.B = args[ 'B' ]
            if n_states > 1:
                assert numpy.shape( self.B ) == ( self.N, self.M )
            else:
                self.B = numpy.reshape(self.B, (1,self.M) )

            if 'F' in args:
                self.F = args[ 'F' ]
                for i in self.F.keys():
                    self.B[ i,: ] = self.F[ i ]
            else:
                self.F = {}
                      
        else:
            # initialize distribution
            B_raw = rand.uniform( 0, 1, self.N * self.M ).reshape( ( self.N, self.M ) )
            self.B = ( B_raw.T / B_raw.T.sum( 0 ) ).T

            if 'F' in args:
                self.F = args[ 'F' ]
                for i in self.F.keys():
                    self.B[ i,: ] = self.F[ i ]
            else:
                self.F = {}


        # Initialize the intitial state distribution
        if 'Pi' in args:
            self.Pi = args[ 'Pi' ]
            assert len( self.Pi ) == self.N
        else:
            # initialize to uniform distribution
            self.Pi = numpy.array ( 1.0 / self.N ).repeat( self.N )

        if 'Labels' in args:
            self.Labels = args[ 'Labels' ]
        else:
            self.Labels = range( self.N )

        if 'F' in args:
            self.F = args[ 'F' ]
            for i in self.F.keys():
                self.B[ i,: ] = self.F[ i ]
        else:
            self.F = {}

    def __repr__( self ):
        print self.A
        retn = ""
        retn += "num hiddens: %d\n" % ( self.N ) + \
                "symbols: %s\n" % ( self.V ) + \
                "\nA:\n %s\n" % ( str( self.A ) ) + \
                "Pi:\n %s" % ( str( self.Pi ) )
        
        return retn


def symbol_index( hmm, Obs ):
    """
    Converts an obeservation symbol sequence into a sequence
    of indices for accessing distribution matrices.
    """
    Obs_ind = []
    for o in Obs: Obs_ind.append( hmm.symbol_map[ o ] )
    
    return Obs_ind


def forward( hmm, Obs, scaling=True ):
    """
    Calculate the probability of an observation sequence, Obs,
    given the model, P(Obs|hmm).
    Obs: observation sequence
    hmm: model
    returns: P(Obs|hmm)
    """
    T = len( Obs ) # Number of states in observation sequence
    
    # Get index sequence of observation sequence to access
    # the observable symbol probabilty distribution matrix

    Obs = symbol_index( hmm, Obs )
        
        
    # create scaling vector 
    if scaling:
        c = numpy.zeros( [ T ], float )
        
    # Base Case:
    Alpha = numpy.zeros( [ hmm.N, T ], float )
    
    Alpha[ :,0 ] = hmm.Pi * hmm.B[ :,Obs[ 0 ] ]
    
    if scaling:
        c[ 0 ] = 1.0 / numpy.sum( Alpha[ :,0 ] )
        Alpha[ :,0 ] = c[ 0 ] * Alpha[ :,0 ]
   
    # Induction Step:
    for t in xrange( 1,T ):
        Alpha[ :,t ] = numpy.dot( Alpha[ :,t-1 ], hmm.A) * hmm.B[ :,Obs[ t ] ]

        if scaling:
            c[ t ] =  1.0 / numpy.sum( Alpha[ :,t ] )
            Alpha[ :,t] = Alpha[ :,t]  * c[ t ]
            
    if scaling:
        
        log_Prob_Obs = -( numpy.sum( numpy.log( c ) ) )
        
        return ( log_Prob_Obs, Alpha, c )
    else:
        prob_Obs = numpy.sum( Alpha[ :,T-1 ] )
        
        return ( prob_Obs, Alpha )
            

def backward( hmm, Obs, c=None ):
    """
    Calculate the probability of a partial observation sequence
    from t+1 to T, given some state t.
    Obs: observation sequence
    hmm: model
    c: the scaling coefficients from forward algorithm
    returns: B_t(i) 
    """
    T = len( Obs ) # Number of states in observation sequence
    
    # Get index sequence of observation sequence to access
    # the observable symbol probabilty distribution matrix
    Obs = symbol_index( hmm, Obs )
    
    # Base Case:
    Beta = numpy.zeros( [ hmm.N, T ], float ) 
    Beta[ :, T-1 ] = 1.0
    if c is not None:
        Beta [ :,T-1  ] = Beta [ :,T-1 ] * c[ T-1 ]

    # Inductive Step:
    for t in reversed( xrange( T-1 ) ):
        Beta[ :,t ] = numpy.dot( hmm.A, ( hmm.B[ :,Obs[ t+1 ] ] * Beta[ :,t+1 ] ) )
            
        if c is not None:
            Beta[ :,t ] = Beta[ :,t ] * c[ t ]
            
    return Beta
            

def viterbi( hmm, Obs, scaling=True ):
    """
    Calculate P(Q|Obs, hmm) and yield the state sequence Q* that
    maximizes this probability. 
    Obs: observation sequence
    hmm: model
    """
    T = len( Obs ) # Number of states in observation sequence
        
    # Get index sequence of observation sequence to access
    # the observable symbol probabilty distribution matrix
    Obs = symbol_index( hmm, Obs )

    # Initialization
    # Delta[ i,j ] = max_q1,q2,...,qt P( q1, q2,...,qt = i, O_1, O_2,...,O_t|hmm )
    # this is the highest prob along a single path at time t ending in state S_i
    Delta = numpy.zeros( [ hmm.N,T ], float)

    if scaling:
        Delta[ :,0 ] = numpy.log( hmm.Pi ) + numpy.log( hmm.B[ :,Obs[ 0] ] )
        

    else:
        Delta[ :,0 ] = hmm.Pi * hmm.B[ :,Obs[ 0] ]
        
        
    # Track Maximal States
    Psi =  numpy.zeros( [ hmm.N, T ], int )
    
    # Inductive Step:
    if scaling:
        for t in xrange( 1,T ):
            nus =  Delta[ :,t-1 ] + numpy.log( hmm.A )
            Delta[ :,t ] =  nus.max(1) + numpy.log( hmm.B[ :,Obs[ t ] ] )
            Psi[ :,t ] = nus.argmax( 1 )
    else:
        for t in xrange( 1,T ):
            nus =  Delta[ :,t-1 ] * hmm.A
            Delta[ :,t ] = nus.max( 1 ) * hmm.B[ :,Obs[ t ] ]
            Psi[ :,t ] = nus.argmax(1)
        
    # Calculate State Sequence, Q*:
    Q_star =  [ numpy.argmax( Delta[ :,T-1 ] ) ]
    for t in reversed( xrange( T-1 ) ) :
        Q_star.insert( 0, Psi[ Q_star[ 0 ],t+1 ] )

    return ( Q_star, Delta, Psi )


def baum_welch( hmm, Obs_seqs, **args ): 
    """
    EM algorithm to update Pi, A, and B for the HMM
    :Parameters:
      - `hmm` - hmm model to train
      - `Obs_seqs` - list of observation sequences to train over
    :Return:
      a trained hmm

    :Keywords:
      - `epochs` - number of iterations to perform EM, default is 20
      - `val_set` - validation data set, not required but recommended to prevent over-fitting
      - `updatePi` - flag to update initial state probabilities
      - `updateA` - flag to update transition probabilities, default is True
      - `updateB` - flag to update observation emission probabilites for discrete types, default is True
      - `scaling` - flag to scale probabilities (log scale), default is True
      - `graph` - flag to plot log-likelihoods of the training epochs, default is False
      - `normUpdate` - flag to use 1 / -(normed log-likelihood) contribution for each observation
                       sequence when updating model parameters, default if False
      - `fname` - file name to save plot figure, default is ll.eps
      - `verbose` - flag to print training times and log likelihoods for each training epoch, default is false
    """
    # Setup keywords
    if 'epochs' in args: epochs = args[ 'epochs' ]
    else: epochs = 20
    
    updatePi=updateA=updateB=scaling=graph = 1
    normUpdate=verbose=validating = 0
    if 'updatePi' in args: updatePi = args[ 'updatePi' ]
    if 'updateA' in args: updateA = args[ 'updateA' ]
    if 'updateB' in args: updateB = args[ 'updateB' ]
    if 'scaling' in args: scaling = args[ 'scaling' ]
    if 'graph' in args: graph = args[ 'graph' ]
    if 'normUpdate' in args: normUpdate = args[ 'normUpdate' ]
    if 'fname' in args: fname = args[ 'fname' ]
    else: fname = 'll.eps'
    if 'verbose' in args: verbose = args[ 'verbose' ]
    if 'val_set' in args:
        validating = 1
        val_set = args[ 'val_set' ]
    
    K = len( Obs_seqs ) # number of observation sequences
    start = time.time() # start training timer
    LLs = []            # keep track of log likelihoods for each epoch
    val_LLs = []        # keep track of validation log-likelihoods for each epoch

    # store best parameters
    best_A = copy.deepcopy( hmm.A )
    best_B = copy.deepcopy( hmm.B )
    best_Pi = copy.deepcopy( hmm.Pi )
    best_epoch = 'N/A'
    
    best_val_LL = None
    
    # Iterate over specified number of EM epochs
    for epoch in xrange( epochs ):
        start_epoch = time.time()                                 # start epoch timer
            
        LL_epoch = 0                                              # intialize log-likelihood of all seqs given the model
        Expect_si_all = numpy.zeros( [ hmm.N ], float )           # Expectation of being in state i over all seqs
        Expect_si_all_TM1 = numpy.zeros( [ hmm.N ], float )       # Expectation of being in state i over all seqs until T-1
        Expect_si_sj_all = numpy.zeros( [ hmm.N, hmm.N ], float ) # Expectation of transitioning from state i to state j over all seqs
        Expect_si_sj_all_TM1 = numpy.zeros( [ hmm.N, hmm.N ], float )
        Expect_si_t0_all = numpy.zeros( [ hmm.N ] )               # Expectation of initially being in state i over all seqs
        Expect_si_vk_all = numpy.zeros( [ hmm.N, hmm.M ], float ) # Expectation of being in state i and seeing symbol vk
        ow = 0
        for Obs in Obs_seqs:
            if ow > 0 and ow % 100 == 0:
                print "epoch %d: %d seqs processed" % ( epoch+1, ow )
            ow += 1
            Obs = list( Obs )
            log_Prob_Obs, Alpha, c = forward( hmm=hmm, Obs=Obs, scaling=1 )  # Calculate forward probs, log-likelihood, and scaling vals
            Beta = backward( hmm=hmm, Obs=Obs, c=c )                         # Calculate backward probs
            LL_epoch += log_Prob_Obs                                         # Update overall epoch log-likelihood
            T = len( Obs )                                                   # Number of states in observation sequence

            # Determine update weight of the observation for contribution
            # to model parameter maximization
        
            if normUpdate:
                w_k = 1.0 / -( log_Prob_Obs + numpy.log( len( Obs ) ) )
            else:
                w_k = 1.0
                
            # Get index sequence of observation sequence to access
            # the observable symbol probabilty distribution matrix
            Obs_symbols = Obs[ : ]
            Obs = symbol_index( hmm, Obs )

            # Calculate gammas
            # Gamma[ i,t ] = P( q_t = S_i|Obs, hmm)
            Gamma_raw = Alpha * Beta
            Gamma = Gamma_raw / Gamma_raw.sum( 0 )
        
            Expect_si_t0_all += w_k * Gamma[ :,0 ]

            # Expect_si_all[ i ] = expected number of transitions from state i over all
            # training sequences.
            Expect_si_all += w_k * Gamma.sum( 1 )
            Expect_si_all_TM1 += w_k * Gamma[ :,:T-1 ].sum( 1 )
            
            # Calculate Xis
            # Xi is an N X N X T-1 matrix corresponding to
            # Xi[ i,j,t ] = P(q_t = S_i, q_t+1 = S_j|Obs, hmm )
            Xi = numpy.zeros( [ hmm.N, hmm.N, T-1 ], float )
                        
            for t in xrange( T-1 ):
                for i in xrange( hmm.N ):
                    Xi[ i,:,t ] = Alpha[ i,t ] * hmm.A[ i,: ] * hmm.B[ :, Obs[ t+1 ] ] * Beta[ :,t+1 ]
            
                if not scaling:
                    Xi[ :,:,t ] = Xi[ :,:,t ] / Xi[ :,:,t ].sum()

            # Expect_si_sj_all = expected number of transitions from state s_i to state s_j
            Expect_si_sj_all += w_k * Xi.sum( 2 )               #which = numpy.array( hmm.V[ k ] == numpy.array( Obs_symbols ) )
            Expect_si_sj_all_TM1 += w_k * Xi[ :,:,:T-1].sum( 2 ) 
          

            if updateB:
                B_bar = numpy.zeros( [ hmm.N, hmm.M ], float )
                for k in xrange( hmm.M ):
                    which = numpy.array( [ hmm.V[ k ] == x for x in Obs_symbols ] )
     
                    B_bar[ :,k ] = Gamma.T[ which,: ].sum( 0 )

                Expect_si_vk_all += w_k * B_bar
                
        ##############    Reestimate model parameters    ###############
        
        # reestimate initial state probabilites
        if updatePi:
            Expect_si_t0_all = Expect_si_t0_all / numpy.sum( Expect_si_t0_all )
            hmm.Pi = Expect_si_t0_all
            
        # reestimate transition probabilites
        if updateA:
            A_bar = numpy.zeros( [ hmm.N, hmm.N ], float )
            for i in xrange( hmm.N ):        
                A_bar[ i,: ] = Expect_si_sj_all_TM1[ i,: ] / Expect_si_all_TM1[ i ] 
            hmm.A = A_bar
            

        if updateB:
            # reestimate emission probabilites 
            # ( observable symbol probability distribution )
            for i in xrange( hmm.N ):
                Expect_si_vk_all[ i,: ] = Expect_si_vk_all [ i,: ] / Expect_si_all[ i ]

            hmm.B = Expect_si_vk_all

            for i in hmm.F.keys():
                hmm.B[ i,: ] = hmm.F[ i ]

        LLs.append( LL_epoch )
        

        # Quit if log_likelihoods have plateaued
        if epoch > 1:
            if LLs[ epoch - 1 ] == LL_epoch:
                print "Log-likelihoods have plateaued--terminating training"
                break
        
        # if validating, then calculate log-likelihood of validation set
        # to determine if training should be terminated.
        if validating:
            val_LL_epoch = 0
            for val_Obs in val_set:
                val_Obs = list( val_Obs )
                val_LL_epoch += forward( hmm=hmm, Obs=val_Obs, scaling=1 )[ 0 ]
            val_LLs.append( val_LL_epoch )

            # Terminate training if validation log-likelihood is worse (lower) than
            # previous epoch
            if epoch > 0:
                if val_LL_epoch > best_val_LL:
                    best_A = copy.deepcopy( hmm.A )
                    best_B = copy.deepcopy( hmm.B )
                    best_Pi = copy.deepcopy( hmm.Pi )
                    best_epoch = epoch
                    best_val_LL = val_LL_epoch
                    
            else:
                best_val_LL = val_LL_epoch
                best_epoch = 0
        if verbose:
            print "Finished epoch %d in %d secs" % ( epoch+1, int( time.time() - start_epoch ) ), LL_epoch
            if validating:
                print "Validation LL: ", val_LLs[ epoch ]
    if graph:
        if validating:
            pylab.figure()
            
            pylab.subplot( 211 )
            pylab.title( "Training Reestimation Performance" )
            pylab.xlabel( "Epochs" )
            pylab.ylabel( r"$\log( P ( O | \lambda ) )$" )
            pylab.plot( LLs,  label="Training data", color='red' )
            
            pylab.subplots_adjust( hspace=0.4 )
            pylab.subplot( 212 )
            pylab.title( "Validation Reestimation Performance" )
            pylab.plot( val_LLs, label="Validation LL", color='blue' )
            pylab.xlabel( "Epochs" )
            pylab.ylabel( r"$\log( P ( O | \lambda ) )$" )
            pylab.axvline( best_epoch, color="black", label="Lowest validation LL", linewidth=2 )
            pylab.legend( labelsep=0.01, shadow=1 , loc='lower right' )
            pylab.savefig( fname )
            
        else:
            pylab.figure()
            pylab.title( "Training Reestimation Performance" )
            pylab.xlabel( "Epochs"  )
            pylab.ylabel( r"$\log( P ( O | \lambda ) )$" )
            pylab.plot( LLs,  label="Training data", color='red' )
            pylab.savefig( fname )
                           
    print "Total training time: %d secs"  % ( int( time.time() - start ) ), "Best epoch: ", best_epoch
    if validating:
        hmm.A = best_A
        hmm.B = best_B
        hmm.Pi = best_Pi
    
    return hmm


                         
###################################################################################
################################  Example  ########################################
###################################################################################
        
def dishonest_casino_test( graph = True ):
    # create transition probability matrix
    A = numpy.array( [ [ 0.95,  0.05],[ 0.05,  0.95 ] ] )

    # create observable probability distribution matrix
    B = numpy.array( [ [ 1.0/6,  1.0/6,  1.0/6,  1.0/6,  1.0/6,  1.0/6, ], \
                       [ 1.0/10, 1.0/10, 1.0/10, 1.0/10, 1.0/10, 1.0/2 ] ] )

    # create set of all observabB = [ (-1,.1), (1,.1) ]
    A = numpy.array( [ [ 0.99, 0.01 ], \
                       [ 0.01, 0.99 ] ] )

    #le symbols
    V =[1, 2, 3, 4, 5, 6]

    # instantiate an hmm, note Pi is uniform probability distribution
    # by default
    hmm = HMM( 2, A=A, B=B, V=V )

    # adjust the precision of printing float values
    numpy.set_printoptions( precision=4 )

    
    print "\nDishonest Casino Example:\n "
    Obs = [ 1,2,1,6,6 ]
    print hmm
    print
    print '*'*80
    print '*'*80
    print "\nWithout Scaling\n"
    print "\nObservation Sequence: %s\n" % ( Obs )
    prob_Obs, Alpha = forward( hmm, Obs, scaling=0 )
    print '*'*29
    print "* Forward Algorithm Results *"
    print '*'*29 + '\n'
    print "p(Obs|hmm) ~ %.7f" % ( prob_Obs )
   
    print "Alpha's:\n %s\n" % (  Alpha   )
    print '*'*80 + '\n'
    

    Beta = backward( hmm, Obs )
    
    print '*'*30
    print "* Backward Algorithm Results *"
    print '*'*30 + '\n'
    print "Beta's:\n %s\n" % ( str( Beta ) )
    print '*'*80 + '\n'

    Q_star, Delta, Psi = viterbi( hmm, Obs, scaling=0 )

    print '*'*29
    print "* Viterbi Algorithm Results *"#Xi[ i,:,t ] =   Xi[ i,:,t ] / Xi[ i,:,: ].sum( 1 )
    print '*'*29 + '\n'
    print "Q* = %s\n" % ( Q_star )
    print "Delta's:\n %s\n" % (  Delta   )
    print "Psi:\n %s\n" % (  Psi  )
    print '*'*80 + '\n'
    
    
    print '*'*80
    print '*'*80
    print "\nWith Scaling\n"
    print "\nObservation Sequence: %s\n" % ( Obs )
    log_prob_Obs, Alpha, c = forward( hmm, Obs, scaling=1 )
    print '*'*29
    print "* Forward Algorithm Results *"
    print '*'*29 + '\n'
    print "p(Obs|hmm) ~ %.7f" % ( numpy.exp( log_prob_Obs ) )
   
    print "Alpha's:\n %s\n" % (  Alpha   )
    print '*'*80 + '\n'
    

    Beta = backward( hmm, Obs, c )
    
    print '*'*30
    print "* Backward Algorithm Results *"
    print '*'*30 + '\n'
    print "Beta's:\n %s\n" % ( str( Beta ) )
    print '*'*80 + '\n'

    Q_star, Delta, Psi = viterbi( hmm, Obs, scaling=1 )

    print '*'*29
    print "* Viterbi Algorithm Results *"
    print '*'*29 + '\n'
    print "Q* = %s\n" % ( Q_star )
    print "Delta's:\n %s\n" % (  Delta   )
    print "Psi:\n %s\n" % (  Psi  )
    print '*'*80 + '\n'
    c = []
    c.append( Obs )
    baum_welch( hmm, c, epochs=15, graph=graph )
###################################################################################
###################################################################################
###################################################################################

    
if __name__ == "__main__":
    ## # run the example, you can turn off graphing by setting it to 0
##     X = rand.uniform(0,1,10).reshape( (5,2) )
##     print norm_df(X)
     dishonest_casino_test( graph = 1 )
    
def runme():
    
	#based on Mike's DC example
	#transition probabilities 
	#A = numpy.array( [ [ 0.95,  0.05],[ 0.1,  0.90 ] ] )
	A = numpy.array( [ [.5,.5],[.5,.5]])
	#emission probabilities
	B = numpy.array( [ [ 1.0/6,  1.0/6,  1.0/6,  1.0/6,  1.0/6,  1.0/6, ], \
                      [ 1.0/10, 1.0/10, 1.0/10, 1.0/10, 1.0/10, 1.0/2 ] ] )
	#symbols
	V = [1,2,3,4,5,6]

	model = HMM(2,A=A,B=B,V=V)
	numpy.set_printoptions(precision=5)
