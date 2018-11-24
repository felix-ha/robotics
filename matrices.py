import numpy as np

def translation(x, y):
    return np.matrix(np.array([[1,0,x],
                               [0,1,y],
                               [0,0,1]]))

def rotation(theta):
    return np.matrix(np.array([[np.cos(theta), -np.sin(theta), 0],
                               [np.sin(theta), np.cos(theta), 0],
                               [0, 0, 1]]))

def flip_y():
    return np.matrix(np.array([[1, 0, 0],
                               [0, -1, 0],
                               [0, 0, 1]]))



if __name__ == '__main__':
    x = np.array([1,0,1])

    t = translation(10, 10)
    r = rotation(np.pi * 1/2)
    print(np.matmul(t*r, x))





