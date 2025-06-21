from collections import defaultdict, Counter

def get_class_stats(results):
    stats = defaultdict(lambda: {
        'total': 0,
        'success_count': 0,
        'top_adversarial': []
    })
    
    # First pass: collect counts
    adv_counts = defaultdict(Counter)
    for res in results:
        orig = res['original_class']
        adv = res['adv_class']
        stats[orig]['total'] += 1
        if orig != adv:
            stats[orig]['success_count'] += 1
            adv_counts[orig][adv] += 1
    
    # Second pass: get top 3 for each class
    for orig in adv_counts:
        stats[orig]['top_adversarial'] = adv_counts[orig].most_common(3)
    
    return dict(stats)