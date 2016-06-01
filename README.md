CREMI Python Scripts
====================

Python scripts associated with the [CREMI Challenge](http://cremi.org).

Installation
------------

If you are using `pip`, installing the scripts is as easy as

```
pip install git+https://github.com/cremi/cremi_python.git
```

Alternatively, you can clone this repository yourself and use `distutils`
```
python setup.py install
```
or just include the `cremi_python` directory to your `PYTHONPATH`.

Reading and writing of CREMI files
----------------------------------

We recommend you use the `cremi.io` package for reading and writing of the
CREMI files. This way, you can be sure that the submissions you produce are of
the form that is expected by the challenge server, and that compression is
used.

You open a file by instantiating a `CremiFile` object:
```python
from cremi.io import CremiFile
file = CremiFile("example.hdf", "r")
```
The second argument specifies the mode, which is `"r"` for reading, `"w"` for
writing a new file (careful, this replaces an existing file with the same
name), and `"a"` to append or change an existing file.

The `CremiFile` class provides read and write methods for each of the challenge
datasets. To read the neuron IDs in the training volumes, for example, use
`read_neuron_ids()`:
```python
(neuron_ids, neuron_ids_resolution, neuron_ids_offset, neuron_ids_comment) = file.read_neuron_ids()
```
This returns the `neuron_ids` as a `numpy` array, along with some meta-information. If you are using the padded version of the volumes, `neuron_ids_offset` will contain the starting point of `neuron_ids` inside the `raw` volume. Note that these numbers are given in nm.

To save a dataset, use the appropriate write method, e.g.,:
```
file.write_neuron_ids(neuron_ids, (40.0, 4.0, 4.0), comment="λ=0.1, LP relaxation + rounding")
```
Here, you can optionally give a comment for your own convenience. It will not
be visible on the challenge website.

Evaluation
----------

Coming soon!

Acknowledgements
----------------

Evaluation code contributed by:

  * [Juan Nunez-Iglesias](http://github.com/jni)
  * [Philipp Hanslovsky](http://github.com/hanslovsky)
  * [Stephan Saalfeld](http://github.com/axtimwalde)
