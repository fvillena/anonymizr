import unittest
import src
import pandas as pd
import numpy as np
import tempfile
import shutil
import os

def assert_series_not_equal(*args, **kwargs):
    try:
        pd.testing.assert_series_equal(*args, **kwargs)
    except AssertionError:
        # frames are not equal
        pass
    else:
        # frames are equal
        raise AssertionError

class TestHasherMd5(unittest.TestCase):
    def test_hasher_md5(self):
        self.assertEqual(src.hasher("12345678-5","test","md5") ,"69e16c0da5c871e99ce521cac1fe8429" )
    def test_hasher_md5_equal(self):
        self.assertEqual(src.hasher("12345678-5","test","md5") ,src.hasher("12345678-5","test","md5") )
    def test_hasher_md5_number(self):
        self.assertEqual(src.hasher(123,"test","md5"), "abe45d28281cfa2a4201c9b90a143095")
    def test_hasher_md5_na(self):
        self.assertTrue(pd.isnull(src.hasher(np.nan,"test","md5")))
    def test_hasher_md5_is_str(self):
        self.assertIsInstance(src.hasher("12345678-5","test","md5"), str)
class TestHasherInt(unittest.TestCase):
    def setUp(self):
        self.identifiers = ["12345678-5","11111111-5"]
    def test_hasher_int_int(self):
        self.assertIsInstance(src.hasher(self.identifiers[0],"test","int"), int)
    def test_hasher_int_equal(self):
        self.assertEqual(src.hasher(self.identifiers[0],"test","int"),src.hasher(self.identifiers[0],"test","int"))
    def test_hasher_int_not_equal(self):
        self.assertNotEqual(src.hasher(self.identifiers[0],"test","int"),src.hasher(self.identifiers[1],"test","int"))
    def test_hasher_int_less_than(self):
        self.assertTrue(src.hasher(self.identifiers[0],"test","int") < 10000)
        self.assertTrue(src.hasher(self.identifiers[1],"test","int") < 10000)

test_df = pd.DataFrame(
    {
        "identifier1": ["12345678-5","11111111-5","00000000-5","11111111-5"],
        "identifier2": ["123","111","000","000"],
        "blank1": ["Juan", "Pedro","Jorge","Juan"],
        "blank2": ["Chile","Paraguay","Uruguay","Argentina"],
        "date1": [np.nan,"1900-02-02","2000-01-01","1900-02-02"],
        "date2": ["1910-01-01","1920-02-02","2030-01-01","1940-02-02"],
        "normal1": ["1","2","3","4"],
        "normal2": ["a","b","c","d"]
    },
    dtype=object
)

class TestAnonymizer(unittest.TestCase):
    def setUp(self):
        self.new_df = src.anonymize(test_df,"identifier1",["identifier1","identifier2"],["blank1","blank2"],["date1","date2"],"test")
    def test_hashing_not_equal(self):
        assert_series_not_equal(
            test_df.identifier1,
            self.new_df.identifier1
        )
    def test_blanking(self):
        self.assertTrue(
            self.new_df.blank1.isna().all()
        )
        self.assertTrue(
            self.new_df.blank2.isna().all()
        )
    def test_date_not_equal(self):
        self.assertFalse(
            (test_df.date1 == self.new_df.date1).all()
        )
    def test_date_difference_equal(self):
        pd.testing.assert_series_equal(
            (pd.to_datetime(test_df.date2, errors="coerce") - pd.to_datetime(test_df.date1, errors="coerce")), 
            (self.new_df.date2 - self.new_df.date1)
        )
class TestLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_excel_file_location = os.path.join(self.test_dir, 'test.xlsx')
        test_df.to_excel(self.test_excel_file_location,index=False)
        self.test_csv_file_location = os.path.join(self.test_dir, 'test.csv')
        test_df.to_csv(self.test_csv_file_location,index=False)
    def test_load_excel(self):
        df_from_excel = src.load_dataset(self.test_excel_file_location)
        pd.testing.assert_frame_equal(
            df_from_excel,
            test_df
        )
    def test_load_csv(self):
        df_from_csv = src.load_dataset(self.test_csv_file_location)
        pd.testing.assert_frame_equal(
            df_from_csv,
            test_df
        )
    def tearDown(self):
        shutil.rmtree(self.test_dir)
if __name__ == '__main__':
    unittest.main()