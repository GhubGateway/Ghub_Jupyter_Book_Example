#----------------------------------------------------------------------------------------------------------------------
# Class: Wrapper
# Component of: ghub_vhub_exercise2 (github.com)
# Called from: Invoked as a thread from ghub_exercise1.ipynb
# Purpose: Run a Pegasus workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: Feb 2023
#---------------------------------------------------------------------------------------------------------------------
import sys
import os

#import Rappture
#from Rappture.tools import executeCommand as RapptureExec
# Modified for Python 2 to 3
import hublib.cmd
#help (hublib.cmd.command.executeCommand)

# API for generating Pegasus DAXes
import DAX3 as DAX3
#help (DAX3)

import signal

from newthreading import Thread

def sig_handler(self, signal, frame):
    print ("\nWrapper.py thread: sig_handler signal: ", signal, "\n")
    if Thread.rapptureCommandPid < 0:
        print ("In sig_handler - Thread.rapptureCommandPid < 0\n")
    else:
        if Thread.rapptureCommandPid == 0:
            print ("In sig_handler - Thread.rapptureCommandPid == 0 (child process)\n")
        else:
            print ("In sig_handler - Thread.rapptureCommandPid > 0 (parent process)\n")
            print ("Terminating the workflow\n")
            os.kill(Thread.rapptureCommandPid, signal)
    print ("Wrapper.py thread about to sys.exit(1)")
    sys.exit(1)

# When multiprocessing is used vice threading GUI t.terminate issues a SIGTERM for this process.
signal.signal(signal.SIGHUP, sig_handler)
signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)

