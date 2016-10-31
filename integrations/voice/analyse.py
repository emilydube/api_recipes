# -*- coding: utf-8 -*-
#
# Copyright © 2016 Receptiviti
#
#

from ConfigParser import SafeConfigParser
from argparse import ArgumentParser
from providers.nuance import Nuance, NuanceConfig
from receptiviti.content import Content, ReceptivitiConfig
import json


def parse_arguments():
    parser = ArgumentParser(description='Analyse text from an audio file')
    parser.add_argument('-p', '--provider', dest='provider', help='transcription provider to use', default='nuance')
    parser.add_argument('-c', '--config', dest='config_file', help='config file to read', default='config.ini')
    parser.add_argument('audio_file', help='audio file to transcribe')
    parser.add_argument('source_id', help='id of person being transcribed')

    return parser.parse_args()


def read_config(config_file):
    config = SafeConfigParser()
    config.read(config_file)
    return config


def provider_factory(args, config):
    provider = None

    if args.provider == 'nuance':
        nuance_config = NuanceConfig.from_config_file(config)
        provider = Nuance(nuance_config, args.audio_file, args.source_id)

    return provider


args = parse_arguments()

config = read_config(args.config_file)

provider = provider_factory(args, config)
if provider is None:
    print 'unknown provider: {}'.format(args.provider)
    exit(1)

text = provider.transcribe()
print 'Transcribed text: ', text, "\n"

# got the text - hand it to Receptiviti to analyse
receptiviti_config = ReceptivitiConfig.from_config_file(config)
content = Content(receptiviti_config,  # the api key and secret from the config file
                   args.source_id,     # use the source id as the person name
                   Content.MALE,       # this is a male
                   args.source_id,     # use the source id as the person handle
                   args.audio_file,    # use the audio file name as the content handle
                   Content.OTHER,      # set the content source to other
                   'english',          # this is an english content
                   text)               # this is the content

profile = content.analyse()
print 'Profile: ', json.dumps(json.loads(profile), indent=4)
