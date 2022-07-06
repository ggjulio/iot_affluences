#### 
I coded two scripts that does the same thing. One in shell and another one in python.
##### The shell one,
I find out that the objectif was pretty similar to a script,
I have written a while ago as a beta tester for a new 42 cursus projet.
So I took some part of this old script. (I just made the [repo public](https://github.com/ggjulio/born2beroot) if you want to look at the original script)


##### Python
It was not really fair for others candidates, to take some code I already written a while ago.
So I just written a second one in python.
Which is also more efficient than a shell script who spawn a lot of commands and pipe them. And some of them probably calling syscalls. (Switching contexts between user space and kernel space take time, while with the python script it probably doesn't happen that much)
In our case, it is not a problems because your iot devices like jetson are pretty powerfull and are probably connected to the mains.
But based on the execution interval, and consuption requirements. We may want to optimize the efficiency.

#### Format size and storage

```
[{DATE}] {HOSTNAME} - {CPU_LOAD};{RAM_USAGE};{DISK_USAGE}
```
```
[2022-07-06T10:51:30+02:00] hostname - 100.0;100.0;100.0
```

time: 27 bytes
delimiters + spaces (including NL): 7B
max hostname length: 64B based on `getconf HOST_NAME_MAX` of the iot device
percentage: 5B * 3 = 15B

max line size: 27 + 7 + 64 + 15 = 113 bytes
line size with hostname 'affluences': 27 + 7 + 10 + 15 = 59 bytes

The script run 14 hours per day, so 840 minutes.
Running a cronjob every minutes will create on average file log of 50 kilobytes.

#### The schedule expression used to run the cronjob
`*/1 8-22 * * 1-5`
- [explanation](https://crontab.guru/#1_8-22_*_*_1-5)

#### ssh connexion

```shell
ssh -i /path/to/private/key user@host 
```
source: `man ssh`

#### python doc
- [psutil module (for cpu, ram and disk usage)](https://psutil.readthedocs.io/en/latest/index.html)
