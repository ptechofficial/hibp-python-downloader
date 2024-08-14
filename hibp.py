import os
import sys
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

BASE_URL = "https://api.pwnedpasswords.com/range/"
MAX_PARALLELISM = 32
OUTPUT_FILE = "hashed_passwords.txt"
TOTAL_HASHES = 1024 * 1024

successful_downloads = 0
failed_downloads = 0
start_time = time.time()

def fetch_and_save_hash_range(hash_range, progress):
    global successful_downloads, failed_downloads
    range_str = get_hash_range(hash_range)
    url = BASE_URL + range_str
    response = requests.get(url)

    if response.status_code == 200:
        with open(OUTPUT_FILE, 'a') as file:
            file.write(response.text)

        successful_downloads += 1
        progress.update(1)
    else:
        failed_downloads += 1

    log_dashboard(range_str, progress.n, progress.total, successful_downloads, failed_downloads)

def get_hash_range(i):
    return f"{i:05X}"[:5]

def log_dashboard(current_hash, current_count, total_count, successes, failures):
    elapsed_time = time.time() - start_time
    speed = current_count / elapsed_time if elapsed_time > 0 else 0
    progress_percentage = (current_count / total_count) * 100
    download_speed = f"{speed:.2f} hashes/sec"
    estimated_total_time = elapsed_time / (progress_percentage / 100) if progress_percentage > 0 else 0

    def format_time(seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))

    sys.stdout.write("\033[H")
    sys.stdout.write("\033[J")
    sys.stdout.flush()

    print(f"Current Hash: {current_hash}")
    print(f"Progress: [{'#' * int(progress_percentage // 2) + '-' * (50 - int(progress_percentage // 2)): <50}] {progress_percentage:.2f}%")
    print(f"Download: {current_count}/{total_count}")
    print(f"Success: {successes} | Failure: {failures}")
    print(f"Speed: {download_speed}")
    print(f"Time Elapsed: {format_time(elapsed_time)}")
    print(f"Estimated Total Time: {format_time(estimated_total_time)}")

if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    print("\n" * 6, end='')

    with tqdm(total=TOTAL_HASHES, ncols=100, leave=False, file=sys.stdout) as progress:
        with ThreadPoolExecutor(max_workers=MAX_PARALLELISM) as executor:
            futures = [executor.submit(fetch_and_save_hash_range, i, progress) for i in range(TOTAL_HASHES)]

            try:
                for future in as_completed(futures):
                    future.result()
            except KeyboardInterrupt:
                print("\nProcess interrupted. Exiting...")
