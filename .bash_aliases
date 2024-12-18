
alias vim="nvim"
function cd() {

	builtin cd "$1"
	ls -ACF
}

function op() {

	openssl s_client -connect $1:$2

}
