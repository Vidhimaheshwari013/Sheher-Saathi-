from collections import defaultdict


MIN_CLUSTER_SIZE = 3


def cluster_complaints(
    complaint_ids: list,
    categories: list,
    min_cluster_size: int = MIN_CLUSTER_SIZE
):
    """
    Create civic clusters based on the AI-generated complaint category.

    A category becomes a cluster only when there are at least
    `min_cluster_size` complaints belonging to that category.

    Different categories are NEVER merged together.

    Returns:
        dict mapping complaint_id -> cluster_label

        -1 means the complaint does not belong to a large enough cluster.
    """

    if not complaint_ids or not categories:
        return {cid: -1 for cid in complaint_ids}

    # Group complaint IDs by their AI-generated category
    category_groups = defaultdict(list)

    for complaint_id, category in zip(complaint_ids, categories):
        if not category:
            continue

        normalized_category = category.strip().lower()
        category_groups[normalized_category].append(complaint_id)

    labels = {}
    cluster_id = 0

    # Create a cluster only when 3+ complaints share the same issue
    for category, ids in category_groups.items():

        if len(ids) >= min_cluster_size:
            for complaint_id in ids:
                labels[complaint_id] = cluster_id

            cluster_id += 1
        else:
            for complaint_id in ids:
                labels[complaint_id] = -1

    # Handle complaints without a category
    for complaint_id in complaint_ids:
        if complaint_id not in labels:
            labels[complaint_id] = -1

    return labels