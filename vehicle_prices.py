import numpy as np


def predict(X, w):
    return np.matmul(X, w)


def loss(X, Y, w):
    return np.average((predict(X, w) - Y) ** 2)


def gradient(X, Y, w):
    return 2 * np.matmul(X.T, (predict(X, w) -Y)) / X.shape[0]


def train(X, Y, iterations, lr):
    w = np.zeros((X.shape[1], 1))
    for i in range(iterations):
        if i % 1000 == 0:
            print("Iteration %4d => Loss: %.15f" % (i, loss(X, Y, w)))
        w -= gradient(X, Y, w) * lr
    return w


dataset = np.loadtxt("car_details_v3.csv", delimiter=",", skiprows=1)  #, unpack=True)
y = dataset[:, -1]
dataset = dataset[:, :-1]

X = np.column_stack((np.ones(dataset[:, 0].size), dataset))
Y = y.reshape(-1, 1)
w = train(X, Y, iterations=1000000, lr=0.0000000001)

print("\nWeights: %s" % w.T)
print("\nA few predictions:")
for i in range(5):
    print("X[%d] -> %.4f (label: %d)" % (i, predict(X[i], w), Y[i]))
