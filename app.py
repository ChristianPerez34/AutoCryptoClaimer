import pathlib
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler

from faucet_collector.crypto_claimer import CryptoClaimer


def claim_crypto_job():
    crypto_claimer = CryptoClaimer()
    crypto_claimer.collect_crypto_faucets(file_path)
    crypto_claimer.start_collecting_crypto()


scheduler = BackgroundScheduler()
scheduler.add_job(claim_crypto_job, "interval", hours=1)

try:
    file_path = pathlib.Path(sys.argv[1])

    if file_path.suffix != ".txt":
        raise SystemExit(
            f"Unsupported file type: {file_path.suffix}\nSupported file type: .txt"
        )
    scheduler.start()

    while True:
        time.sleep(2)


except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <file_to_read>")
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
