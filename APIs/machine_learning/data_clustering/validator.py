import numpy as np
def db_adjusted(data: np.ndarray, membership: np.ndarray, centroids: np.ndarray):
	n = data.shape[0]
	intra_cluster_variance = 0
	inter_cluster_variance = 0

	for i in range(n):
		cluster_idx = np.argmax(membership[i])
		intra_cluster_variance += np.sum((data[i] - centroids[cluster_idx])**2)
		for j in range(n):
			if membership[j][cluster_idx] > 0:
				inter_cluster_variance += np.sum((data[i] - data[j])**2)
	
	return (intra_cluster_variance / inter_cluster_variance) * (n / sum(membership.sum(axis=1)))

def calculate_sse(data, v, u, m):
	sse = 0
	for i in range(data.shape[0]):
		for j in range(v.shape[0]):
			sse += u[i, j] * m * np.linalg.norm(data[i, :] -  v[j, :]) * 2
	return sse


def dunn_index(X: np.ndarray, W: np.ndarray, mu:np.ndarray):
	n = X.shape[0]
	c = mu.shape[0]

	within_cluster_distances = []
	for i in range(c):
		cluster_i = X[W[:, i] == 1]
		within_cluster_distances.append(np.mean([np.linalg.norm(x - y) for x, y in itertools.combinations(cluster_i, 2)]))
	
	between_cluster_distances = []
	for i in range(c):
		for j in range(i + 1, c):
			cluster_i = X[W[:, i] == 1]
			cluster_j = X[W[:, j] == 1]
			between_cluster_distances.append(np.linalg.norm(mu[i] - mu[j]))
	return np.max(between_cluster_distances) / np.sum(within_cluster_distances)


def get_validator_criteria(data: np.ndarray, membership: np.ndarray, centroids: np.ndarray, m, DB:bool = True, SSE:bool = True, Dunn: bool = True):
	validators = {}
	if SSE:
		validators['SSE'] = calculate_sse(data, centroids, membership, m)
	if DB:
		validators['DB'] = db_adjusted(data, membership, centroids)
	# if Dunn:
	# 	validators['Dunn'] = dunn_index(data, membership, centroids)
	return validators