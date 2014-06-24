#Wikienergy Deep Dive 1
_____________________________
##Outline
- Goals
  - tool for evaluating energy-saving interventions
  - accurate energy disaggregator (15 minutes)
- Data Sources
  - Pecan Street
  - Tracebase
  - Weather
  - [Oak Park]
- Algorithms
  - FHMM
  - Neural Networks
- Analysis
  - eV Analytics
  - Weather vs. Energy Usage
  - % HVAC
  - Most Common Appliances
 _____________________________

##Data Sources

###Pecan Street

####Overview
- 23 cities
- disaggregated ground truth
- ~70 unique appliances
  - 8-20 typical per house
- professional audit and survey data
  - city
  - type of insulation
  - type of HVAC
  
####Curated Dataset
- Austin, TX
- 75 households
- January-November 2013
- 15 minute intervals

####Raw Dataset
- 577 households
- 15 minute and 1 minute

####Shared Dataset
- 200 households
- January-April 2014
- 1 minute intervals

###Tracebase
- 24-hour, 1-second data for 43 unique appliances
- up to 200 traces per appliance
- from TU Darmstadt, Germany

###Weather
- historical and live hourly interval weather data
- source: wunderground

###Oak Park
- 15 minute (possibly 1 minute)
- green button API
- LIVE!!

 _____________________________
 
##Goals

###Disaggregation

- Existence
- Modeling Appliances
- Labeling States
- Extracting Signal
 _____________________________
 
##Algorithms

###Hidden Markov Model (HMM)

-  Develop appliance instance parameters using hidden markov models
    *   z<sub>t</sub>(discrete variable) corresponds to one of K states (state1=on, state2=off)
    *   x<sub>t</sub> (continous variable) is amount of power > 0 (e.x. 100 W)
    *   Hidden Markov Parameters:
        *   Initial Probabilities (&alpha;)
        *   Transition matrix (C) (probability of transition between hidden states)
        *   Emission variables (&phi;) – Gaussian-Gamma, hyperparameters: 
            *   mean, precision, shape, scale
        *   Observed Data (power values, other features)
        *   Hidden States (ON or OFF)
    *  Can be used to generate sample data, predict states, evaluate likelihood
    *  Often used for modeling probabalistic temporal processes
    *  Limited ability to model periodic signals
    *  
![Hidden Markov Model Image](readme_images/bayesianhiddenmarkov.png)


###Factorial Hidden Markov Model (FHMM)
*  combines several hidden markov models in parallel
*   state space comprises all possible combinations of appliance states

###Neural Networks
* Used for semi-supervised and supervised learning
* 

##Accomplishments

##Challenges




































#Wikienergy Deep Dive 1
_____________________________
##Outline
- Goals
  - tool for evaluating energy-saving interventions
  - accurate energy disaggregator (15 minutes)
- Data Sources
  - Pecan Street
  - Tracebase
  - Weather
  - [Oak Park]
- Algorithms
  - FHMM
  - Neural Networks
- Analysis
  - eV Analytics
  - Weather vs. Energy Usage
  - % HVAC
  - Most Common Appliances
 _____________________________

##Data Sources

###Pecan Street

####Overview
- 23 cities
- disaggregated ground truth
- ~70 unique appliances
  - 8-20 typical per house
- professional audit and survey data
  - city
  - type of insulation
  - type of HVAC
  
####Curated Dataset
- Austin, TX
- 75 households
- January-November 2013
- 15 minute intervals

####Raw Dataset
- 577 households
- 15 minute and 1 minute

####Shared Dataset
- 200 households
- January-April 2014
- 1 minute intervals

###Tracebase
- 24-hour, 1-second data for 43 unique appliances
- up to 200 traces per appliance
- from TU Darmstadt, Germany

###Weather
- historical and live hourly interval weather data
- source: wunderground

###Oak Park
- 15 minute (possibly 1 minute)
- green button API
- LIVE!!

 _____________________________
 
##Goals

###Disaggregation

- Existence
- Modeling Appliances
- Labeling States
- Extracting Signal
 _____________________________
 
##Algorithms

###Hidden Markov Model (HMM)

-  Develop appliance instance parameters using hidden markov models
    *   z<sub>t</sub>(discrete variable) corresponds to one of K states (state1=on, state2=off)
    *   x<sub>t</sub> (continous variable) is amount of power > 0 (e.x. 100 W)
    *   Hidden Markov Parameters:
        *   Initial Probabilities (&alpha;)
        *   Transition matrix (C) (probability of transition between hidden states)
        *   Emission variables (&phi;) – Gaussian-Gamma, hyperparameters: 
            *   mean, precision, shape, scale
        *   Observed Data (power values, other features)
        *   Hidden States (ON or OFF)
    *  Can be used to generate sample data, predict states, evaluate likelihood
    *  Often used for modeling probabalistic temporal processes
    *  Limited ability to model periodic signals
    *  
![Hidden Markov Model Image](readme_images/bayesianhiddenmarkov.png)


###Factorial Hidden Markov Model (FHMM)
*  combines several hidden markov models in parallel
*   state space comprises all possible combinations of appliance states

###Neural Networks
* Used for semi-supervised and supervised learning
* 

##Accomplishments

##Challenges





































