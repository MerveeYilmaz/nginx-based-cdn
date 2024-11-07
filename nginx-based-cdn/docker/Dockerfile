FROM openresty/openresty:alpine

RUN apk add build-base curl \
    lua5.1 \
    lua5.1-dev \
    readline-dev \
    openssl-dev \
    zlib-dev \
    git
WORKDIR /root
RUN curl -R -O https://luarocks.github.io/luarocks/releases/luarocks-3.11.1.tar.gz

RUN tar zxpf luarocks-3.11.1.tar.gz
WORKDIR /root/luarocks-3.11.1

RUN chmod +x configure

RUN ./configure --lua-version=5.1
RUN make
RUN make install
WORKDIR /root
RUN git clone https://github.com/jkeys089/lua-resty-hmac.git
WORKDIR /root/lua-resty-hmac
RUN luarocks make
RUN luarocks install lua-resty-http
RUN luarocks install lua-resty-base64
RUN cp -rp /root/lua-resty-hmac /usr/local/openresty/lualib/resty/
CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]
STOPSIGNAL SIGQUIT