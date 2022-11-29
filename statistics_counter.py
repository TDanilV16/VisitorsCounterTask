def count_global():
    with open("stats.txt", "r") as f:
        old_data = f.read()
        counter = int(old_data)
    with open("stats.txt", "w") as f:
        new_data = old_data.replace(str(counter), str(counter + 1))
        f.write(new_data)
    f.close()

    return counter
