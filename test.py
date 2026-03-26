import random
import time
import os
from datetime import datetime
import threading

# =========================
# Generare vector
# =========================
def genereaza_vector(n, filename):
    v = [random.randint(0, 10000) for _ in range(n)]
    with open(filename, "w") as f:
        f.write(" ".join(map(str, v)))

def citeste_vector(filename):
    with open(filename, "r") as f:
        return list(map(int, f.read().split()))

# =========================
# Sortari
# =========================
def merge_sort(v):
    if len(v) <= 1:
        return v
    mid = len(v) // 2
    left_half = merge_sort(v[:mid])
    right_half = merge_sort(v[mid:])
    return merge(left_half, right_half)

def merge(left, right):
    sorted_list = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list 

def sortare_py(v):
    arr = v.copy()
    arr.sort()
    return arr

def bubble_sort(v):
    arr = v.copy()
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def selection_sort(v):
    arr = v.copy()
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(v):
    arr = v.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def quick_sort(v):
    if len(v) <= 1:
        return v
    pivot = v[len(v)//2]
    left = [x for x in v if x < pivot]
    mid = [x for x in v if x == pivot]
    right = [x for x in v if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# =========================
# Masurare timp + stats
# =========================
def masoara(sort_function, v, timeout_sec):
    result = [None]  # listă mutabilă pentru a stoca rezultatul
    finished = threading.Event()

    def worker():
        start = time.perf_counter()
        sort_function(v)
        end = time.perf_counter()
        result[0] = (end - start, len(v) / (end - start) if (end - start) > 0 else 0)
        finished.set()

    t = threading.Thread(target=worker)
    t.start()
    t.join(timeout=timeout_sec)

    if not finished.is_set():
        return None, None  # timeout
    return result[0]

# =========================
# Salvare rezultate
# =========================
def salveaza_rezultate(folder, nume_sort, n, timp, eps):
    os.makedirs(folder, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fisier = os.path.join(folder, f"{nume_sort}.txt")
    with open(fisier, "a") as f:
        f.write(f"Data: {now}\n")
        f.write(f"Elemente: {n}\n")
        f.write(f"Timp: {timp:.6f} sec\n" if timp is not None else "Timp: timeout\n")
        f.write(f"Elemente/secunda: {eps:.2f}\n" if eps is not None else "Elemente/secunda: -\n")
        f.write("-" * 30 + "\n")

# =========================
# Calcul medie
# =========================
def calculeaza_media_din_fisier(fisier):
    valori = []
    if not os.path.exists(fisier):
        return 0
    with open(fisier, "r") as f:
        for linie in f:
            if "Elemente/secunda" in linie:
                try:
                    valoare = float(linie.split(":")[1])
                    valori.append(valoare)
                except:
                    pass
    if len(valori) == 0:
        return 0
    return sum(valori) / len(valori)

# =========================
# MAIN
# =========================
def main():
    n = int(input("Cate elemente: "))
    timeout_minute = int(input("Timeout (minute): "))
    timeout_secunde = timeout_minute * 60

    folder_baza = "rezultate_sortari"
    vector_file = "vector.txt"

    genereaza_vector(n, vector_file)
    print("S-a generat\n")
    v = citeste_vector(vector_file)

    sortari = {
        "python": sortare_py,
        "merge": merge_sort,
        "quick": quick_sort,
        "insertion": insertion_sort,
        "selection": selection_sort,
        "bubble": bubble_sort
    }

    print("\n--- Rezultate ---")
    for nume, functie in sortari.items():
        timp, eps = masoara(functie, v, timeout_secunde)
        if timp is None:
            print(f"{nume}: Timeout!")
        else:
            print(f"{nume}: {timp:.6f} sec | {eps:.2f} elem/sec")
        salveaza_rezultate(folder_baza, nume, n, timp, eps)

    print("\n--- Medii pentru toate testele ---")
    for nume in sortari.keys():
        fisier = os.path.join(folder_baza, f"{nume}.txt")
        media = calculeaza_media_din_fisier(fisier)
        if media == 0:
            print(f"{nume}: nu are date")
        else:
            print(f"{nume}: {media:.2f} elem/sec (medie)")

if __name__ == "__main__":
    main()