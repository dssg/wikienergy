Prototyping notebooks for FHMM
==============================
- Cleaned\_iter\_models: This notebook attempts to find a good air conditioning HMM by iterating through the hyperparameters and fitting them to test data rather than directly fitting data to the model directly.  It iterates through a range of means and covariances and finds the one that fits the best for the most traces. There is also a method shows the performance of a single house across several days.

- FHMM\_Class\_test: This notebook uses our fhmm class to create hidden markov models and evaluate them.  It utilizes Pecan Street data for the testing and analysis.

- FHMM\_Evaluate\_Instance\_Models: An older notebook that was used to create models for many individual consumers from Pecan Street and analyzed the parameters of each of those models.

- FHMM\_Tracebase: This notebook creates FHMMs using tracebase data. It uses several different appliances.

- manual\_fhmm: This notebook was an attempt to manually the best FHMM parameters for a given signal. 

- nameless\_appliance\_model: This notebook is a prototype of a technique using pymc to automatically determine the parameters for an HMM given our raw signal.

- Test\_Model: This notebook uses Pecan Street data to create and evaluate HMMs. It is very similar to the FMM\_Class\_Test notebook.
