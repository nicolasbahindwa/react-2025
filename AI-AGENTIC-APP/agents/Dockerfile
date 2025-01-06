FROM langchain/langgraph-api:3.11 as agent

LABEL maintainer="AI AGENT" \
    version="1.0" \
    description="Langgraph API - build Environment for agent service"


# set working directory
WORKDIR /deps/agents/src

# build variables for build and runtime
ENV BUILD_DEPS=""\
    APP_DEPS="curl" \
    PYTHONPATH=$(pwd):$PYTHONPATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="${PATH}:/home/langgraph/.local/bin" \
    LANGSERVE_GRAPHS='{"task_ai": "/deps/agents/src/task_ai/graph.py:graph"}'


# System setup and dependencies
RUN apt-get update \
    && apt-get install -y ${BUILD_DEPS} ${APP_DEPS} --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && groupadd -g "${GID}" langgraph \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" langgraph \
    && chown langgraph:langgraph -R /deps/agents

# switch to non-root user
USER langgraph

#Copy application code
COPY agents/ /deps/agents/src/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --upgrade --no-cache-dir -c /api/constraints.txt -r /deps/agents/src/requirements.txt \
    && rm -rf /tmp/pip-* 

# Setup project configuration
RUN set -ex && \
    for line in '[project]' \
                'name = "agents"' \
                'version = "0.1"' \
                '[tool.setuptools.package-data]' \
                '"*" = ["**/*"]'; do \
        echo "$line" >> /deps/agents/pyproject.toml; \
    done

# Install editable packages
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -c /api/constraints.txt -e /deps/* \
    && rm -rf /tmp/pip-*

EXPOSE 8000