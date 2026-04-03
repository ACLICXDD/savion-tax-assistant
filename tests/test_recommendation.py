from savion.recommendation import generate_recommendations


def test_generate_recommendations():
    recs = generate_recommendations(50000, 10000)
    assert len(recs) > 0
    for r in recs:
        assert "rationale" in r
        assert isinstance(float(r["suggested_amount"]), float)
