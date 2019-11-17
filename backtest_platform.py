import numpy as np
import pandas as pd


class Platform:
    def __init__(self, data):
        self.data = data

    def processor(self):
        pass

    def group(self, N, means):
        pass

    def get_performance(self, factor):
        pass


