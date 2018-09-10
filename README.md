
## Saving PID of a current process with Java 8 or before

`
int savePid(String filepath) {
		int pid = Integer.parseInt(new File("/proc/self").getCanonicalFile().getName())
		File tmp = new File(filepath)
		tmp.write("$pid")
		return pid
	}
`
