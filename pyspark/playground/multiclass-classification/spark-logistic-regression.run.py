#!/usr/bin/env python

import time
import subprocess
import argparse
import os
import tempfile

from lightning import Lightning

from pythonwrapper.util import findspark, findjar, baseargs

def main():

    # parse arguments
    parser = argparse.ArgumentParser(description='Spark Logistic  Regression.')
    parser = baseargs(parser)

    '''
    parser.add_argument('-nc', '--ncenters', type=int, default=3, required=False, 
        help='Number of cluster centers')
    parser.add_argument('-nd', '--ndims', type=int, default=2, required=False, 
        help='Number of dimensions')
    parser.add_argument('-rs', '--randomseed', type=int, default=None, required=False,
        help='Random seed')
    parser.add_argument('-sd', '--std', type=float, default=0.3, required=False,
        help='Standard deviation of points')
    parser.add_argument('-up', '--update', type=str, choices=('jump', 'drift', 'none'), default='drift', required=False,
        help='Update behavior')
    '''
    parser.add_argument('-a', '--autoopen', type=bool, choices=(True, False), default=True, required=False,
        help='Whether to automatically open Lightning session on a browser')
    parser.add_argument('-laddr', '--lightningAddr', type=str, choices=('http://acm:3010'), default='http://acm:3010', required=False,
        help='Lightning server address')
    args = parser.parse_args()
    # basic setup
    sparkhome = findspark()
    jar = findjar()
    
    # set up lightning
    print ("lgn address", args.lightningAddr)
    lgn = Lightning(args.lightningAddr)
    lgn.create_session('spark-logistic-regression')
    if (args.autoopen):
        lgn.session.open()

    # set temp path
    path = args.path
    if not path or path == '':
        path = tempfile.gettempdir()
    tmpdir = os.path.join(path, 'sparklogisticregression')

    # setup the demo
    #s = StreamingDemo.make('kmeans', npoints=args.npoints, nbatches=args.nbatches)
    #s.setup(tmpdir, overwrite=args.overwrite)
    #s.params(ncenters=args.ncenters, ndims=args.ndims, std=args.std, seed=args.randomseed, update=args.update)

    # setup the spark job
    sparkSubmit = sparkhome + "/bin/spark-submit"
    sparkArgs = ["--class", "spark.classification.LogisticRegressionWithLBFGSExample", jar]
    #demoArgs = [s.datain, s.dataout, str(args.batchtime), str(args.ncenters), str(args.ndims), str(args.halflife), str(args.timeunit)]
    demoArgs = []
    cmd = [sparkSubmit] + sparkArgs + demoArgs

    try:
        # start the spark job    
        p = subprocess.Popen(cmd)
        # wait for spark streaming to start up
        time.sleep(4)
        # start the demo
        #s.run(lgn)

    finally:
        pass
       #p.kill()

if __name__ == "__main__":
    main()

