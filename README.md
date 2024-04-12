# Impact-of-voice-on-disclosure
Impact of voice on disclosure during phone interviews

# Rasa Installation and Usage Guide

This guide provides instructions on how to install Rasa, an open-source conversational AI framework, and how to use it to train and test our models.

## Installation

### Step 1: Prerequisites

Before installing Rasa, ensure you have the following prerequisites installed on your system.

An environment ready with:
- Python: recommended version: 3.7 or higher (Python 3.10 might be trickier to get setup properly)
- pip (Python package installer)

### Step 2: Install Rasa

You can install Rasa by running the following command in your terminal or command prompt: 'pip install rasa'

## Usage

Once Rasa is installed, you can start using it to build and test conversational AI models. Below are instructions on how to perform common tasks using Rasa.

### Train Rasa models

To train a Rasa model using your NLU (Natural Language Understanding) and dialogue training data, run the following command in your terminal: 'rasa train'


This command will train both the NLU and dialogue management models based on the data provided in your project directory.

### Launch Rasa shell

After training your model, you can interact with it using the Rasa shell. To launch the Rasa shell, run the following command: 'rasa shell'


This will start the interactive shell where you can chat with your trained conversational model.

## Additional Resources

- [Rasa Documentation](https://rasa.com/docs/rasa/)
- [Rasa Community Forum](https://forum.rasa.com/)
- [Rasa GitHub Repository](https://github.com/RasaHQ/rasa)

## You have to train each model beforehand to be able to launch the whole project!

## Launch project

To use it, start rasaInputOutput.py in Impact-of-voice-on-disclosure/code/data/
