def normalize_ctrl_vals(ctrl_vals):
    normalized = [0, 0, 0, 0, 0, 0]

    vector_total = abs(ctrl_vals[0]) + abs(ctrl_vals[3]) + abs(ctrl_vals[4])        # yaw, x, y
    non_vector_total = abs(ctrl_vals[1]) + abs(ctrl_vals[2]) + abs(ctrl_vals[5])    # roll, pitch, z

    normalized[0] = ctrl_vals[0]
    normalized[1] = ctrl_vals[1]
    normalized[2] = ctrl_vals[2]
    normalized[3] = ctrl_vals[3]
    normalized[4] = ctrl_vals[4]
    normalized[5] = ctrl_vals[5]

    if vector_total > 1:
        normalized[0] = ctrl_vals[0] / vector_total
        normalized[3] = ctrl_vals[3] / vector_total
        normalized[4] = ctrl_vals[4] / vector_total

    if non_vector_total > 1:
        normalized[1] = ctrl_vals[1] / non_vector_total
        normalized[2] = ctrl_vals[2] / non_vector_total
        normalized[5] = ctrl_vals[5] / non_vector_total

    if vector_total == 0:
        normalized[0] = 0
        normalized[3] = 0
        normalized[4] = 0

    if non_vector_total == 0:
        normalized[1] = 0
        normalized[2] = 0
        normalized[5] = 0

    return normalized
