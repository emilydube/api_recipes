from datetime import datetime
import os
import random
import uuid
from conftest import writing_sample

__author__ = 'skaranth'


def get_writing_sample_data(**kwargs):
    attribs = {
        "content": writing_sample,
        "content_source": random.randint(1, 2),
        "client_reference_id": uuid.uuid4().hex,
        "sample_date": datetime.now().isoformat(),
        "recipient": None,
        "tags": ['tag1', 'tag2', 'tag3'],
        'language': 'english'
    }
    attribs.update(kwargs)
    return attribs


def get_person_data(writing_sample=None):
    person_data = {'name': "John {0} Doe".format(uuid.uuid4().hex), 'client_reference_id': uuid.uuid4().hex, 'gender': 1}
    if writing_sample:
        person_data["writing_sample"] = writing_sample
    return person_data


def get_sample_csv_file(file_name):
    current_dir = os.path.dirname(os.path.realpath(__file__))

    test_file = os.path.join(current_dir, file_name)
    return test_file

