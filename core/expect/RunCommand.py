
def RunCommand(args, timeout=None, logfile=None):
  """Runs a given command through pexpect.run.

  This function acts as a wrapper over pxpect.run . You can have exception or
  return values based on the exitstatus of the command execution. If exitstatus
   is not zero, then it will return -1, unless you want RuntimeError. If there
  is TIMEOUT, then exception is raised. If events do not match, command's
  output is printed, and -1 is returned.
  Args:
    args: command with arguments as an array
    timeout: timeout for pexpect.run .
    logfile: an opened filestream to write the output
  Raises:
    RuntimeError: Command's exit status is not zero
  Returns:
    Returns -1, if bad exitstatus is not zero and when events do not match
    Otherwise returns 0, if everything is fine
  """
  child = pexpect.spawn(args[0], args=args[1:], timeout=timeout,
                        logfile=logfile)
  child.expect(pexpect.EOF)
  child.close()
  if child.exitstatus:
    print (args)
    raise RuntimeError(("Error: {}\nProblem running command. "
                        "Exit status: {}").format(child.before,
                                                  child.exitstatus))
  return 0 
