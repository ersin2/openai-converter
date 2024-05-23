import re
import yaml

def parse_markdown(markdown_content):
    api_spec = {
        'openapi': '3.0.0',
        'info': {
            'title': 'API Documentation',
            'version': '1.0.0'
        },
        'paths': {}
    }

    # Regular expressions to match sections
    path_re = re.compile(r'## (GET|POST|PUT|DELETE) (\/[^\s]*)')
    param_re = re.compile(r'- (\w+): (.*)')

    lines = markdown_content.split('\n')
    current_path = None
    current_method = None

    for line in lines:
        path_match = path_re.match(line)
        if path_match:
            current_method, current_path = path_match.groups()
            if current_path not in api_spec['paths']:
                api_spec['paths'][current_path] = {}
            api_spec['paths'][current_path][current_method.lower()] = {
                'summary': '',
                'responses': {
                    '200': {
                        'description': 'Successful response'
                    }
                }
            }
            continue

        if current_path and current_method:
            param_match = param_re.match(line)
            if param_match:
                param_name, param_description = param_match.groups()
                if 'parameters' not in api_spec['paths'][current_path][current_method.lower()]:
                    api_spec['paths'][current_path][current_method.lower()]['parameters'] = []
                api_spec['paths'][current_path][current_method.lower()]['parameters'].append({
                    'name': param_name,
                    'in': 'query',
                    'description': param_description,
                    'required': False,
                    'schema': {
                        'type': 'string'
                    }
                })

    return api_spec

def markdown_to_openapi(markdown_file, output_file):
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()
    
    api_spec = parse_markdown(markdown_content)
    
    with open(output_file, 'w') as f:
        yaml.dump(api_spec, f, sort_keys=False)

# Example usage:
markdown_to_openapi('api.md', 'openapi.yaml')
