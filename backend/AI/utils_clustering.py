from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from scipy.spatial.distance import cdist
import numpy as np

def perform_kmeans_clustering(X, n_clusters=4):
    kmeans = KMeans(n_clusters=n_clusters, init='random', max_iter=100)
    kmeans.fit(X)
    return kmeans

def calculate_metrics(X, kmeans):
    # Calculate inertia
    inertia = kmeans.inertia_

    # Calculate silhouette score
    silhouette_avg = silhouette_score(X, kmeans.labels_)

    # Calculate Davies-Bouldin index
    davies_bouldin = davies_bouldin_score(X, kmeans.labels_)

    # Calculate Calinski-Harabasz index
    calinski_harabasz = calinski_harabasz_score(X, kmeans.labels_)

    # Calculate intra-cluster distance
    intra_distances = kmeans.transform(X).min(axis=1)
    intra_cluster_distance = intra_distances.mean()

    # Calculate inter-cluster separation
    cluster_centers = kmeans.cluster_centers_
    inter_cluster_distances = cdist(cluster_centers, cluster_centers)
    inter_cluster_separation = inter_cluster_distances[np.triu_indices(len(cluster_centers), k=1)].mean()

    # Return all metrics
    return {
        'inertia': inertia,
        'silhouette_score': silhouette_avg,
        'davies_bouldin_index': davies_bouldin,
        'calinski_harabasz_index': calinski_harabasz,
        'intra_cluster_distance': intra_cluster_distance,
        'inter_cluster_separation': inter_cluster_separation,
    }
