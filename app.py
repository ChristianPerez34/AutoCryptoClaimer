import argparse
import pathlib
import time

from apscheduler.schedulers.background import BackgroundScheduler

from faucet_collector.crypto_claimer import CryptoClaimer


def claim_crypto_job():
    crypto_claimer = CryptoClaimer()
    crypto_claimer.start_driver()
    crypto_claimer.collect_crypto_faucets(crypto_faucets_file)
    crypto_claimer.start_collecting_crypto()


scheduler = BackgroundScheduler()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto crypto claimer")
    parser.add_argument("path", type=str, help="File path to text file")
    parser.add_argument(
        "-d",
        "--driver",
        action="store",
        default="chrome",
        help="Browser name of web driver to use i.e (Chrome, Firefox, and so forth)",
    )
    args = parser.parse_args()

    crypto_faucets_file = pathlib.Path(args.path)

    if crypto_faucets_file.suffix != ".txt":
        raise SystemExit(
            f"Unsupported file type: {crypto_faucets_file.suffix}\nSupported file type: .txt"
        )
    scheduler.add_job(claim_crypto_job, "interval", hours=1)
    scheduler.start()
    claim_crypto_job()

    while True:
        time.sleep(1)
