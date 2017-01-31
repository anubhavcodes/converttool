## Utilities for using converttool with ease.

### Instructions

There is a `Vagrantfile` provided as a utility to quickly deploy `converttool` and in as easy and little as 3 commands

1. Download Vagrant from [the official website](https://www.vagrantup.com/downloads.html)

2. Create a directory for our vagrant-box:

	`$ mkdir vagrant-box`

3. Inside vagrant-box copy the `Vagrantfile` provided here and the complete trivago package submitted by me. 

	`$ cp /path/to/Vagrantfile vagrant-box/`
	
	`$ cp -r /path/to/trivago vagrant-box/`

The directory structure should look somewhat like this:
```
vagrant-box
├── Vagrantfile
└── trivago
    ├── LICENSE
    ├── PROBLEM.md
    ├── README.md
    ├── converttool
    ├── dev-requirements.txt
    ├── requirements.txt
    ├── setup.py
    └── tests
    ├── utilities
    └── validate.json
```

4. You may also want to copy any csv to vagrant-box so that you can find it in the vm when it boots

	`cp test.csv vagrant-box`
	
*Note that since vagrant-box will be shared directory between the guest and the hosts, all the contents of `vagrant-box` will be available in the `/vagrant` directory of the guest.* 

5. Run the following commands 

	`$ vagrant init ubuntu/trusty64`
	
	`$ vagrant up`
	
	`$ vagrant ssh`

6. You are now into the vm, where `convertool` is installed and available system wide. You can test it from anywhere on the console using

	`$ converttool json /vagrant/hotels.csv`

