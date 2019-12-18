import os
import re

from jinja2 import Environment, FileSystemLoader

import base64


class TemplateBuilder:
    last_data = None

    @staticmethod
    def template_render(content, data) -> str:
        """
        Render the supplied Jinja2 content with the supplied data

        :type content: str
        :param content: Jinja2 content

        :type data: dict
        :param data: Data to provide to the template

        :return: Rendered template
        """
        environment = Environment(loader=FileSystemLoader('./'))
        template = environment.from_string(content)
        template.globals['to_camel'] = TemplateBuilder.to_camel
        template.globals['to_title'] = TemplateBuilder.to_title
        template.globals['to_snake'] = TemplateBuilder.to_snake
        template.globals['to_upper'] = TemplateBuilder.to_upper
        template.globals['to_lower'] = TemplateBuilder.to_lower
        template.globals['to_csv'] = TemplateBuilder.to_csv
        template.globals['to_aws_resource_id'] = TemplateBuilder.to_aws_resource_id
        template.globals['to_aws_domain'] = TemplateBuilder.to_aws_domain
        template.globals['len'] = TemplateBuilder.len
        template.globals['coalesce'] = TemplateBuilder.coalesce
        template.globals['is_empty'] = TemplateBuilder.is_empty
        template.globals['is_list'] = TemplateBuilder.is_list
        template.globals['is_dict'] = TemplateBuilder.is_dict
        template.globals['read_file'] = TemplateBuilder.read_file
        template.globals['strip'] = TemplateBuilder.strip
        template.globals['base64_encode'] = TemplateBuilder.base64_encode
        template.globals['base64_decode'] = TemplateBuilder.base64_decode
        template.globals['load_template'] = TemplateBuilder.load_template
        template.globals['raise_error'] = TemplateBuilder.raise_error

        TemplateBuilder.last_data = data
        return template.render(data)

    @staticmethod
    def raise_error(error):
        """
        Raise an error from template

        :type error: str
        :param error: Message to display
        """
        print('Template Error: {error}'.format(error=error))
        exit(1)

    @staticmethod
    def to_aws_resource_id(name, invert=False):
        """
        Using an environments data, convert the name to AwsResourceId format

        :type name: str
        :param name: Name of the resource

        :type environment: dict
        :param environment: Environment dictionary

        :type invert: bool
        :param invert: Invert project/environment order

        :return: AWS resource ID string
        """
        environment = TemplateBuilder.last_data['environment']
        environment_id = environment['id']

        # If no project is specified use a placeholder 'Untitled'
        if 'project' not in environment['data']:
            project_name = 'Untitled'
        else:
            project_name = environment['data']['project']

        environment_id = TemplateBuilder.to_camel(environment_id)
        project_id = TemplateBuilder.to_camel(project_name)
        name = TemplateBuilder.to_camel(name)

        if invert is True:
            return "{environment_id}{project_id}{name}".format(
                environment_id=environment_id,
                project_id=project_id,
                name=name
            )

        return "{project_id}{environment_id}{name}".format(
            environment_id=environment_id,
            project_id=project_id,
            name=name
        )

    @staticmethod
    def to_aws_domain(name):
        """
        Using an environments data, convert the name to resource.environment.domain.com format

        :type name: str
        :param name: Name of the resource

        :type environment: dict
        :param environment: Environment dictionary

        :return: AWS resource ID string
        """
        environment = TemplateBuilder.last_data['environment']
        environment_id = environment['id']

        # If no project is specified use a placeholder 'Untitled'
        if 'project' not in environment['data']:
            project_name = 'Untitled'
        else:
            project_name = environment['data']['project']

        # If no domain is specified use a placeholder 'domain.com'
        if 'domain' in environment['data']:
            domain = environment['data']['domain']
        else:
            domain = 'domain.com'

        environment_id = TemplateBuilder.to_snake(environment_id)
        project_id = TemplateBuilder.to_snake(project_name)
        domain = TemplateBuilder.to_snake(domain)
        name = TemplateBuilder.to_snake(name)

        return "{name}.{environment_id}.{project_id}.{domain}".format(
            name=name,
            environment_id=environment_id,
            project_id=project_id,
            domain=domain
        )

    @staticmethod
    def to_snake(value, separator='-') -> str:
        """
        :type value: str
        :param value: String to convert

        :type separator: str
        :param separator: The separator to use

        :return: The input string converted to snake-case
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1{separator}\2'.format(separator=separator), value)
        return re.sub('([a-z0-9])([A-Z])', r'\1{separator}\2', s1).format(separator=separator).lower()

    @staticmethod
    def load_template(filename, data=None, indent=0, indent_width=1, indent_first=False, indent_character=' '):
        """
        Load template inside another template

        :type filename: str
        :param filename:

        :type data: dict or None
        :param data:

        :type indent: int
        :param indent:

        :type indent_width:
        :param indent_width:

        :type indent_first: bool
        :param indent_first:

        :type indent_character: str
        :param indent_character:
        """
        if data is None:
            data = {}

        last_data = TemplateBuilder.last_data
        template_root = last_data['template']['template_root']
        base_filename = '{template_root}/{filename}'.format(
            template_root=template_root.rstrip('/'),
            filename=filename.lstrip('/')
        )

        template_filename = base_filename

        # If the file doesn't exist, try with j2
        if os.path.exists(template_filename) is False:
            template_filename = "{base_filename}.j2".format(base_filename=base_filename)

        # Try with J2
        if os.path.exists(template_filename) is False:
            template_filename = "{base_filename}.J2".format(base_filename=base_filename)

        # If we haven't found it- die
        if os.path.exists(template_filename) is False:
            raise Exception('The requested template ({template_filename}) could not be found'.format(template_filename=template_filename))

        # Read the file and return its content
        file_object = open(template_filename, 'rt')
        content = file_object.read()
        file_object.close()

        last_data['data'].update(data)
        rendered_content = TemplateBuilder.template_render(content=content, data=last_data)

        if indent > 0:
            lines = rendered_content.split('\n')
            rendered_content = ''
            first = True
            for line in lines:
                for i in range(0, indent * indent_width):
                    if indent_first is True or first is False:
                        line = indent_character + line
                    first = False
                rendered_content += line + '\n'

        return rendered_content

    @staticmethod
    def coalesce(value_a, value_b):
        """
        Return value A unless it is empty (from left to right)

        :param value_a:
        :param value_b:
        :return:
        """
        if TemplateBuilder.is_empty(value_a):
            return value_b

        return value_a

    @staticmethod
    def is_empty(value):
        """
        Check if value is empty

        :return:
        """
        if value is None:
            return True

        if isinstance(value, str):
            if len(value.strip()) == 0:
                return True

        if value:
            return False

        return True

    @staticmethod
    def to_csv(value):
        """
        Convert list to CSV string
        :param value:
        :return: CSV string
        """
        if isinstance(value, str) is True:
            return value

        result = ''
        for item in value:
            result += '"{item}",'.format(item=item.replace('"', '\\"'))

        return result[:-1]

    @staticmethod
    def len(value):
        """
        Return length of supplied value

        :param value: Value to test

        :return: Length
        """
        return len(value)

    @staticmethod
    def is_list(value):
        """
        Return boolean indicating whether the supplied value is a list

        :param value: Value to test

        :return: Boolean flag
        """
        return isinstance(value, list)

    @staticmethod
    def is_dict(value):
        """
        Return boolean indicating whether the supplied value is a dictionary

        :param value: Value to test

        :return: Boolean flag
        """
        return isinstance(value, dict)

    @staticmethod
    def strip(value):
        """
        Strip whitespace from value

        :type value: str
        :param value:

        :return: Stripped value
        """
        return value.strip()

    @staticmethod
    def read_file(filename):
        """
        :type filename: str
        :param filename:

        :return: The files contents
        """
        file = open(filename, 'rt')
        content = str(file.read())
        file.close()

        return content

    @staticmethod
    def to_title(value):
        """
        Convert value to title case

        :type value: str
        :param value: 
        :return: The value in title case
        """
        return str(value).title()

    @staticmethod
    def to_camel(value, separator='-', include_first=True):
        """
        Convert 'dash-value' to 'CamelValue'

        :type value: str
        :param value:

        :type separator: str
        :param separator: The dashes used as separator

        :type include_first: bool
        :param include_first:

        :return: Camel case variant of string
        """
        components = value.split(separator)

        if include_first is True:
            return ''.join(x.title() for x in components)

        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def to_upper(value):
        """
        Convert value to upper case

        :type value: str
        :param value:

        :return: The value in upper case
        """
        return str(value).upper()

    @staticmethod
    def to_lower(value):
        """
        Convert value to lower case

        :type value: str
        :param value:

        :return: The value in lower case
        """
        return str(value).lower()

    @staticmethod
    def base64_encode(value):
        """
        Base 64 encode the specified value

        :type value: str
        :param value:

        :return: The Base 64 encoded value
        """
        return base64.encodebytes(bytes(value, 'utf-8')).decode('ascii').strip()

    @staticmethod
    def base64_decode(value):
        """
        Base 64 decode the specified value

        :type value: str
        :param value:

        :return: The Base 64 decoded value
        """
        return base64.decodebytes(value.encode('utf-8'))
