from construction_system.models.template import Template

def get_template():
    return Template(template_id='cli_tool',name='cli_tool',description='cli_tool template',template_type='CLI_TOOL',language='python',template_string="import argparse\ndef main():\n    p=argparse.ArgumentParser(description='{{description}}')\n    sub=p.add_subparsers(dest='cmd')\n{{commands|indent:4}}\n    a=p.parse_args();print(a)\nif __name__=='__main__':main()\n",variables=[])
