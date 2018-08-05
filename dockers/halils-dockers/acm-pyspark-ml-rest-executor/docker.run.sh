docker  run --name acm-mult-clsf-test  --network acmnet -v `pwd`:/home/jovyan/acm/ml/classification/text-clsf  --detach-keys="ctrl-k,k,k"  -ti acm-mult-clsf-runner:0.0.1 bash
#docker  run --name acm-mult-clsf  --detach-keys="ctrl-l,l,l" -d acm-mult-clsf-runner:0.0.1
