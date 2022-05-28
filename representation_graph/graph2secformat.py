import json
import pandas as pd
import sys

outputFile = ''

originalData = sys.argv[1]
originalDataFrame = pd.read_csv(originalData, sep='\t')
