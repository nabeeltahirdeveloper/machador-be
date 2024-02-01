from typing import Dict, Union
def remove_empty_values(data):
    return {k: v for k, v in data.items() if v != ''}
def generate_filter_object(filter_str: str) -> Dict[str, Union[str, float, bool]]:
    if not len(filter_str) > 1:
        return {}
    filter_obj = {}
    for i in range(0, len(filter_str), 2):
        if i + 1 >= len(filter_str): break
        raw_value = filter_str[i + 1]
        try:
            # numeric values
            if "." in raw_value:
                a_value = float(raw_value)
            else:
                a_value = int(raw_value)
        except Exception as e:
            if raw_value == 'true' or raw_value == 'false':
                a_value = True if raw_value == 'true' else False
            else:
                a_value = raw_value
        filter_obj[filter_str[i]] = a_value

    return remove_empty_values(filter_obj)
