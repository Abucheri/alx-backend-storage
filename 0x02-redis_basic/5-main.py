#!/usr/bin/env python3
""" Main file """

import time
get_page = __import__('web').get_page

url = "http://slowwly.robertomurray.co.uk"

# Measure the time before calling get_page
start_time = time.time()

html_content = get_page(url)

# Measure the time after calling get_page
end_time = time.time()

# Calculate the time taken
time_taken = end_time - start_time

# Print the time taken
print(f"Time taken to fetch {url}: {time_taken:.2f} seconds")

# Print the HTML content
# print(html_content)
