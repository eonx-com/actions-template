import sys

from TemplateEngine.TemplateEngine import TemplateEngine

if __name__ == '__main__':
    environment = sys.argv[1]
    template_path = sys.argv[2]
    config_path = sys.argv[3]
    output_filename = sys.argv[4]

    template = TemplateEngine.generate(
        environment=environment,
        template_path=template_path,
        config_path=config_path
    )

    file = open(output_filename, 'wt')
    file.write(template)
    file.close()
