from flight_optimizer.distance import km_between


def test_zero_for_same_point():
    assert km_between((0.0, 0.0), (0.0, 0.0)) == 0


def test_lhr_to_jfk_about_5540_km():
    lhr = (51.4700, -0.4543)
    jfk = (40.6413, -73.7781)
    assert 5500 < km_between(lhr, jfk) < 5600


def test_symmetric():
    a = (52.0, 13.0)
    b = (40.4, -3.7)
    assert abs(km_between(a, b) - km_between(b, a)) < 1e-6
