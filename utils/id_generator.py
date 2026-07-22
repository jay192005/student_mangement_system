def generate_id(prefix, existing_ids):
    max_num = 0
    for eid in existing_ids:
        if eid.startswith(prefix):
            try:
                num = int(eid[len(prefix):])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    return f"{prefix}{max_num + 1}"