import os
import yaml

from TemplateEngine.TemplateBuilder import TemplateBuilder


class TemplateEngine:
    templates = {}
    template_path = None
    config_path = None

    @staticmethod
    def generate(environment, template_root='templates', config_root='config'):
        """
        Generate output template

        :type config_root: str
        :param config_root: The base path under which the configuration files are located

        :type template_root: str
        :param template_root: The base path under which templates are located

        :type environment: str
        :param environment: The name of the environment to build

        :return:
        """
        TemplateEngine.config_path = config_root
        TemplateEngine.template_path = template_root

        path = '{config_root}/{environment}'.format(config_root=config_root, environment=environment)

        # Load configuration file for the environment
        config = {}
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower() == 'config.yaml' or file.lower() == 'config.yml':
                    filename = os.path.join(root, file)
                    file = open(filename, 'rt')
                    yaml_content = yaml.full_load(file)
                    file.close()
                    for block_id, block in yaml_content.items():
                        if id == 'config':
                            config.update(block_id)

        # Render templates
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.yaml') or file.lower().endswith('.yml'):
                    # Mangle the filename several different ways
                    filename = os.path.join(root, file)
                    basename = os.path.basename(filename)
                    path = filename[:-len(basename)].strip('/')
                    path_components = filename[:-len(basename)].strip('/').split('/')
                    split_basename = os.path.splitext(basename)
                    if len(split_basename) > 1:
                        extension = split_basename[1]
                    else:
                        extension = ''

                    # Load the YAML content into dictionary
                    file = open(filename, 'rt')
                    yaml_content = yaml.full_load(file)
                    file.close()

                    # Skip if no template was defined
                    if 'template' not in yaml_content.keys():
                        continue

                    template = yaml_content['template']

                    # Load the template
                    template_content = TemplateEngine.load_template_file(template['filename'])

                    template_data = {}
                    if 'data' in template.keys():
                        template_data = template['data']

                    data = {
                        'environment': environment,
                        'config': config,
                        'data': template_data,
                        'template': {
                            'config_root': config_root,
                            'template_root': template_root,
                            'path': path,
                            'directory': path_components[-1],
                            'filename': split_basename[0],
                            'extension': extension
                        }
                    }

                    TemplateBuilder.last_data = data
                    template_rendered = TemplateBuilder.template_render(
                        content=template_content,
                        data=data
                    )

                    # Remove blank lines from the template, and standard tabs to 4 spaces
                    output_content = ''
                    lines = template_rendered.split('\n')
                    for line in lines:
                        if len(line.strip()) > 0:
                            output_content += '{line}\n'.format(line=line.rstrip().replace('\t', '    '))
                    output_filename = '{environment}-{filename}.yml'.format(
                        environment=path_components[-1].lower(),
                        filename=basename.lower()
                    )
                    output_file = open(output_filename, 'wt')
                    output_file.write(output_content)
                    output_file.close()

    @staticmethod
    def load_template_file(filename) -> str:
        """
        Load Jinja2 template file from disk

        :type filename: str
        :param filename: The filename of the template to be loaded (relative to the /templates/ path)

        :return: The content of the content
        """
        # Make sure the template is relative to the template folder and ends with a '.j2' extension
        filename = TemplateEngine.template_path + '/' + filename.lstrip('/')

        if filename.endswith('.j2') is False:
            filename += '.j2'

        # Make sure the template exists
        if os.path.exists(filename) is False:
            print('ERROR: Could not locate template ({filename})'.format(filename=filename))
            exit(1)

        # Read the file and return its content
        file_object = open(filename, 'rt')
        template_content = file_object.read()
        file_object.close()

        return template_content
