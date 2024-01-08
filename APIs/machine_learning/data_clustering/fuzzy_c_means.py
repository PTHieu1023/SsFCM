import numpy as np

def init_membership_matrix(number_sample:int, number_cluster:int):
    membership_matrix = np.random.rand(number_sample, number_cluster)
    membership_matrix /= np.sum(membership_matrix, axis=1)[:, np.newaxis]
    return membership_matrix

def update_centroids(dataset, u_matrix, centroids, number_cluster, m):
    for i in range(number_cluster):
        centroids[i, :] = (np.sum((u_matrix[:, i] ** m)[:, np.newaxis] * dataset, axis=0) /
            np.sum(u_matrix[:, i] ** m))
    return centroids

def update_membership_matrix(dataset, centroids, number_cluster, m):
    u_matrix = np.zeros((dataset.shape[0], number_cluster))
    for i in range(number_cluster):
        u_matrix[:, i] = np.linalg.norm(dataset - centroids[i, :], axis=1)

    u_matrix = 1 / (u_matrix ** (2 / (m - 1)) * np.sum((1 / u_matrix) ** (2 / (m - 1)), axis=1)[:, np.newaxis])
    return u_matrix

def fcm(dataset, number_cluster, m, max_iter, epsilon):
    """
    :param dataset: Data after preprocessing (No category, no string and scaled)
    :param number_cluster: Number of cluters
    :param m: fuzziness index
    :param max_iter: the maximum times of loops to prevent infinite time execute
    :param epsilon: the maximum error of objective function - J(U,V)
    :return u: membership matrix after converged,
    :return v: centroids matrix,
    :return d: number loops executed
    """
    number_sample = dataset.shape[0]
    number_figures = dataset.shape[1]
    centroids = np.zeros((number_cluster, number_figures))
    u = init_membership_matrix(number_sample, number_cluster)
    for i in range(max_iter):
        pre_u = u
        centroids = update_centroids(dataset, u, centroids, number_cluster, m)
        u = update_membership_matrix(dataset, centroids, number_cluster, m)
        eps = np.linalg.norm(pre_u - u)
        if eps < epsilon:
            return u, centroids, i
    return u, centroids, max_iter
