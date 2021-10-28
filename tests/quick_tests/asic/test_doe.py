import siliconcompiler
import multiprocessing
import os

# unit routine
def run_design(rootdir, design, N, job):

    chip = siliconcompiler.Chip(loglevel='INFO')
    chip.set('design', design)
    chip.add('source', rootdir+'/stdlib/hdl/'+design+'.v')
    chip.set('param', 'N', str(N))
    chip.set('jobname', job)
    chip.set('relax', True)
    chip.set('quiet', True)
    chip.set('steplist', ['import', 'syn'])
    chip.target("asicflow_freepdk45")
    chip.run()

def test_doe():
    '''Test running multiple experiments sweeping different parameters in
    parallel using multiprocessing library.'''

    rootdir = (os.path.dirname(os.path.abspath(__file__)) +
           "/../../../third_party/designs/oh/")
    design = 'oh_add'
    N = [4, 8, 16, 32, 64, 128]

    # Define parallel processingg
    processes = []
    for i in range(len(N)):
        job = 'job' + str(i)
        processes.append(multiprocessing.Process(target=run_design,
                                                args=(rootdir,
                                                      design,
                                                      str(N[i]),
                                                      job
                                                )))

    # Boiler plate start and join
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    # Post-processing data
    chip = siliconcompiler.Chip()
    prev_area = 0
    for i in range(len(N)):
        jobname = 'job'+str(i)
        chip.read_manifest(f"build/{design}/{jobname}/syn/0/outputs/{design}.pkg.json", job=jobname)
        area = chip.get('metric','syn','0','cellarea','real', job=jobname)

        # expect to have increasing area as we increase adder width
        assert area > prev_area
        prev_area = area