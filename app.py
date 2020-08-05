import pathlib
import sys

from faucet_collector.crypto_claimer import CryptoClaimer

try:
    file_path = pathlib.Path(sys.argv[1])

    if file_path.suffix != ".txt":
        raise SystemExit(
            f"Unsupported file type: {file_path.suffix}\nSupported file type: .txt"
        )

    crypto_claimer = CryptoClaimer()
    crypto_claimer.collect_crypto_faucets(file_path)
    crypto_claimer.start_collecting_crypto()
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <file_to_read>")
