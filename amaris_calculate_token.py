# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:41:01 2025

@author: JPHarsonMe
"""

import pandas as pd
import tiktoken

working_dir = "C:\\Users\\JPHARSONME\\Downloads\\private-generativeai\\"

df = pd.read_excel(working_dir + "amaris_main_data.xlsx")
# Combine QUESTION and ANSWER columns into a single text column
df['CONTEXT'] = df['Question'] + " " + df['Answer']
