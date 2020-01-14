import time

from fly import Fly
from worm import Worm

from mod import MOD

fly = Fly()
worm = Worm()

mod = MOD()

mods = [worm, fly]

for m in mods:
    start_time = time.time()
    m.load_genes()
    print (" --- %s seconds --- " % (time.time() - start_time))

# mod.load_homologs()

for m in mods:
    start_time = time.time()
    m.load_go()
    print (" --- %s seconds --- " % (time.time() - start_time))

for m in mods:
    start_time = time.time()
    m.load_diseases()
    print (" --- %s seconds --- " % (time.time() - start_time))

mod.save_into_file()

mod.delete_mapping()
mod.put_mapping()

mod.index_genes_into_es()
mod.index_go_into_es()
mod.index_diseases_into_es()
