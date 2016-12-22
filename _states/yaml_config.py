import salt.exceptions

def set_value(name, key, value):
    '''
    Change a value of a key in a YAML document

    name
        The YAML file to modify
    key
        The key to modify. Can specify the whole path, with tokens delimited by '/'
    value
        The new value    
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': '',
        'pchanges': {},
    }

    current_yaml = __salt__['yaml.load_yaml'](name)
    current_value = __salt__['yaml.get_value'](current_yaml, key)

    if current_value == value:
        ret['result'] = True
        ret['comment'] = 'The key \'' + key + '\' already has the value \'' + value + '\''
        return ret

    if __opts__['test'] == True:
        ret['comment'] = 'The value of \'' + key + '\' will be changed'
        ret['pchanges'] = {
            'old': current_value,
            'new': value,
        }
        
        ret['result'] = None

        return ret
    
    new_state = __salt__['yaml.modify_yaml'](current_yaml, key, value)

    __salt__['yaml.save_yaml'](current_yaml, name)

    ret['comment'] = 'The state of "{0}" was changed!'.format(name)

    ret['changes'] = {
        'old': current_value,
        'new': value,
    }

    ret['result'] = True    

    return ret