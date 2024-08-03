# sudo docker build -t system_health_check .
# sudo docker run -d -p 1024:1024 --rm -it system_health_check

FROM ubuntu@sha256:3f85b7caad41a95462cf5b787d8a04604c8262cdcdf9a472b8c52ef83375fe15
#FROM multiarch/qemu-user-static

WORKDIR /home/ctf

COPY chall .
COPY libcapstone.so.4 /lib/x86_64-linux-gnu/libcapstone.so.4
COPY libglib-2.0.so.0 /lib/x86_64-linux-gnu/libglib-2.0.so.0
RUN mkdir lib
COPY lib/* ./lib/
COPY flag ./Flag.txt
COPY qemu-mips .
COPY ynetd .

RUN chown root:root ./Flag.txt

EXPOSE 1024
EXPOSE 1234
CMD ./ynetd -p 1024 "./qemu-mips -L . chall"

