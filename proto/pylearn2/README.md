Pylearn2
========

This directory contains the following:

- Neural network architectures (good and bad)
  - Best: conv\_nn\_2\_layer\_32\_stride\_2.yaml
- Scripts for the following tasks:
  - creating datasets
  - removing NaNs from datasets
  - evaluating models
  - training models
  - concatenating datasets

Example usage:

    python run_model.py network.yaml path/to/data/dir data_prefix model_prefix
