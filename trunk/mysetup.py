#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Filename:mysetup.py

from distutils.core import setup
import py2exe

includes=["encodings","encodings.*"]
          
options={"py2exe":
         {"compressed":1,
             'includes':includes,
             "ascii":1,
             "optimize":2,
             "bundle_files":1}
        }

setup(
    version="2.4.0",
    description="crawl info from taobao",
    name="crawler",
    console=[{"script":"tb_crawl_queue.py",
                "icon_resources":[(1,"myapp.ico")]
                }],
    data_files=[('.', ['shop.txt'])], 
    options=options,
    zipfile=None)
