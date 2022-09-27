source ./IP_Setup_Master.bash
xterm -hold -e "sleep 30;source ./IP_Setup_Master.bash;python3 ./conv_ai_performances.py --topic='/grace_performance'"&
hrsdk start --storage ~/workspace/hrsdk_configs/ --head grace9 --body bodyNC
