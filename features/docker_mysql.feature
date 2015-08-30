Feature: Showing off behave and docker available

Scenario: Run a simple Behave test
    Given we have behave installed
    When we implement a test
    Then behave will test it for us!

Scenario: Check Docker version
    When we connect to docker
    Then docker version is >=1.5

#Scenario: Build MySQL image
#   When we connect to docker
#    and we create an image mysqldb based on github.com/nkratzke/easymysql

Scenario: Pull MySQL image
    When we connect to docker
     And we pull an image sameersbn/mysql:latest
    Then we can see sameersbn/mysql in the image list

Scenario: Run MySQL in Docker container
    When we connect to docker
     And we create container mysqld from image sameersbn/mysql
     And we start container mysqld
    Then we can see mysqld in the running containers list
