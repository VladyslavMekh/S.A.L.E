import functools

def count_lines_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        total_lines_read = 0
        successful_mapped = 0
        for item in generator:
            total_lines_read += 1
            if item is not None:
                successful_mapped += 1
                yield item

        print("="*100)
        print("Total lines read: ", total_lines_read)
        print("Successful mapped: ", successful_mapped)
        print("="*100)
    return wrapper