# -*- coding: utf-8 -*-
"""STIR DataContainer algebra tests
v{version}

Usage:
  tests_five [--help | options]

Options:
  -r, --record   record the measurements rather than check them
  -v, --verbose  report each test status

{author}

{licence}
"""
from sirf.Utilities import assert_validities, petmr_data_path, \
     existing_filepath, pTest, RE_PYEXT
from sirf.STIR import MessageRedirector, AcquisitionData
__version__ = "0.2.2"
__author__ = "Casper da Costa-Luis, Edoardo Pasca"


def test_main(rec=False, verb=False, throw=True):
    datafile = RE_PYEXT.sub(".txt", __file__)
    test = pTest(datafile, rec, throw=throw)
    test.verbose = verb

    msg_red = MessageRedirector()

    data_path = petmr_data_path('pet')
    raw_data_file = existing_filepath(data_path, 'my_forward_projection.hs')
    acq_data = AcquisitionData(raw_data_file)

    if verb:
        print('Checking images algebra:')
    image_data = acq_data.create_uniform_image(1.0)
    dims = image_data.dimensions()
    # N number of elements in the array
    N = 1
    for i,el in enumerate(len(dims)):
        N *= el
    
    # 1 test sum: N * 1 / N = 1
    test.check(image_data.sum()/N) 
    # test algebra 2 to 5
    # 2 scalar add 1 + 1 = 2
    b = image_data + 1.
    test.check(b.sum()/N) 
    # 3 DataContainer add (2+1) = 3
    c = b + image_data
    test.check(b.sum()/N) 
    # 4 scalar subtract (1 - 1) = 0
    b = image_data - 1.
    test.check(b.sum()/N)
    # 5 DataContainer subtract 1 - (1 + 1) = -1
    b = image_data + 1.
    c = image_data - b
    test.check(c.sum()/N)
    # 6 scalar multiply (1 * 3) = 3
    b = image_data * 3.
    test.check(b.sum()/N) 
    # 7 DataContainer multiply ( 3 * 1 ) = 3
    c = b * image_data
    test.check(c.sum()/N)
    # 8 scalar divide 1 / 2 = 0.5
    b = image_data / 2.
    test.check(b.sum()/N) 
    # 9 DataContainer divide (1 / 0.5) = 2.
    c = image_data / b
    test.check(c.sum()/N)
    # reverse operands 
    # 10 scalar add 1 + 1 = 2
    b = 1. + image_data 
    test.check(b.sum()/N) 
    # 11 scalar subtract (1 - 1) = 0
    b = 1. - image_data 
    test.check(b.sum()/N) 
    # 12 scalar multiply 3*1 = 3
    b = 3. * image_data 
    test.check(b.sum()/N) 
    # 13 scalar divide 0.5 / 1 = 0.5
    b = 0.5 / image_data
    test.check(b.sum()/N)
    # 14 power
    b = 1.5*image_data
    c = b.power(0.5)
    test.check(c.sum()/N)
    # 15 maximum
    test.check(c.maximum(b).sum()/N)
    # 16 sign 
    b = -1 * image_data 
    test.check(b.sign().sum()/N)
    # 17 abs
    test.check(b.abs().sum()/N)
    # 18 sqrt
    b = 1.5*image_data
    c = b.sqrt()
    test.check(c.sum()/N)
    # inline algebra
    # 19 inline add
    b = acq_data.create_uniform_image(1.5)
    b += 0.5
    test.check(b.sum()/N)
    # 20 inline subtract
    b = acq_data.create_uniform_image(1.5)
    b -= 0.5
    test.check(b.sum()/N)
    # 21 inline multiply
    b = acq_data.create_uniform_image(1.5)
    b *= 2
    test.check(b.sum()/N)
    # 22 inline divide
    b = acq_data.create_uniform_image(1.5)
    b /= 3
    test.check(b.sum()/N)

    

    return test.failed, test.ntest


if __name__ == "__main__":
    runner(test_main, __doc__, __version__, __author__)
