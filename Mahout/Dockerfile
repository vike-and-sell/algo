FROM openjdk:11-jre-slim

# Set environment variables for Mahout
ENV MAHOUT_VERSION 14.1
ENV MAHOUT_HOME /opt/mahout

RUN apt-get update && apt-get install -y wget tar && rm -rf /var/lib/apt/lists/*

# Download and install Mahout
RUN wget https://downloads.apache.org/mahout/$MAHOUT_VERSION/apache-mahout-distribution-$MAHOUT_VERSION.tar.gz && \
    mkdir /opt/mahout && \
    tar -xzf apache-mahout-distribution-$MAHOUT_VERSION.tar.gz -C /opt/mahout && \
    rm apache-mahout-distribution-$MAHOUT_VERSION.tar.gz

ENV PATH $MAHOUT_HOME/bin:$PATH

RUN apt list | grep mahout

WORKDIR $MAHOUT_HOME
CMD ["mahout"]