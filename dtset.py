#%%
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

x = np.array( [[1],[1],[2],[2],[3],[5]])

y = np.array([[1.5],[4.5],[1.5],[3.5],[2.5],[6]])

data = [[1, 1.5], [1, 4.5], [2, 1.5], [2, 3.5], [3, 2.5], 
        [5, 6]]

model = KMeans(n_clusters=2, n_init=2, random_state=0)
model.fit(data)

print(model.labels_)
print('cluster_centroid_')
print(model.cluster_centers_)
print()

pd = model.predict([[1.2, 1.7]])     #ทำนายผลของตำแหน่ง (7, 7)
print('%.2f'%(pd[0]))
LABEL_COLOR_MAP = {0 : 'r',
                   1 : 'g',
                   }

label_color = [LABEL_COLOR_MAP[l] for l in model.labels_]
plt.scatter(x,y, c=label_color)
plt.ylim(-3,7)
plt.xlim(-3,7)
# %%