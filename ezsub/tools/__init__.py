#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def to_screen(msg='', silent=False, **kwargs):
    if not silent:
        print(str(msg), **kwargs)
