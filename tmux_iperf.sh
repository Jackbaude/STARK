#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    source .env
else
    echo ".env file not found! Exiting..."
    exit 1
fi

SESSION="starlink_monitor"

# Start a new tmux session
tmux new-session -d -s $SESSION

# Split the window into two panes
tmux split-window -h  # Split into left and right

# Pane 0 (AWS Server)
tmux select-pane -t 0
tmux send-keys "ssh -i $AWS_SSH_KEY ubuntu@$AWS_INSTANCE_IP" C-m
tmux send-keys "cd $GIT_STARK_PATH" C-m
tmux send-keys "export AWS_IP=$AWS_INSTANCE_IP" C-m
tmux send-keys "./aws_machine/aws-iperf.sh" C-m  # Start iperf server on AWS
tmux send-keys "sleep 3" C-m  # Ensure iperf server has time to start before client

# Pane 1 (Starlink Machine SSH & Client Setup)
tmux select-pane -t 1
tmux send-keys "sleep 3" C-m  # Ensure AWS server is ready before running client
tmux send-keys "ssh $STARLINK_SSH_USER@$STARLINK_SSH_HOST" C-m
tmux send-keys "cd $GIT_STARK_PATH" C-m
tmux send-keys "chmod +x starlink_machine/starlink-iperf.sh" C-m
tmux send-keys "export AWS_IP=$AWS_INSTANCE_IP" C-m  # Use AWS instance IP directly
tmux send-keys "./starlink_machine/starlink-iperf.sh" C-m  # Start iperf client

# Attach to session
tmux attach-session -t $SESSION
