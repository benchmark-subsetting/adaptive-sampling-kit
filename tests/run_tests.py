#!/usr/bin/nosetests --with-xunit
### This file should be executed with nosetests --with-xunit to generate
### xml test report.
import subprocess
import os.path
from xml.etree import ElementTree as ET

INFORMATION_FILE = "information.xml"

def find_directories(root = None):
    if not root:
        root = os.path.abspath(".")

    test_directories = []
    def accumulate_directories(arg, dirname, fnames):
        if INFORMATION_FILE in fnames:
            arg.append(dirname)

    os.path.walk(root, accumulate_directories , test_directories)
    for d in test_directories: yield d

def read_content(fname):
    #Read content
    return file(fname).read()

def submitCommand (command, params):
    goThere = "."

    #Prepare it
    if ("change_path" in params):
        goThere = params["change_path"];

    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd = goThere);

    #Launch it
    print "Executing -> " + command
    stdout,stderr = p.communicate()

    return stdout, stderr, p.returncode

def fileExists (path, params):
    filePath = path

    if (not os.path.isabs (path)):
        filePath = "./"

        if ("change_path" in params):
            filePath = params["change_path"];

        filePath += "/" + path

    return os.path.exists (filePath)


def getXMLAttribute (listAttributes, attribute, path = None):
    if (not attribute in listAttributes):
        return None

    out = listAttributes[attribute]

    if path:
        out = out.replace ('$PATH', path);

    return out

def run_micro_regression(path):

    #Get current pwd
    pwd = os.path.abspath (".")

    #Get the information
    information_file = path + "/" + INFORMATION_FILE

    if (not os.path.exists (information_file)):
        print path, " does not contain an information file"
        return

    #Now go through the file
    information = read_content (information_file)

    try:
        element = ET.XML(information)
    except:
        message = information_file + " is not a valid XML file"
        raise AssertionError(message)

    params = {}
    #Retrive params
    for subelement in element:
        params[subelement.tag] = getXMLAttribute (subelement.attrib, "value", path);

    #Paranoid test: do we have a command
    if (not "command" in params):
        message = "Command is missing in information file: " + information_file
        raise AssertionError (message)

    #Paranoid test: if we have an output, does it exist
    if ("expected_output" in params):
        if (not fileExists (params["expected_output"], params)):
            message = "Output file: " + params["expected_output"] + " does not exist"
            raise AssertionError (message)

    #Paranoid test: if we have an output, we must have a comparison
    if ("expected_output" in params):
        if (not "obtained_output" in params):
            message = "Expected output file: " + params["expected_output"] + " is defined but not obtained file"
            raise AssertionError (message)

    #Perform preprocess
    if "pre_process" in params:
        stdout,stderr,return_code = submitCommand (params["pre_process"], params)

        if return_code != 0:
            message = ("Pre-process failed: \n\nSTDOUT\n======\n{1}\n\nSTDERR\n"
                    "======\n{2}".format(return_code, stdout, stderr))
            raise AssertionError(message)

    #Create command
    cmd = []
    cmd.append(params["command"])

    if "arguments" in params:
        cmd.append(params["arguments"])

    #Submit command
    stdout,stderr,return_code = submitCommand (" ".join (cmd), params);

    #Expected return handling
    expected_return = 0
    if "return" in params:
        expected_return = int (params["return"])

    #Did it fail?
    if return_code != expected_return:
        message = ("Got return code of {0}, expected {1}.\n\nSTDOUT\n======\n{2}\n\nSTDERR\n"
                "======\n{3}".format(return_code, expected_return, stdout, stderr))
        raise AssertionError(message)

    #Paranoid test: if we have a comparison, does the file now exist
    if ("obtained_output" in params):
        if (not fileExists (params["obtained_output"], params)):
            message = "Obtained output file: " + params["obtained_output"] + " does not exist"
            raise AssertionError (message)
       

    #It did not fail, that's good but do we have an expected output
    if "expected_output" in params:
            
        #We've got both files then we can compare them
        cmd = []

        #Get the diff operator
        diff_operator = "diff -d"
        if ("diff_operator" in params):
            diff_operator = params["diff_operator"]

        cmd.append (diff_operator)
        cmd.append (params["expected_output"])
        cmd.append (params["obtained_output"])

        #Prepare it
        p = subprocess.Popen(" ".join(cmd),
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             )
        #Launch it
        stdout, stderr, return_code = submitCommand (" ".join (cmd), params)

        if return_code != 0:
            message = ("Difference failed: \n\nSTDOUT\n======\n{0}\n\nSTDERR\n"
                    "======\n{1}\n{2}".format(stdout, stderr, os.path.abspath(".")))
            raise AssertionError (message)

    if "post_process" in params:
        stdout,stderr,return_code = submitCommand (params["post_process"], params);

        if return_code != 0:
            message = ("Post process failed: \n\nSTDOUT\n======\n{1}\n\nSTDERR\n"
                    "======\n{2}".format(return_code, stdout, stderr))
            raise AssertionError(message)

def test_all():
    for path in find_directories():
        print "Testing " + path
        yield run_micro_regression, path


if __name__ == "__main__":
    for call, elem in test_all(): 
        run_micro_regression (elem)

