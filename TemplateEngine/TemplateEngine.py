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

        yaml_environment_data = {
            'id': environment,
            'paths': {
                'template': template_root,
                'config': config_root
            },
            'data': {}
        }
        yaml_block_data = {}
        yaml_resource_templates = {}

        # Load configuration files
        path = '{config_root}/{environment}'.format(config_root=config_root, environment=environment)

        # Load all YAML files
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.yaml') or file.lower().endswith('.yml'):
                    filename = os.path.join(root, file)

                    # Read the YAML
                    file = open(filename, 'rt')
                    yaml_content = yaml.full_load(file)
                    file.close()

                    # Extract the configuration blocks from the YAML
                    for block_type, block in yaml_content.items():
                        if block_type == 'render':
                            # Render block found
                            if 'template' not in block:
                                print('ERROR: Render block did not specify template name ({filename})'.format(filename=filename))
                                exit(1)
                            template = block['template']

                            # Get data for the template
                            if 'data' in block:
                                data = block['data']
                            else:
                                data = {}

                            data['filename'] = os.path.basename(filename)

                            yaml_resource_templates[template] = TemplateEngine.load_template_file(template)
                            yaml_block_data[template] = data
                        elif block_type == 'environment':
                            # Environment data block found
                            yaml_environment_data['data'].update(block)

        return TemplateEngine.create_template(
            environment_data=yaml_environment_data,
            block_data=yaml_block_data,
            block_templates=yaml_resource_templates
        )

    @staticmethod
    def create_template(environment_data, block_data, block_templates) -> str:
        """
        Create the CloudFormation files resources section

        :type environment_data: dict
        :param environment_data: Dictionary containing data exposed to all blocks in the environment

        :type block_data: dict
        :param block_data: Dictionary containing the data supplied to each block
        
        :type block_templates: dict
        :param block_templates: Dictionary containing each of the block templates we need to render

        :return: The compiled output
        """
        blocks = []

        for block_id, block in block_data.items():
            data = {
                'environment': environment_data,
                'this': {
                    'id': block_id,
                    'data': block
                }
            }

            blocks.append(TemplateBuilder.template_render(content=block_templates[block_id], data=data))

        file_output = ''

        for block in blocks:
            lines = block.split('\n')
            for line in lines:
                if len(line.strip()) > 0:
                    file_output += '{line}\n'.format(line=line.rstrip().replace('\t', '    '))
            file_output += '\n'

        return file_output

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
