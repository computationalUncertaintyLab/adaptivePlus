#mcandrew

class adaptiveEnsemble(object):
    def __init__(self,scores,logscore=True,weight=1):
        self.scores   = scores
        self.logscore = logscore
        self.rho      = weight 

        self.M = self.numModels()

    def numModels(self):
        return len(self.scores.component_model_id.unique())

    def buildProbMatrix(self):
        import pandas as pd
        import numpy as np
        
        scoresOnly = self.scores[["Location","Target","MW","component_model_id","logscore"]]
        
        scoresMatrix = pd.pivot_table(scoresOnly,index=["Location","Target","MW"],columns=["component_model_id"],values="logscore")
        scoresMatrix = scoresMatrix.replace(-np.inf,-10.) # It is a convention to replace -infinity with a negative finite number (-10)
        scoresMatrix[scoresMatrix<-10] = -10              # It is a convention to replace values < -10 with a negative finite number (-10)
        
        probMatrix   = np.exp(scoresMatrix)
        #probMatrix   = np.exp(scoresMatrix.to_numpy())
        #probMatrix   = probMatrix/probMatrix.sum(1).reshape(-1,1)

        self.scoresMatrix = scoresMatrix
        self.probMatrix   = probMatrix

        self.N = len(self.probMatrix)
        
    def train(self):
        import pymc3 as pm
        from theano import theano, tensor as tt

        import numpy as np 
        import pandas as pd

        self.buildProbMatrix()
        
        #Theano loglikelihood
        def loglik(P, pis):
            return tt.sum(tt.log(pm.math.dot(P, pis)))

        LL = lambda pis: loglik(self.probMatrix,pis)
        
        # This is our model. We sample weights from a Dirichlet distribution and use our Loglikelihood as a filter
        with pm.Model() as model:
            # prior
            pi = pm.Dirichlet("pi",a=[self.rho*self.N/self.M]*self.M)
            pi = pi.reshape((self.M,1))

            pm.DensityDist("loglik", logp=LL, shape=self.M, observed = pi ) # Here is where our Loglikelihood is used

            trace = pm.sample( 10**4, tune=2*10**3, chains=4, progressbar=False,pickle_backend='dill',mp_ctx="forkserver" )

        self.trace=trace

    def computeWeightStats(self):
        pis = self.trace.get_values("pi")

        quantiles = [2.5,10,25,50,75,90,97.5]
        
        means = pis.mean(0)
        component_model_ids = sorted(self.probMatrix.columns)

        means = pd.DataFrame({"component_model_id":component_model_ids,"mean":means})

        quantileMatrix = pd.DataFrame(np.percentile(pis,quantiles,axis=0))
        quantileMatrix.index = quantiles

        quantileMatrix = quantileMatrix.reset_index().melt(id_vars="index")
        quantileMatrix = quantileMatrix.rename(columns={"index":"quantile","variable":"component_model_id","value":"quantileValue"})

        return means,quantileMatrix
        
