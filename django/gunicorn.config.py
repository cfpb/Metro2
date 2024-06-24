import multiprocessing

bind = ":8000"
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 150
max_requests_jitter = 50
log_file = "-"
timeout = 300
log_level = "info"