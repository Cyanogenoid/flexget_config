import sys, logging
from flexget.utils.tools import MergeException, merge_dict_from_to 
from flexget import manager, plugin 
from flexget.event import event 
from flexget.utils.template import render_from_task, get_template, RenderError 

log = logging.getLogger('twitter') 

schema = {
    'type': 'object',
    'properties': {
        'active': {'type': 'boolean', 'default': True},
        'template': {'type': 'string', 'default': 'Flexget: {{ title }} accepted'},
        'consumerkey': {'type': 'string'},
        'consumersecret': {'type': 'string'},
        'accesskey': {'type': 'string'},
        'accesssecret': {'type': 'string'}
    },
    'required': ['consumerkey', 'consumersecret', 'accesskey', 'accesssecret'],
    'additionalProperties': False
}

@event('manager.execute.started') 
def setup(manager, options):
    if not 'twitter' in manager.config:
        return
    try:
        import tweepy
    except ImportError:
        raise plugin.PluginError('The Twtter plugin requires the tweepy module to be installed, please install it before using.')
    global task_content
    task_content = {}
    for task in manager.tasks.itervalues():
        task.config.setdefault('twitter', {})
        try:
            merge_dict_from_to(config, task.config['twitter'])
        except MergeException as exc:
            raise PluginError('Failed to merge twitter config to task %s due to')
        task.config.setdefault('twitter', config)


class OutputTwitter(object):

    def on_task_output(self, task, config):
        # Initialize twitter client
        import tweepy
        auth = tweepy.OAuthHandler(config['consumerkey'], config['consumersecret'])
        auth.set_access_token(config['accesskey'], config['accesssecret'])
        api = tweepy.API(auth)
        for entry in task.accepted:
            try:
                content = entry.render(config['template'])
            except RenderError as e:
                log.error('Error rendering message: %s' % e)
                return
            if task.manager.options.test:
                log.info('Would update twitter with: %s' % content)
                continue
            try:
                api.update_status(status=content)
            except Exception as e:
                log.warning('Unable to post tweet: %s' % e) 

@event('plugin.register')
def register_plugin():
    plugin.register(OutputTwitter, 'twitter', api_ver=2) 
