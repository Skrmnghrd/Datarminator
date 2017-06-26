#!/usr/bin/python
import os
import sys
import getopt
import threading
import logging
import datetime
import sqlite3
import datetime
import timeit
import multiprocessing
#first = inugE[:len(inugE)/2]
#second = inugE[len(inugE)/2:]
#two threads is atmost


def usage():
    a = """
    usage():

    --copy            copies a file from source to destination (default = None)

    --move            moves a file from source to destination (deletes files from source) (default = None)

    -mkl or --makelog       makes a log of copied or scanned files (default = True)

    -d or --destination     sets destination where you wanna copy files

    -t or --threads         lets you set how many threads you want (default = number of folders in source)

    -e or --extensions      lets you set custom extensions (eg: .sh .txt .mp3 .Anastasia .locky .net)

    "-lo" or "--logonly"    just makes a log file out of the scanned files in source

    "--scanall"             scans errything it can find. including your private parts if you allow it

    "--fromtxtfile"         reads everyline form text file and uses it as extension .sh .txt .py 

    "--preserve"            preserves directory file try. so you will not get disoriented when dealing with files.

    "--max"                 for very impatient persons. just wanting to push their machine to do it the fastest way




    example: 
    *copies all content from /root/ to /root/Desktop without file extensions. and shows what it do*

    python script.py --copy -s /root/ -d /root/Desktop/ --scanall --verbose (copies from root to root/Desktop while getting all files and displays what is does)
    example:
    *copies all extensions of whatever you have entered when it asks, from root to Desktop and preserves the file tree. *
    python script.py --copy -s /root/ -d /root/Desktop --extensions --verbose --preserve 




    *threading is being developed. soo umm, ill just upload it when its cool. gonna switch to multiprocessing to go out of GIL.
    """
    print a
    sys.exit()


def logme(Fname, Filename):

    logging.basicConfig(filename=Fname,level=logging.WARNING)
    logging.warning('{0}{1}{2}'.format(Fname,'  ===========>  \t ',Filename))


def walkingthedog(srcc, thread_number, logonly=False, copy=False):
    #print str(inugE)
    items_per_threads = (len(inugE) / int(thread_number) + 1 ) #+1 to avoid 0
    jobs = []
    for i in range (int(items_per_threads)):
        #p = multiprocessing.Process(target=threadme, args=(thread_number,)) ###THREAD NUMBNER IS THE ITEMS PER THREAD SORRY
        p = threading.Thread(target=threadme, args=(thread_number,))
        jobs.append(p)
    for waiting_threads in jobs:

        waiting_threads.start()


    for working_threads in jobs:
        working_threads.join()

def threadme(pop_number): #pop number items per threads 
    listofdirs = []
    global source
    for i in range(pop_number):
        try:

            p = inugE.pop()
            #print listofdirs
            listofdirs.append(p)
            #print listofdirs
        except IndexError as err:
            pass
    for direk in listofdirs:
        for root, subfiles, files in os.walk(direk):
            for filename in files:
                fname = os.path.join(root,filename)
                if scanall == True:
                    list_of_files.append(fname)
                    logme(fname, filename)
                    if verbose == True:
                        print fname
                else:
                    if fname.endswith(tuple(extensions)):
                        list_of_files.append(fname)
                        logme(fname, filename)
                        if verbose == True:
                            print fname
                    else:
                        pass
                if logonly == True:
                    logme(fname)
                #else:
                #    pass
#problem wid dir. umm put whole name of dir
def interact(filename, dest): #COPY PA LANG ni. wala pa move or preserve
    outFile = os.path.join(dest, os.path.basename(filename))
    itexists = os.path.exists(os.path.basename(filename))
    if os.path.exists(outFile) == True:
        print "[!] File %s exists! renaming file " % outFile
        for i in range (99): #tama naman na ka abusado kung 9999999999 na haha
            outFile = os.path.join(dest, str(i) + os.path.basename(filename))
            if os.path.exists(outFile) == True:
                print "[!] Filename exists again. attempting to rename it with another name"
                continue
            else:
                outFile = os.path.join(dest, str(i) + os.path.basename(filename))
                print "[!] Now copying %s with filename of %s" % (filename, outFile)
                try:
                    with open(filename, "rb") as infile:
                        with open(outFile, "wb") as outfile:
                            for line in infile:
                                outfile.write(line)
                    logging.warning('{0}{1}'.format(str(i), os.path.basename(filename)))
                    break
                except:
                    print '[x] Error happend while copying %s' % os.path.basename(filename)
    else:
        try:
            with open(filename, "rb") as infile:
                with open(outFile, "wb") as outfile:
                    for line in infile:
                        outfile.write(line)
            logging.warning('{0}'.format(os.path.basename(filename)))
        except:
            print '[x] Error happend while copying %s' % os.path.basename(filename)
def readfromtext(textfilee):
    with open(textfilee, 'rb') as extensionfile:
        for line in extensionfile:
                striped = line.strip()
                extensions.append(striped)

