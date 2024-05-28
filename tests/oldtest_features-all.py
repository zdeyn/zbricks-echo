import pytest
from pytest_bdd import scenarios
import os

# Import common steps
from .steps.routes import *

# Discover and run all feature files in the 'features' directory
features_dir = os.path.join(os.path.dirname(__file__), 'features')
for feature_file in os.listdir(features_dir):
    if feature_file.endswith('.feature'):
        scenarios(os.path.join(features_dir, feature_file))
