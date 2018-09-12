FROM mysql
ADD env.sh /env.sh
EXPOSE 22
CMD ["ls"]