def preserve_function(filenamee, src, dest):
    try:
        for root, subfiles, files in os.walk(src):
            os.system("mkdir -p {0}{1}".format(dest,root))
    except:
        pass
    outFile = os.path.join(dest + os.path.dirname(filenamee),  os.path.basename(filenamee))
    print outFile + 'OUFILE'
    desty = os.path.join(dest, os.path.dirname(filenamee))
    print desty + 'DESTYYYYy'
    print "[!] Now copying %s >>>> %s " %(filenamee, desty)
    logging.basicConfig(filename='copied.log',level=logging.WARNING)
    logging.warning('{0}'.format(os.path.basename(filenamee)))
    try:
        with open(filenamee, "rb") as infile:
            with open(outFile, "wb") as outfile:
                for line in infile:
                    outfile.write(line)
    except:
        pass

def main():
    global logonly
    global copy
    global list_of_files
    start_time = timeit.default_timer()
    if custom_extensions == True:
        #readfromtext(textfile)
        pass

    try:

        for f in os.listdir(source):
            if os.path.isdir(os.path.join(source, f)):
                inugE.append(os.path.join(source, f))
            if os.path.isfile(os.path.join(source, f)):
                list_of_files.append(os.path.join(source, f))
            if verbose == True:
                print os.path.join(source, f)
    except:
                usage()

    walkingthedog(source, threads, logonly, copy)
    if copy == True and move == True:
        print 'ERROR PLEASE PICK ONLY ONE'
        sys.exit()

    if copy == True and preserve == True:
        print "DUPLICATION OF FILES IF YOU WILL COPY AND PRESERVE"
        is_this_ok = raw_input("Please type anything to continue (ctrl + c to exit) or type exit to stop")
        if is_this_ok in "exit":
            sys.exit()
        else:
            pass



    if copy == False and move == False:
        print 'copy and move is false. nothing to do.'
        pass
    if copy == True:
        for xfiles in list_of_files:
            #salt += 1
            interact(xfiles, destination)
    if move == True:
        for xfiles in list_of_files:
            interact(xfiles, destination)
            #os.remove(xfiles)
    #print "[x] Moved a total of %s file/s"
    if preserve == True:
        for xfiles in list_of_files:
            preserve_function(xfiles, source, destination)
    if verbose == True:
        #print "[$] Total size of files moved/copied/recorded is approximately:"
        #cmd = "du -sh {0} | cut -f1 -d \"/\"".format(destination)
        #os.system(cmd)
        print destination
    elapsed = timeit.default_timer() - start_time
    print "It took %d apprx seconds to finish. \n [/] All tasks done. Bye bye" % (round(elapsed, 2))
#python errormoveplsdeebug.py --copy -s /root/ -d /root/Desktop/ --scanall --verbose
today = datetime.date.today()
now = today.strftime('%b %d %Y')
#asdfasdf = str(now.year) + ':' + str(now.month) + ':' + str(now.day) + '[*]' + str(now.minute) + '.copied.log'
logging.basicConfig(filename=now,level=logging.WARNING)
copy = False
move = False
makelog = False
verbose = False
destination = ""
source = ""
threads = 1
logonly = False
scanall = False
extensions = []
inugE = []
custom_extensions = False
textfile = ""
list_of_files = [] #HEY LIST OF FILES HERE
databasename = ""
tablename = ""
preserve = False



try:
    opts, args = getopt.getopt(sys.argv[1:], "copy:move:makelog:d:s:t:lo:scanall:a:extensions:fromtxtfile:preserve:verbose:databasename:tablename",["copy","move","makelog","destination","source","threads","logonly","scanall","extensions","fromtxtfile","preserve","verbose","databasename","tablename","max"])
except:
    usage()
    print "Unexpected error:", sys.exc_info()[0]
    raise




for o, a in opts:
    if o in ("--copy"):
            copy = True
    elif o in ("--move"):
            move = True
    elif o in ("--makelog"):
            makelog = True
    elif o in ("-d", "--destination"):
            destination = a
    elif o in ("-s", "--source"):
            source = a
    elif o in ("-t", "--threads"):
            threads = a
    elif o in ("-lo", "--logonly"):

            logonly = True
    elif o in ("-SA", "--scanall"):
            scanall = True

    elif o in ("--extensions"):
        while True:
            try:

                enput = raw_input("Please enter extension (ctrl + c to end)")
                extensions.append(str(enput))
            except:
                break

    elif o in ("--fromtxtfile", "--fromtextfile"):
            textfile = str(a)
            custom_extensions = True
    elif o in ("--preserve"):
        preserve = True
    elif o in ("--verbose"):
        verbose = True
    elif o in ("--tablename"):
        tablename = a
    elif o in ("--databasename"):
        databasename = a
    elif o in ("--max"):
        threads = 10000

main()
#print list_of_files


#inugE = [ f for f in os.listdir(source) if os.path.isdir(os.path.join(source, f))]





#printme = [ f for f in os.listdir(src) if os.path.isdir(os.path.join(src, f))]
#sprint printme
# if str.lower(name) in [files.lower() for files in file_list]


#print move ,makelog, verbose,destination ,source ,extensions
#print extensions