# Wrapper class
# Called from ghub_exercise1.ipynb
class Wrapper():
    

    def __init__(self, parent, tooldir, bindir, datadir, workingdir, rundir,\
           lat_south, lat_north, lon_west, lon_east,\
           grassgis_database, grassgis_location, grassgis_mapset, grassgis_map, maxwalltime):

        self.parent = parent
        self.tooldir = tooldir
        self.bindir = bindir
        self.datadir = datadir
        self.workingdir = workingdir
        self.rundir = rundir
        self.lat_south = lat_south
        self.lat_north = lat_north
        self.lon_west = lon_west
        self.lon_east = lon_east
        self.grassgis_database = grassgis_database
        self.grassgis_location = grassgis_location
        self.grassgis_mapset = grassgis_mapset
        self.grassgis_map = grassgis_map
        self.maxwalltime = maxwalltime
    
        #'''
        print('self.parent: ', self.parent)
        print('self.tooldir: ', self.tooldir)
        print('self.bindir: ', self.bindir)
        print('self.datadir: ', self.datadir)
        print('self.workingdir: ', self.workingdir)
        print('self.rundir: ', self.rundir)
        print('self.lat_south: ', self.lat_south)
        print('self.lat_north: ', self.lat_north)
        print('self.lon_west: ', self.lon_west)
        print('self.lon_east: ', self.lon_east)
        print('self.grassgis_database: ', self.grassgis_database)
        print('self.grassgis_location ', self.grassgis_location)
        print('self.grassgis_mapset: ', self.grassgis_mapset)
        print('self.grassgis_map: ', self.grassgis_map)
        print('self.maxwalltime: ', self.maxwalltime)
        #'''
        
        self.run()

    def run(self):

        try:
        
            #print ("Thread.rapptureCommandPid: ", Thread.rapptureCommandPid)
    
    
            #########################################################
            # Paths to executables
            #########################################################
    
            # Launch python scripts.
            python_launch_exec_path = os.path.join(self.tooldir, "remotebin", "pythonLaunch.sh")
            print ("python_launch_exec_path: %s" %python_launch_exec_path)
    
            e_python_launch = DAX3.Executable(namespace="ghub_vhub_exercise2-workflow", name="python-launch", \
                os="linux", arch="x86_64", installed=False)
            e_python_launch.addPFN(DAX3.PFN("file://" + python_launch_exec_path , "local"))
            
            #########################################################
            #########################################################
    
            # Create the Pegasus workflow.
            # Create an abstract DAG
    
            dax = DAX3.ADAG("ghub_vhub_exercise2-workflow")
    
            # Add launch script and input files to the DAX-level replica catalog
    
            dax.addExecutable(e_python_launch)
            
            # Original MATLAB file:
            # Zenodo archive with doi: https://doi.org/10.5281/zenodo.3940768   
            
            # PFNs:
            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN). 
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow. 
            
            
            # Job 1 matlab executable
            filename = "DEM.py"
            filepath = os.path.join(self.bindir, filename)
            DEM_py =  DAX3.File(filename)
            DEM_py.addPFN(DAX3.PFN("file://" + filepath, "local"))
            dax.addFile(DEM_py)
            
            # Job 1 output
            dirname = "%s" %self.grassgis_database
            dirpath = os.path.join(self.workingdir, dirname)
            database =  DAX3.File(dirname)
            database.addPFN(DAX3.PFN("file://" + dirpath, "local"))
            
            # Create the Grass GIS database directory.
            
            jobstep1 = DAX3.Job(namespace="ghub_vhub_exercise2-workflow", name="python-launch")
            jobstep1.addProfile(DAX3.Profile(DAX3.Namespace.GLOBUS,'maxwalltime', self.maxwalltime))
            jobstep1.addArguments("""./DEM.py %s %s %s %s %s %s %s %s""" \
                %(self.lat_south, self.lat_north, self.lon_west, self.lon_east,\
                 self.grassgis_database, self.grassgis_location, self.grassgis_mapset, self.grassgis_map))
            jobstep1.uses(DEM_py, link=DAX3.Link.INPUT)
            jobstep1.uses(database, link=DAX3.Link.OUTPUT, transfer=True)
            dax.addJob(jobstep1)
            
            
            #########################################################
            # Execute the workflow
            #########################################################
    
            dax_filename = "ghub_vhub_exercise2-workflow.dax"
            dax_filepath = os.path.join(self.workingdir,dax_filename);
            fp = open(dax_filepath, "w")
            if fp:
                dax.writeXML(fp)
                fp.close()
                #print ("Wrapper.py thread: %s daxfile created successfully\n" %dax_filepath)
            else:
                print ("Wrapper.py thread: Could not create the %s daxfile\n" %dax_filepath)
                #self.parent.handle_wrapper_error()
                return
    
            # Verify contents
            #fp = open("benthysplitworkflow.dax", "r")
            #file_contents = fp.read()
            #print (file_contents)
            #fp.close()
            
            sys.stdout.flush()
            
            #'''
            submitcmd = ["submit", "--venue", "WF-ccr-ghub", "pegasus-plan", "--dax", "ghub_vhub_exercise2-workflow.dax"]
            #print ("submitcmd: ", submitcmd)
    
            # Fork to allow SIGTERM signal to get sent to RapptureExec
            Thread.rapptureCommandPid = os.fork()
            if (Thread.rapptureCommandPid >= 0):
                if Thread.rapptureCommandPid == 0:
                    # Reference: https://hubzero.org/documentation/1.3.0/tooldevs/grid.rappture_submit
                    # child process.
                    # RapptureExec messages redirected to the output log
                    #print ("child branch: ");
                    #print (Thread.rapptureCommandPid)
                    # This waits until completion (blocks)
                    exitCode,pegasusStdout,pegasusStderr = hublib.cmd.command.executeCommand(submitcmd,streamOutput=True)
                    #print ("Wrapper.py thread: hublib.cmd.command.executeCommand(%s) exit code = %d\n" %(submitcmd, exitCode))
                    if (exitCode == 0):
                        os._exit(0)
                    else:
                        os._exit(exitCode)
                else:
                    # parent process.
                    # Wait for child to complete
                    #print ("wrapper.py thread: Waiting for workflow to complete...\n")
                    print ("Waiting for the workflow to complete...\n")
                    # Send message to the parent's parent to enable the abort button
                    #self.parent.handle_wrapper_initialized()
                    pid, rapptureExitCode = os.waitpid(Thread.rapptureCommandPid, 0)
    
                    Thread.rapptureCommandPid = -1
                    if (rapptureExitCode != 0):
                        # In this case, look for .stderr and .stdout files in the work directory
                        print ("Wrapper.py thread: hublib.cmd.command.executeCommand(%s) returned with a non zero exit code = %d\n" %(submitcmd, rapptureExitCode))
                        #self.parent.handle_wrapper_error()
                        files = os.listdir(self.workingdir)
                        files.sort(key=lambda x: os.path.getmtime(x))
                        for file in files:
                            # Get the numbered Pegasus work directory
                            #print ('type(file): ', type(file)) #<class 'str'>
                            if os.path.isfile(file) and file[0].isdigit() and file.endswith('.stderr'):
                                print ("stderr file: %s\n" %os.path.join(self.workingdir, file))
                                print ("For the ismip6aissvn tool, the following errors were returned while running a Pegasus workflow: ")
                                with open(file) as f:
                                    lines = f.readlines()                                
                                    for line in lines:
                                        if "WARNING" not in line:
                                            print (line)
                                # In case there is more than one stderr file in the working directory
                                break          
                        return
            else:
                print ("Wrapper.py thread: Failed to fork RapptureExec\n")
                #self.parent.handle_wrapper_error()
                return
    
            #'''
            print (" ")
            
        except Exception as e:
            
            print ("Wrapper.py Exception: %s" %str(e))
            print (" ")
            
        return


#######################################################

if __name__ == "__main__":

    print ('sys.argv: ', sys.argv)
    #Wrapper(sys.argv)
