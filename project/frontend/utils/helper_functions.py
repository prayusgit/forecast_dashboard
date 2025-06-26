def format(amount):
    if amount >= 10_000_000:
        return f"{amount / 1_00_00_000:.2f} Cr"
    elif amount >= 1_00_000:
        return f"{amount / 1_00_000:.2f} Lakh"
    elif amount >= 1_000:
        return f"{amount / 1_000:.2f} Thousand"
    else:
        return f"{amount:.2f}"

