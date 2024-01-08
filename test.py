import numpy as np
import pandas
from APIs.machine_learning.data_clustering.semi_supervised_fuzzy_c_means import *
from APIs.data_processor import *

# filepath = "D:\projects\code\zHJuniikPy\CODE PYTHON\GraduateResearch1\dataset\iris.csv"
# df = export_data(filepath)
# df_col = df.columns
data_processor = DataProcess()
df = [[-2, 1.5],[-2, 1], [-2.3, 2], [-2.5, 1.2], [-3.5, -1.5], [-3, -1.5], [-4.5, -1.5], [-4, -1], [0.5, 1.5], [1, 1.5], [1.5, 1], [-0.2, 1.8]]
supervised = [[0.5, 0, 0], [0.5, 0 , 0], [0.5, 0 ,0], [0, 0 ,0], [0, 0.5, 0], [0, 0.5,0], [0,0,0], [0, 0.5, 0], [0, 0, 0.5], [0, 0, 0.5], [0,0,0],[0,0,0]]
supervised = np.array(supervised)
df = pandas.DataFrame(df)
data = data_processor.preprocess_data(df)
u, v, d = ssfcm(data, 3, 2, 10000, 0.0001, np.zeros((data.shape[0], 3)))
print(u)
print(data_processor.reverse_scale_data(v))