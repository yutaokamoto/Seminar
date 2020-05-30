BEGIN {
    FS=" |\t"
}
{
    if ($1 == "from" && $3=="import" && $4=="*"){
#	print($2)
	cmd="cat "$2".py"
#	print(cmd)
	system(cmd)
    } else {
	print($0)
    }
}