import sys

from TemplateEngine.TemplateEngine import TemplateEngine

if __name__ == '__main__':
    environment = sys.argv[1]
    template_root = sys.argv[2]
    config_root = sys.argv[3]
    output_filename = sys.argv[4]

    TemplateEngine.generate(
        environment=environment,
        template_root=template_root,
        config_root=config_root,
        output_filename=output_filename
    )

