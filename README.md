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
neuron_ids = file.read_neuron_ids()
```
This returns the `neuron_ids` as a `cremi.Volume`, which contains an HDF5 dataset (`neuron_ids.data`) and some meta-information. If you are using the padded version of the volumes, `neuron_ids.offset` will contain the starting point of `neuron_ids` inside the `raw` volume. Note that these numbers are given in nm.

To save a dataset, use the appropriate write method, e.g.,:
```
file.write_neuron_ids(neuron_ids)
```
See the included `example_read.py` and `example_write.py` for more details.

Evaluation
----------

For each of the challenge categories, you find an evaluation class in
`cremi.evaluation`, which are `NeuronIds`, `Clefts`, and `SynapticPartners`.

After you read a test file `test` and a ground truth file `truth`, you can
evaluate your results by instantiating these classes as follows:
```python
from cremi.evaluation import NeuronIds, Clefts, SynapticPartners

neuron_ids_evaluation = NeuronIds(truth.read_neuron_ids())
(voi_split, voi_merge) = neuron_ids_evaluation.voi(test.read_neuron_ids())
adapted_rand = neuron_ids_evaluation.adapted_rand(test.read_neuron_ids())

clefts_evaluation = Clefts(test.read_clefts(), truth.read_clefts())
fp_count = clefts_evaluation.count_false_positives()
fn_count = clefts_evaluation.count_false_negatives()
fp_stats = clefts_evaluation.acc_false_positives()
fn_stats = clefts_evaluation.acc_false_negatives()

synaptic_partners_evaluation = SynapticPartners()
fscore = synaptic_partners_evaluation.fscore(
    test.read_annotations(),
    truth.read_annotations(),
    truth.read_neuron_ids())
```
See the included `example_evaluate.py` for more details. The metrics are
described in more detail on the [CREMI Challenge website](http://cremi.org/metrics/).

Acknowledgements
----------------

Evaluation code contributed by:

  * [Jan Funke](https://github.com/funkey)
  * [Juan Nunez-Iglesias](http://github.com/jni)
  * [Philipp Hanslovsky](http://github.com/hanslovsky)
  * [Stephan Saalfeld](http://github.com/axtimwalde)
