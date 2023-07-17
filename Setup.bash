#This script is supposed to run on Grace nuc

#Config master machine ip
source ./IP_Setup_Master.bash

#Start custom vad process
xterm -hold -e "sleep 30;cd ..; source launch_custom_vad.sh" &

#Performance connector is now legacy
#xterm -hold -e "sleep 30;source ./IP_Setup_Master.bash;python3 ./conv_ai_performances.py --topic='/grace_performance'"&

#Start HRSDK
hrsdk start --storage ~/workspace/hrsdk_configs/ --head grace9 --body bodyNC
