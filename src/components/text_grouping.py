def extend_box(box, extend_ratio=0.25):
    """ x, y, height, width"""
    x, y, h, w = box
    mid_x = x + w/2
    mid_y = y + h/2
    ext_h = (1 + extend_ratio) * h
    ext_w = (1 + extend_ratio) * w
    return [mid_x - ext_w / 2, mid_y - ext_h / 2, ext_h, ext_w]


def is_box_overlap(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # If one rectangle is to the left of the other
    if x1 > x2 + w2 or x2 > x1 + w1:
        return False

    # If one rectangle is above the other
    if y1 > y2 + h2 or y2 > y1 + h1:
        return False

    return True


def get_graph(boxes):
    graph = {}
    for box_idx1 in range(len(boxes)-1):
        if box_idx1 not in graph:
            graph[box_idx1] = set()
        for box_idx2 in range(box_idx1+1, len(boxes)):
            if box_idx2 not in graph:
                graph[box_idx2] = set()
            if is_box_overlap(boxes[box_idx1], boxes[box_idx2]):
                graph[box_idx1].add(box_idx2)
                graph[box_idx2].add(box_idx1)
    return graph


def assign_group(new_group_id, box_idx, graph, groups, visited):
    groups[box_idx] = new_group_id
    visited.add(box_idx)
    if box_idx in graph:
        for next_box_idx in graph[box_idx]:
            if next_box_idx not in visited:
                assign_group(new_group_id, next_box_idx, graph, groups, visited)


def get_text_group(texts, confidences, boxes):
    # extend bounding box
    boxes_extended = []
    for box in boxes:
        boxes_extended.append(extend_box(box, 0.5))

    # get bounding box graph
    graph = get_graph(boxes_extended)

    # group bounding box
    groups, visited, n_group = {}, set(), 0
    for box_idx in range(len(boxes)):
        if box_idx in visited:
            continue
        n_group += 1
        assign_group(n_group, box_idx, graph, groups, visited)

    # get grouped text
    grouped_text_dct, grouped_text_count_dct, grouped_confidence_sum_dct = {}, {}, {}
    for box_idx in range(len(boxes)):
        if box_idx not in groups:
            continue

        group = groups[box_idx]
        if group not in grouped_text_dct:
            grouped_text_dct[group] = []
            grouped_text_count_dct[group] = 0
            grouped_confidence_sum_dct[group] = 0.
        grouped_text_dct[group].append(texts[box_idx])
        grouped_text_count_dct[group] += 1
        grouped_confidence_sum_dct[group] += confidences[box_idx]

    # get new list of texts and confidences
    new_texts_ls, new_confidences = [], []
    for group in grouped_text_dct:
        new_texts_ls.append(grouped_text_dct[group])
        if grouped_text_count_dct[group] > 0:
            new_confidences.append(grouped_confidence_sum_dct[group]/grouped_text_count_dct[group])
        else:
            new_confidences.append(0.)

    new_texts = [''.join(texts_ls) for texts_ls in new_texts_ls]

    return new_texts, new_confidences