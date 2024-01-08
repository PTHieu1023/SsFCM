import numpy as np

#from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score
#from sklearn.metrics.pairwise import euclidean_distances
def init_membership_matrix(number_sample: int, number_cluster: int):
    membership_matrix = np.random.rand(number_sample, number_cluster)
    membership_matrix /= np.sum(membership_matrix, axis=1)[:, np.newaxis]
    return membership_matrix

def init_centroids(dataset, n_cluster, m, u = None):
    if u is None:
        return np.random.rand(n_cluster, dataset.shape[1])
    u = u**m
    centroids = np.zeros((n_cluster, dataset.shape[1]))
    for i in range(n_cluster):
        d = np.sum(u[:, i])
        if d == 0:
            centroids[i] = np.random.rand(dataset.shape[1])
        else:
            for j in range(dataset.shape[0]):
                centroids[i] += u[j][i] * dataset[j]
            centroids[i] /= d
    return centroids
    
def diff_membership_matrix(u: np.ndarray, u_bar: np.ndarray)->np.ndarray:
	return abs(u-u_bar)


def update_centroids(dataset, u_matrix, u_bar_matrix, centroids, number_cluster, m):
    
    diff_u = diff_membership_matrix(u_matrix, u_bar_matrix)
    for i in range(number_cluster):
        centroids[i, :] = (np.sum((diff_u[:, i] ** m)[:, np.newaxis] * dataset, axis=0) /
                           np.sum(diff_u[:, i] ** m))
    return centroids

def euclid_distance_square(point1, point2):
    """
    :param point1: coordinate of first point
    :param point2: coordinate of second point
    :return: distance square between 2 points
    """
    d = len(point1)
    return sum([(point1[i] - point2[i])**2 for i in range (d)])

def update_membership_matrix(dataset, centroids, u_supervised, m):
    u_matrix = np.zeros((u_supervised.shape[0], u_supervised.shape[1]))
    for i in range(u_supervised.shape[1]):
        u_matrix[:, i] = np.linalg.norm(dataset - centroids[i, :], axis=1)
    u_matrix = 1 / (u_matrix ** (2 / (m - 1)) * np.sum((1 / u_matrix) ** (2 / (m - 1)), axis=1)[:, np.newaxis])
    sum_supervised = [np.sum(r) for r in u_supervised]
    for i in range(u_matrix.shape[0]):
        u_matrix[i, :] *= (1-sum_supervised[i])
    u_matrix += u_supervised
    # print(u_matrix)
    return u_matrix

def ssfcm(dataset, number_cluster, m, max_iter, epsilon, supervised_matrix:np.ndarray = None):
    """
    :param dataset: Data after preprocessing (No category, no string and scaled)
    :param number_cluster: Number of clusters
    :param m: fuzziness index
    :param max_iter: the maximum times of loops to prevent infinite time execute
    :param epsilon: the maximum error of objective function - J(U,V)
    :param supervised_matrix: matrix of data points that supervised the result
    :return u: membership matrix after converged,
    :return v: centroids matrix,
    :return d: number loops executed
    """
    number_sample = dataset.shape[0]
    if supervised_matrix is None:
        supervised_matrix = np.zeros((number_sample, number_cluster))
    # number_figures = dataset.shape[1]
    centroids = init_centroids(dataset=dataset, n_cluster=number_cluster, m= m, u=supervised_matrix)
    u = init_membership_matrix(number_sample, number_cluster)
    for i in range(max_iter):
        pre_u = u
        u = update_membership_matrix(dataset, centroids, supervised_matrix, m)
        centroids = update_centroids(dataset, u, supervised_matrix, centroids, number_cluster, m)
        # u = update_membership_matrix(dataset, centroids, supervised_matrix, m)
        eps = np.linalg.norm(pre_u - u)
        if eps < epsilon:
            return u, centroids, i
    return u, centroids, max_iter

