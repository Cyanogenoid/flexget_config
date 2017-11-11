import yaml


with open('anime.yml') as fd:
  anime = yaml.load(fd)

anime['settings'] = {}
for group in anime.keys():
    if group == 'settings':
        continue
    settings = anime['settings'].setdefault(group, {})
    settings['from_group'] = group
    settings['quality'] = '720p'
    settings['identified_by'] = 'sequence'
    settings['tracking'] = 'backfill'


config = '''
templates:
  global:
    make_rss:
      file: ~/public_html/flexget.rss
      days: -1
      items: 32
      title: "{{{{title}}}}"
      template: "bare"
  anime:
    series: {}

tasks:
  nyaa:
    template: [anime]
    rss: http://www.nyaa.si/?page=rss&c=1_2&f=1
    include:
      - twitter.yml
    assume_quality: 720p
    discover:
      what:
        - next_series_episodes:
            from_start: yes
            backfill: yes
      from:
        - nyaa:
            category: anime eng
            filter: filter remakes 
      interval: 12 hours
      release_estimations: ignore
'''

print(config.format(anime))
