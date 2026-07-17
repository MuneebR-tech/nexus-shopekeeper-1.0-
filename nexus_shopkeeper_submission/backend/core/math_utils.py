"""
Nexus Shopkeeper - Core Mathematics & Clustering Engine
Vectorized matrix math, distance calculations, and clustering hook for KMeans engine.
"""

import sys
import numpy as np
from pathlib import Path
from typing import Tuple

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.core.kmeans_engine import KMeansEngine


def calculate_distance_matrix(data: np.ndarray) -> np.ndarray:
    """
    Computes a vectorized 16-dimensional distance matrix between all customer feature vectors.
    Uses NumPy broadcasting for speed.
    
    :param data: A NumPy array of shape (N, 16) containing customer feature vectors.
    :return: A matrix of shape (N, N) containing Euclidean distances.
    """
    # Vectorized pairwise Euclidean distance
    # d(u, v) = sqrt(||u||^2 + ||v||^2 - 2 u . v)
    dot_product = np.dot(data, data.T)
    square_norms = np.diag(dot_product)
    
    # Broadcasting to get pairwise squared differences
    dists_sq = square_norms[:, np.newaxis] + square_norms[np.newaxis, :] - 2 * dot_product
    # Avoid numerical precision negative values
    dists_sq = np.clip(dists_sq, 0.0, None)
    
    return np.sqrt(dists_sq)


def calculate_silhouette_score(data: np.ndarray, labels: np.ndarray) -> float:
    """
    Computes the silhouette score to optimize the selection of clusters (K).
    
    :param data: Customer feature vectors.
    :param labels: Assigned cluster labels.
    :return: Silhouette coefficient float between -1 and 1.
    """
    engine = KMeansEngine(n_clusters=len(np.unique(labels)))
    return engine.calculate_silhouette_score(data, labels)


def run_k_means_clustering(data: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Executes K-means clustering on customer purchase histories.
    Maps customer profiles to 6 core retail personas.
    
    :param data: NumPy array of shape (N, 16).
    :param k: Number of target clusters (typically 6).
    :return: A tuple of (centroids, labels).
    """
    engine = KMeansEngine(n_clusters=k, max_iterations=300, tolerance=1e-6, random_state=42)
    labels = engine.fit_predict(data)
    return engine.centroids, labels
