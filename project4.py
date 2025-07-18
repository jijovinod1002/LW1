import psutil

memory = psutil.virtual_memory()

print(f"Total RAM: {memory.total / (1024 ** 3):.2f} GB")
print(f"Available RAM: {memory.available / (1024 ** 3):.2f} GB")
print(f"Used RAM: {memory.used / (1024 ** 3):.2f} GB")
print(f"RAM Usage Percentage: {memory.percent}%")