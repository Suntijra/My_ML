#%%
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import  euclidean_distances
#%%
# df = pd.read_excel(r'data\fruit_data.xlsx')
# with pd.option_context('display.max_rows', 8): display(df)

# x = df[['width', 'height', 'mass', 'color_score']]
# y = df['fruit_name']
#%%
x = pd.DataFrame({
    'กบ':     [0,1,0,0,0,0,1,1,0],
    'ปลาหมอ': [0,1,0,0,1,0,1,0,1],
    'จระเข้':    [0,1,0,0,1,0,1,0,0],
    'ปลาหมอ':[0,0,0,0,1,0,1,0,1],
    'เต่า':[0,1,0,0,0,0,1,0,0],
    'dog':[1,0,1,1,0,1,0,0,0],
    'bird':[1,0,0,1,0,1,0,0,0],
        
})
x = x.T
y =[0,1,2,1,2,2,3]
y = pd.DataFrame(y,columns=['animal'])
x = pd.concat([x,y])

#%%
# x_train, x_test, y_train, y_test = train_test_split(x, y)

# # #scaling after splitting
# # scaler = StandardScaler()
# # x_train = scaler.fit_transform(x_train)
# # x_test = scaler.transform(x_test)

k = 5
# model = KNeighborsClassifier(n_neighbors=k)
# model.fit(x.T, y)

x_pred = [[0,0,1,0,0,0,0,0,0]]
# x_pred_sc = scaler.transform(x_pred)
y_pred = model.predict(x_pred)

a = x_pred[0][0]
b = x_pred[0][1]
c = x_pred[0][2]
d = x_pred[0][3]
e = x_pred[0][4]
f = x_pred[0][5]
g = x_pred[0][6]
g2 = x_pred[0][7]
g3 = x_pred[0][8]
g4 = x_pred[0][9]
y = y[0][10]
print(y)
# print('K =', k)
# print('Prediction:')
# # print(f'width: {w}, height: {h}, mass: {m}, ', end='')
# # print(f'color score {c} => fruit: {f}')
# # print()
# print('Accuracy:', '{:.2f}'.format(model.score(x_test, y_test)))
# %%
