import sys

from TemplateEngine.TemplateEngine import TemplateEngine

if __name__ == '__main__':
    environment = sys.argv[1]
    template_root = sys.argv[2]
    config_root = sys.argv[3]
    output_path = sys.argv[4]
    output_prefix = sys.argv[5]
    output_suffix = sys.argv[6]

    TemplateEngine.generate(
        environment=environment,
        template_root=template_root,
        config_root=config_root,
        output_path=output_path,
        output_prefix=output_prefix,
        output_suffix=output_suffix
    )

