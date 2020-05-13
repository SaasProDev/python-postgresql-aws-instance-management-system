import os, sys, crypt
import argparse
import pexpect
import random, string
import yaml
import ansible_runner


def main():

        r = ansible_runner.interface.run(private_data_dir='/tmp/runner', directory_isolation_base_path='/tmp/runner', json_mode=False, process_isolation=False, host_pattern='localhost', module='shell', module_args='uptime')
        
        print("runner : {}".format(vars(r)))
        
        for each_host_event in r.events:
            print("event --| {}".format(each_host_event['event']))
            print("dict --| {}".format(each_host_event))
        


        print("status : {}".format(r.status))
        print("rc : {}".format(r.rc))
        print("{}: {}".format(r.status, r.rc))
        # successful: 0        
        print("Final status:")
        print(r.stats)


if __name__ == '__main__':
        main()