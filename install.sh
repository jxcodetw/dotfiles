# check number of arguments
if test "$#" -eq 0; then
	me=`basename "$0"`
	echo "Usage: ./$me <module1> <module2> ..."
	exit
fi

# for each command line argument
for module; do
	# check if subdir exist
	if [[ ! -d $module ]]; then
		echo "Module $module doesn't exist"
		continue
	fi

	# get all file and dir in the subdir
	files=$(find $module -maxdepth 1 ! -path $module)

	# if any of the config is present then skip this one
	installed=false
	for file in $files; do
		if [[ -f $target ]]; then
			installed=true
			break
		fi
	done
	if [[ $installed ]]; then
		echo Module $module skipped.
		continue
	fi

	# symlink them to $HOME
	for file in $files; do
		fullpath="$(readlink -f $file)"
		target="$HOME/$(basename -- $file)"
		ln -s $fullpath $target
	done
	echo $module installed.
done
