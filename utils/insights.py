def generate_insights(base, target, rate_change, country=None, avg_infl=None):
    """Return a short insight paragraph based on data."""
    sentences = []

    # Exchange rate movement
    if rate_change > 0:
        sentences.append(f"**{base}** strengthened by **{rate_change:.2f}%** against **{target}** in the last six months.")
    elif rate_change < 0:
        sentences.append(f"**{base}** weakened by **{abs(rate_change):.2f}%** against **{target}** in the last six months.")
    else:
        sentences.append(f"The exchange rate between **{base}** and **{target}** remained stable.")

    # Inflation context
    if avg_infl is not None and country:
        if avg_infl > 6:
            sentences.append(f"High inflation in **{country}** ({avg_infl:.1f}%) may have pressured its currency.")
        elif avg_infl < 2:
            sentences.append(f"Low inflation in **{country}** ({avg_infl:.1f}%) indicates stable purchasing power.")
        else:
            sentences.append(f"Inflation in **{country}** averaged **{avg_infl:.1f}%**, a moderate level overall.")

    return " ".join(sentences)
