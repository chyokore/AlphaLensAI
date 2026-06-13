from signal_engine import (
    get_best_opportunity
)

print(
    "\n===== SIGNAL TEST =====\n"
)

for i in range(5):

    signal = (
        get_best_opportunity()
    )

    print(
        f"Signal {i+1}:"
    )

    print(signal)

    print()