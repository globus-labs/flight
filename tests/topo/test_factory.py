def test_create_two_tier_topo():
    from flight.topo.factory import create_standard_topo

    for n in [1, 10, 100]:
        topo = create_standard_topo(n)
        assert topo.number_of_workers == n
        assert topo.leader is not None
