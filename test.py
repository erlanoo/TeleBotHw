
def make_readable(seconds):
    h = seconds // 3600
    m = (seconds - h * 3600) // 60
    s = seconds - (h * 3600) - (m * 60)
    return f"{h:0>2d}:{m:0>2d}:{s:0>2d}"

print(make_readable(5))
print(make_readable(25))
print(make_readable(999))
print(make_readable(359999))