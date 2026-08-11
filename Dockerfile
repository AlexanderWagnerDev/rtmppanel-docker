FROM alexanderwagnerdev/alpine:builder AS builder

RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 py3-pip python3-dev git gcc musl-dev libffi-dev openssl-dev rust cargo bash tzdata && \
    rm -rf /var/cache/apk/*

WORKDIR /app

ARG PANEL_REPO=https://github.com/OpenRTMP/librtmp2-server-panel.git
ARG PANEL_REF=v0.1.6

RUN git clone --depth 1 --branch "$PANEL_REF" "$PANEL_REPO" . && \
    rm -rf .git

RUN python3 -m venv /venv

RUN /bin/sh -c "source /venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt"

ENV PATH="/venv/bin:$PATH"

FROM alexanderwagnerdev/alpine:latest

RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 bash libffi openssl libgcc libstdc++ tzdata && \
    rm -rf /var/cache/apk/*

WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /venv /venv

RUN mkdir -p /data && \
    adduser -D -h /app openrtmp && \
    chown -R openrtmp:openrtmp /app /data

ENV PATH="/venv/bin:$PATH"
ENV PANEL_DB_PATH=/data/panel.db

EXPOSE 8000/tcp

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER openrtmp

CMD ["/entrypoint.sh"]
