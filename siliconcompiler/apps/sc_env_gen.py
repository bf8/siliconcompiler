# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.
import sys
import siliconcompiler

def main():
    progname = "sc-env-gen"
    chip = siliconcompiler.Chip()
    switchlist = ['cfg',
                  'project',
                  'version']
    description = """
    -----------------------------------------------------------
    Restricted SC app to set up a project working environment
    based on a project name or manifest.
    -----------------------------------------------------------
    """
    chip.create_cmdline(progname,
                        switchlist=switchlist,
                        description=description)


    #Error checking
    if bool(not chip.get('cfg')) and bool(not chip.get('project')):
        #print(progname+": error: the following arguments are required: [-cfg | -project]")
        #sys.exit()
        with open('test.sh', 'w') as test_env:
            test_env.write('export SC_TEST_VAR="test_val2"')
    else:
        chip.create_env()

#########################
if __name__ == "__main__":
    sys.exit(main())