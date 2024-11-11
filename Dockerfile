# Use the official ROS 2 Humble base image
FROM ros:humble-ros-base

# Set environment variables
ENV ROS_DISTRO humble
ENV WORKSPACE /ros_ws

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    pip \
    && rm -rf /var/lib/apt/lists/*

# Install python deps
RUN pip install requests

# Initialize rosdep (already done with humble install)
#RUN rosdep init && \
#    rosdep update

# Create a workspace directory
RUN mkdir -p $WORKSPACE/src

# Set the working directory
WORKDIR $WORKSPACE

# Copy source files
COPY ./src $WORKSPACE/src

# Install the ROS 2 packages listed in the workspace (uncomment if needed)
# RUN rosdep install --from-paths src --ignore-src -r -y

# Build the workspace
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    colcon build

# Source the workspace setup file
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
RUN echo "source $WORKSPACE/install/setup.bash" >> ~/.bashrc

# Set the entrypoint to the bash shell
CMD ["/bin/bash"]

