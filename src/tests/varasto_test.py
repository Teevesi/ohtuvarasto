import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)


class TestVarastoExtra(unittest.TestCase):
    def test_init_with_negative_alku_saldo_is_zeroed(self):
        v = Varasto(10, -5)
        self.assertEqual(v.tilavuus, 10)
        self.assertEqual(v.saldo, 0.0)

    def test_init_with_negative_tilavuus_and_negative_alku_saldo(self):
        v = Varasto(-5, -3)
        self.assertEqual(v.tilavuus, 0.0)
        self.assertEqual(v.saldo, 0.0)

    def test_init_with_negative_tilavuus_and_positive_alku_saldo_sets_saldo_to_param(self):
        # This exercises the branch where alku_saldo > tilavuus (uses parameter tilavuus)
        v = Varasto(-1, 5)
        self.assertEqual(v.tilavuus, 0.0)
        # current implementation assigns the parameter 'tilavuus' to saldo in that branch
        self.assertEqual(v.saldo, -1)

    def test_lisaa_varastoon_negative_does_nothing(self):
        v = Varasto(10, 5)
        v.lisaa_varastoon(-2)
        self.assertEqual(v.saldo, 5)

    def test_lisaa_varastoon_exceeding_sets_to_tilavuus(self):
        v = Varasto(10, 3)
        v.lisaa_varastoon(100)
        self.assertEqual(v.saldo, 10)

    def test_ota_varastosta_negative_returns_zero_and_keeps_saldo(self):
        v = Varasto(10, 4)
        ret = v.ota_varastosta(-1)
        self.assertEqual(ret, 0.0)
        self.assertEqual(v.saldo, 4)

    def test_ota_varastosta_more_than_saldo_returns_all_and_empties(self):
        v = Varasto(10, 4)
        ret = v.ota_varastosta(10)
        self.assertEqual(ret, 4)
        self.assertEqual(v.saldo, 0.0)
        self.assertEqual(v.paljonko_mahtuu(), 10.0)

    def test_str_representation_with_integers(self):
        v = Varasto(7, 2)
        self.assertEqual(str(v), "saldo = 2, vielä tilaa 5")

    def test_str_representation_with_floats(self):
        v = Varasto(3.5, 1.2)
        self.assertEqual(str(v), "saldo = 1.2, vielä tilaa 2.3")

