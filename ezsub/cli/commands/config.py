#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezsub.conf import UserConf, display_configs

def config(req):
    configs = UserConf()
    if req.subcommand == 'show':
        display_configs(configs.path)

    elif req.subcommand == 'set':
        section, option = req.option.split('.')
        configs.set_option(section, option, req.value)
