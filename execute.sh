#!/bin/bash
cd /home/flexget/.flexget
source /home/flexget/flexget/bin/activate
python config.py > config.yml
flexget --cron execute
