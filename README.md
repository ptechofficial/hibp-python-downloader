# HIBP Downloader

This Python script downloads hash ranges from the Have I Been Pwned (HIBP) API and stores them in a single file. It also provides a real-time dashboard in the terminal, showing the progress of the download, current hash being downloaded, number of successful and failed downloads, and the download speed.

## Features

- **Parallel Downloading**: The script uses multithreading to download hash ranges in parallel, making the process faster.
- **Real-time Dashboard**: The terminal displays a dashboard that updates in real-time, showing progress, current hash, download statistics, and speed.
- **Customizable Parameters**: Easily modify the number of parallel threads and the output file location.

## Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - `requests`
  - `tqdm`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/hibp-downloader.git
   cd hibp-downloader
