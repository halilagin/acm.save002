name=acm-ml-mult-clsf-runner-compose
screen -Sdm $name -t doc-comp  vim docker-compose.yml && \
screen -S $name -X screen -t tab1 bash && \
screen -S $name -X screen -t tab2 bash && \
screen -S $name -X screen -t tab3 bash && \
screen -S $name -X screen -t tab4 bash && \
screen -S $name -X screen -t tab5 bash && \
screen -S $name -X screen -t tab6 bash && \
screen -S $name -X screen -t tab7 bash && \
screen -S $name -X screen -t tab8 bash && \
screen -S $name -X screen -t tab9 bash && \
screen -r -d $name
